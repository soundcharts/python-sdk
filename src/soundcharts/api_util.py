import requests
import time
import json
import logging
from datetime import datetime, timedelta
from requests.structures import CaseInsensitiveDict
from http import HTTPStatus
from math import ceil

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Accept all levels; handlers will filter

# Console handler (default setup, level adjusted later)
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)


# File handler (delayed creation)
class LazyFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=True):
        super().__init__(filename, mode, encoding, delay=delay)


log_file_handler = LazyFileHandler("soundcharts_api.log")
log_file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)

# Global config variables
HEADERS = None
BASE_URL = None
MAX_RETRIES = 5
RETRY_DELAY = 10
EXCEPTION_LOG_LEVEL = logging.ERROR


def setup(
    app_id,
    api_key,
    base_url="https://customer.api.soundcharts.com",
    max_retries=5,
    retry_delay=10,
    console_log_level=logging.INFO,
    file_log_level=logging.WARNING,
    exception_log_level=logging.ERROR,
):
    """
    Initialize the Soundcharts client.

    :param app_id: Soundcharts App ID
    :param api_key: Soundcharts API Key
    :param base_url: Base URL for API. Default: production.
    :param max_retries: Max number of retries in case of an error 500. Default: 5.
    :param retry_delay: Time in seconds between retries for a 500 error. Default: 10.
    :param console_log_level: The severity of issues written to the console. Default: logging.INFO.
    :param file_log_level: The severity of issues written to the logging file. Default: logging.WARNING.
    :param exception_log_level: The severity of issues that cause exceptions. Default: logging.ERROR.
    """
    global HEADERS, BASE_URL, MAX_RETRIES, RETRY_DELAY, EXCEPTION_LOG_LEVEL

    HEADERS = CaseInsensitiveDict()
    HEADERS["x-app-id"] = app_id
    HEADERS["x-api-key"] = api_key

    BASE_URL = base_url
    MAX_RETRIES = max_retries
    RETRY_DELAY = retry_delay
    EXCEPTION_LOG_LEVEL = exception_log_level

    # Clear existing handlers to avoid duplication
    logger.handlers.clear()

    # Add console handler with updated level
    console_handler.setLevel(console_log_level)
    logger.addHandler(console_handler)

    # Add file handler with updated level
    log_file_handler.setLevel(file_log_level)
    logger.addHandler(log_file_handler)


def request_wrapper(
    endpoint,
    params=None,
    body=None,
    max_retries=MAX_RETRIES,
    retry_delay=RETRY_DELAY,
    method=None,
    timeout=10,
):
    """
    Sends a request to the Soundcharts API with error handling and retries.

    :param endpoint: The API endpoint (string).
    :param params: Dictionary of query parameters (default: None).
    :param body: JSON payload (default: None).
    :param max_retries: Max retries for 5xx errors.
    :param retry_delay: Delay between retries in seconds.
    :param method: HTTP method: GET, POST, DELETE (default: POST if body else GET).
    :param timeout: Request timeout in seconds.
    :return: Parsed JSON response if successful, None for 404, raises RuntimeError for other errors.
    """
    global HEADERS

    url = f"{BASE_URL}{endpoint}"
    headers = HEADERS.copy()
    params = params or {}

    if body:
        headers["Content-Type"] = "application/json"

    for attempt in range(max_retries):
        try:
            # Determine HTTP method
            if method is None:
                method_func = requests.post if body else requests.get
                method_name = "POST" if body else "GET"
            elif method.lower() == "delete":
                method_func = requests.delete
                method_name = "DELETE"
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Log outgoing request
            full_url = requests.Request(method_name, url, params=params).prepare().url
            logger.info(
                f"Attempt {attempt + 1}/{max_retries}: {method_name} {full_url}"
            )
            logger.debug(f"Headers: {headers}")
            if params:
                logger.debug(f"Params: {params}")
            if body:
                logger.debug(f"Body: {json.dumps(body)}")

            # Execute the request
            response = method_func(
                url,
                params=params,
                headers=headers,
                data=json.dumps(body) if body else None,
                timeout=timeout,
            )

            logger.debug(f"Response Status: {response.status_code}")
            logger.debug(f"Response Body: {response.text}")

            # Success
            if response.status_code == HTTPStatus.OK:
                return response.json()

            # Extract error message
            try:
                error_data = response.json()
                message = (
                    error_data.get("errors", [{}])[0].get("message")
                    or error_data.get("message")
                    or response.text
                )
            except (ValueError, IndexError, KeyError):
                message = response.text

            # Handle known errors
            if response.status_code == HTTPStatus.NOT_FOUND:
                log_msg = f"404 Not Found: {url} — {message}"
                logger.warning(log_msg)
                if logging.WARNING >= EXCEPTION_LOG_LEVEL:
                    raise RuntimeError(log_msg)
                return None

            # Server errors
            elif response.status_code in {
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
                HTTPStatus.GATEWAY_TIMEOUT,
            }:
                logger.warning(
                    f"{response.status_code} Server Error: {message} — Retrying ({attempt + 1}/{max_retries})"
                )
                time.sleep(retry_delay)

            # Authorization errors
            elif response.status_code in {
                HTTPStatus.TOO_MANY_REQUESTS,
                HTTPStatus.FORBIDDEN,
                HTTPStatus.UNAUTHORIZED,
            }:

                if response.status_code == 429 and "maximum request count" in message:
                    logger.warning(
                        f"{response.status_code} Error: {message} — Retrying in 30 seconds ({attempt + 1}/{max_retries})"
                    )
                    time.sleep(30)
                else:
                    log_msg = f"{response.status_code} Error: {message}"
                    logger.error(log_msg)
                    if logging.ERROR >= EXCEPTION_LOG_LEVEL:
                        raise RuntimeError(log_msg)
                    return None

            # Unknown errors
            else:
                logger.error(response.status_code, log_msg)
                if logging.ERROR >= EXCEPTION_LOG_LEVEL:
                    raise RuntimeError(f"HTTP {response.status_code}: {message}")

        except requests.RequestException as e:
            logger.error(f"Request exception: {e}")
            if attempt == max_retries - 1:
                raise RuntimeError("Maximum retry attempts reached.") from e

    final_msg = "Unhandled error or maximum retries exceeded."
    logger.error(final_msg)
    if logging.ERROR >= EXCEPTION_LOG_LEVEL:
        raise RuntimeError(final_msg)

    return None


def request_looper(
    endpoint,
    params=None,
    body=None,
    handle_period=True,
    print_progress=False,
):
    """
    Sends requests to the Soundcharts API, looping through time periods or paginated data as needed.

    :param endpoint: The API endpoint (string).
    :param params: Dictionary of query parameters (default: None).
    :param body: JSON payload (default: None).
    :param handle_period: Enable period splitting for long date ranges (default: True).
    :param print_progress: Whether to print progress.
    :return: Aggregated API response.
    :raises: RuntimeError for rate-limiting or persistent server errors.
    """

    def str_to_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")

    def str_date_add(date_str, amount):
        new_date = str_to_date(date_str) + timedelta(days=amount)
        return new_date.strftime("%Y-%m-%d")

    def date_difference(start_date, end_date):
        return (str_to_date(end_date) - str_to_date(start_date)).days

    def is_empty(obj):
        return obj is None or len(obj) == 0

    def print_percentage(progress, total):
        if total > 0:
            percentage = min(round(progress * 100 / total, 2), 100)
            print(f"\r{percentage}% done  ", end="", flush=True)
            if progress >= total:
                print()

    # Setup
    params = params.copy() if params else {}
    results = {}
    period = 90
    loops = 1

    # Limit handling
    limit = params.get("limit")
    if limit:
        limit = int(limit)
        params["limit"] = min(limit, 100)

    # Period loop setup
    start_date, end_date = params.get("startDate"), params.get("endDate")
    if handle_period and end_date:
        start_date = start_date or str_date_add(end_date, -period)
        loops = ceil(date_difference(start_date, end_date) / period)

    while period > 0:
        # Adjust period boundaries
        if handle_period and end_date:
            params["endDate"] = end_date
            period = min(date_difference(start_date, end_date), 90)
            params["startDate"] = str_date_add(end_date, -period)
            end_date = str_date_add(params["startDate"], -1)

        next_get = endpoint
        options = params.copy()
        progress = 0

        # Pagination loop
        while next_get:
            response = request_wrapper(next_get, options, body=body)

            if is_empty(response):
                break

            if not results:
                results = response
            elif "items" in results and "items" in response:
                merged_items = results.get("items", []) + response.get("items", [])
                response["items"] = merged_items
                results = response

            next_get = results.get("page", {}).get("next")
            options = None

            # Progress
            progress = len(results.get("items") or [])
            total = limit or results.get("page", {}).get("total", progress) * loops
            if "page" in results:
                results["page"]["total"] = max(
                    results["page"].get("total", 0), progress
                )
            if print_progress:
                print_percentage(progress, total)

            if limit and progress >= limit:
                break

        if not handle_period or limit and progress >= limit:
            break
        if start_date == end_date or date_difference(start_date, end_date) < 0:
            break

    if results.get("items") and limit:
        results["items"] = results["items"][:limit]

    return results


def sort_items_by_date(result, reverse=False, key="date"):

    result["items"] = sorted(
        result["items"],
        key=lambda x: datetime.fromisoformat(x[key].replace("Z", "")),
        reverse=reverse,
    )

    return result
