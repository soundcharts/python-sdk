import asyncio
import aiohttp
import json
import logging
from requests.structures import CaseInsensitiveDict
from http import HTTPStatus
from datetime import datetime
from urllib.parse import urlencode

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)


class LazyFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=True):
        super().__init__(filename, mode, encoding, delay=delay)


log_file_handler = LazyFileHandler("soundcharts_api.log")
log_file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)

# Global config
HEADERS = None
BASE_URL = None
PARALLEL_REQUESTS = 5
MAX_RETRIES = 5
RETRY_DELAY = 10
TIMEOUT = 10
EXCEPTION_LOG_LEVEL = logging.ERROR


def setup(
    app_id,
    api_key,
    base_url="https://customer.api.soundcharts.com",
    parallel_requests=5,
    max_retries=5,
    retry_delay=10,
    timeout=10,
    console_log_level=logging.WARNING,
    file_log_level=logging.WARNING,
    exception_log_level=logging.ERROR,
):
    global HEADERS, BASE_URL, PARALLEL_REQUESTS, MAX_RETRIES, RETRY_DELAY, TIMEOUT, EXCEPTION_LOG_LEVEL

    HEADERS = CaseInsensitiveDict()
    HEADERS["x-app-id"] = app_id
    HEADERS["x-api-key"] = api_key

    BASE_URL = base_url
    PARALLEL_REQUESTS = parallel_requests
    MAX_RETRIES = max_retries
    RETRY_DELAY = retry_delay
    TIMEOUT = timeout
    EXCEPTION_LOG_LEVEL = exception_log_level

    logger.handlers.clear()

    console_handler.setLevel(console_log_level)
    logger.addHandler(console_handler)

    log_file_handler.setLevel(file_log_level)
    logger.addHandler(log_file_handler)


async def _request_wrapper_async(
    endpoint,
    params=None,
    body=None,
    max_retries=None,
    retry_delay=None,
    timeout=None,
    method=None,
    session: aiohttp.ClientSession | None = None,
):
    """
    Async HTTP wrapper with retries.
    """
    global HEADERS, BASE_URL, MAX_RETRIES, RETRY_DELAY, TIMEOUT

    if max_retries is None:
        max_retries = MAX_RETRIES
    if retry_delay is None:
        retry_delay = RETRY_DELAY
    if timeout is None:
        timeout = TIMEOUT

    url = f"{BASE_URL}{endpoint}"
    headers = dict(HEADERS or {})

    raw_params = params or {}
    params = {}

    for k, v in (raw_params or {}).items():
        if not v:
            continue
        if isinstance(v, bool):
            params[k] = "true" if v else "false"
            continue
        params[k] = v

    if body:
        headers["Content-Type"] = "application/json"

    owns_session = False
    if session is None:
        timeout_cfg = aiohttp.ClientTimeout(total=timeout)
        session = aiohttp.ClientSession(timeout=timeout_cfg)
        owns_session = True

    try:
        for attempt in range(max_retries):
            try:
                if method is None:
                    method_name = "POST" if body else "GET"
                elif method.lower() == "delete":
                    method_name = "DELETE"
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                if params:
                    full_url = f"{url}?{urlencode(params, doseq=True)}"
                else:
                    full_url = url

                logger.info(
                    f"Attempt {attempt + 1}/{max_retries}: {method_name} {full_url}"
                )
                logger.debug(f"Headers: {headers}")
                if params:
                    logger.debug(f"Params: {params}")
                if body:
                    logger.debug(f"Body: {json.dumps(body)}")

                async with session.request(
                    method_name,
                    url,
                    params=params,
                    headers=headers,
                    data=json.dumps(body) if body else None,
                ) as response:
                    status = response.status
                    text = await response.text()

                    logger.debug(f"Response Status: {status}")
                    logger.debug(f"Response Body: {text}")

                    if status == HTTPStatus.OK:
                        try:
                            return await response.json()
                        except Exception:
                            return text

                    # Extract error message
                    try:
                        error_data = await response.json()
                        message = (
                            error_data.get("errors", [{}])[0].get("message")
                            or error_data.get("message")
                            or text
                        )
                    except Exception:
                        message = text

                    # 404
                    if status == HTTPStatus.NOT_FOUND:
                        log_msg = f"404 Not Found: {full_url} — {message}"
                        logger.warning(log_msg)
                        if logging.WARNING >= EXCEPTION_LOG_LEVEL:
                            raise RuntimeError(log_msg)
                        return None

                    # 5xx
                    elif status in {
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                        HTTPStatus.BAD_GATEWAY,
                        HTTPStatus.SERVICE_UNAVAILABLE,
                        HTTPStatus.GATEWAY_TIMEOUT,
                    }:
                        logger.warning(
                            f"{status} Server Error: {message} when calling {full_url} — "
                            f"Retrying ({attempt + 1}/{max_retries})"
                        )
                        await asyncio.sleep(retry_delay)

                    # Auth / rate limit
                    elif status in {
                        HTTPStatus.TOO_MANY_REQUESTS,
                        HTTPStatus.FORBIDDEN,
                        HTTPStatus.UNAUTHORIZED,
                    }:
                        if (
                            status == HTTPStatus.TOO_MANY_REQUESTS
                            and "maximum request count" in message
                        ):
                            logger.warning(
                                f"{status} Error: {message} when calling {full_url} — "
                                f"Retrying in 30 seconds ({attempt + 1}/{max_retries})"
                            )
                            await asyncio.sleep(30)
                        else:
                            log_msg = (
                                f"{status} Error: {message} when calling {full_url}"
                            )
                            logger.error(log_msg)
                            if logging.ERROR >= EXCEPTION_LOG_LEVEL:
                                raise RuntimeError(log_msg)
                            return None

                    else:
                        log_msg = (
                            f"{status} Unknown Error: {message} when calling {full_url}"
                        )
                        logger.error(log_msg)
                        if logging.ERROR >= EXCEPTION_LOG_LEVEL:
                            raise RuntimeError(f"HTTP {status}: {message}")

            except aiohttp.ClientError as e:
                logger.error(f"Request exception: {e}")
                if attempt == max_retries - 1:
                    raise RuntimeError(
                        f"Maximum retry attempts reached when calling {full_url}."
                    ) from e

        final_msg = (
            f"Unhandled error or maximum retries exceeded when calling {full_url}."
        )
        logger.error(final_msg)
        if logging.ERROR >= EXCEPTION_LOG_LEVEL:
            raise RuntimeError(final_msg)

        return None

    finally:
        if owns_session and session is not None:
            await session.close()


async def _request_looper_async(
    endpoint,
    params=None,
    body=None,
    print_progress=False,
    max_parallel_requests=5,
):
    def print_percentage(progress, total):
        if total > 0:
            percentage = min(round(progress * 100 / total, 2), 100)
            print(f"\r{percentage}% done  ", end="", flush=True)
            if progress >= total:
                print()

    params = params.copy() if params else {}
    results = {}

    # Limit / offset
    raw_limit = params.pop("limit", None)
    if raw_limit is not None:
        limit = int(raw_limit)
        params["limit"] = min(limit, 100)  # page size
    else:
        limit = None

    offset = int(params.get("offset") or 0)
    params["offset"] = max(offset, 0)

    timeout_cfg = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout_cfg) as session:
        # First page
        first_params = params.copy()
        results = await _request_wrapper_async(
            endpoint,
            first_params,
            body=body,
            session=session,
        )

        if not results or "items" not in results:
            return results

        items = list(results.get("items", []))

        first_page = results.get("page", {}) or {}
        total_server = first_page.get("total", len(items))
        total_effective = (
            min(total_server, limit) if limit is not None else total_server
        )

        if print_progress:
            print_percentage(len(items), total_effective)

        # Are we fetching the full dataset or a limited slice?
        fetched_all = (limit is None) or (limit >= total_server)

        if len(items) >= total_effective:
            if limit is not None:
                items = items[:limit]
            results["items"] = items

            # pagination from first page (also "last fetched" here)
            results["page"] = dict(first_page) if first_page else {}
            results["page"]["total"] = total_server

            if fetched_all:
                results["page"]["next"] = None  # only if we truly fetched all

            return results

        page_size = params.get("limit", 100)
        extra_offsets = list(range(offset + page_size, total_effective, page_size))
        if not extra_offsets:
            if limit is not None:
                items = items[:limit]
            results["items"] = items

            results["page"] = dict(first_page) if first_page else {}
            results["page"]["total"] = total_server
            if fetched_all:
                results["page"]["next"] = None

            return results

        sem = asyncio.Semaphore(max_parallel_requests)

        async def fetch_page(off):
            page_params = params.copy()
            page_params["offset"] = off
            page_params["limit"] = page_size
            async with sem:
                resp = await _request_wrapper_async(
                    endpoint,
                    page_params,
                    body=body,
                    session=session,
                )
            return off, resp

        tasks = [asyncio.create_task(fetch_page(o)) for o in extra_offsets]

        last_page_offset = offset
        last_page_block = first_page if first_page else {}

        for task in asyncio.as_completed(tasks):
            off, response = await task
            if not response or "items" not in response:
                continue

            page_items = response.get("items") or []
            if page_items:
                items.extend(page_items)

            page_block = response.get("page") or {}
            if off >= last_page_offset and page_block:
                last_page_offset = off
                last_page_block = page_block

            if print_progress:
                progress = min(len(items), total_effective)
                print_percentage(progress, total_effective)

            if len(items) >= total_effective:
                break

        if limit is not None:
            items = items[:limit]

        results["items"] = items

        # Pagination = last logical page we fetched
        results["page"] = dict(last_page_block) if last_page_block else {}
        results["page"]["total"] = total_server  # always true total

        if fetched_all:
            # only overwrite next if we truly reached the server end
            results["page"]["next"] = None

        results["page"].setdefault("offset", last_page_offset)
        results["page"].setdefault("limit", page_size)

        return results


def _run_blocking(coro):
    """
    Run an async coroutine in a blocking way.
    Used to provide a sync public API on top of async internals.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop -> normal script -> safe
        return asyncio.run(coro)
    else:
        # Already in an event loop -> calling sync API from async code is a bad idea
        raise RuntimeError(
            "Soundcharts sync API called from an async context. "
            "Use the async API directly instead."
        )


def request_wrapper(
    endpoint,
    params=None,
    body=None,
    max_retries=None,
    retry_delay=None,
    timeout=None,
    method=None,
):
    """
    Public sync API: wraps the async paginator.
    """
    return _run_blocking(
        _request_wrapper_async(
            endpoint,
            params=params,
            body=body,
            max_retries=max_retries,
            retry_delay=retry_delay,
            timeout=timeout,
            method=method,
        )
    )


def request_looper(
    endpoint,
    params=None,
    body=None,
    print_progress=False,
):
    """
    Public sync API: wraps the async paginator.
    """
    return _run_blocking(
        _request_looper_async(
            endpoint,
            params=params,
            body=body,
            print_progress=print_progress,
        )
    )


def sort_items_by_date(result, reverse=False, key="date"):

    if result == None or len(result) == 0 or "items" not in result:
        return result

    if key is not None:
        sort_key = lambda x: datetime.fromisoformat(x[key].replace("Z", ""))
    else:
        sort_key = lambda x: datetime.fromisoformat(x.replace("Z", ""))

    result["items"] = sorted(
        result["items"],
        key=sort_key,
        reverse=reverse,
    )

    return result


def list_join(list, separator=","):
    result_string = separator.join(str(item) for item in list)
    return result_string
