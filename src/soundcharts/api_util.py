import requests
import time
import json
import logging
from datetime import datetime, timedelta
from requests.structures import CaseInsensitiveDict
from http import HTTPStatus
import os
from math import ceil

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Accept all levels; filter by handler

# Console handler: show INFO and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)
logger.addHandler(console_handler)


# File handler: only logs WARNING and above, and delays file creation
class LazyFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=True):
        super().__init__(filename, mode, encoding, delay=delay)


log_file_handler = LazyFileHandler("soundcharts_api.log")
log_file_handler.setLevel(logging.WARNING)  # Only log WARNING or above
log_file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)
logger.addHandler(log_file_handler)


# Global variables to store API credentials
HEADERS = None
BASE_URL = None

# Config
LOG_ERRORS = True
MAX_RETRIES = 5
RETRY_DELAY = 10


def setup(
    app_id,
    api_key,
    base_url="https://customer.api.soundcharts.com",
    log_errors=True,
    max_retries=5,
    retry_delay=10,
):
    """
    Setup API credentials and logging preference for the module.

    :param app_id: Soundcharts App ID
    :param api_key: Soundcharts API Key
    :param base_url: Base URL for API (default: production)
    :param log_errors: If True, logs errors to file and console
    :param max_retries: Max number of retries in case of an error 500 (default: 5).
    :param retry_delay: Time in seconds between retries for a 500 error (default: 10).
    """
    global HEADERS, BASE_URL, LOG_ERRORS

    HEADERS = CaseInsensitiveDict()
    HEADERS["x-app-id"] = app_id
    HEADERS["x-api-key"] = api_key

    BASE_URL = base_url
    LOG_ERRORS = log_errors
    MAX_RETRIES = max_retries
    RETRY_DELAY = retry_delay


def request_wrapper(
    endpoint,
    params=None,
    body=None,
    max_retries=MAX_RETRIES,
    retry_delay=RETRY_DELAY,
    method=None,
    debug=True,
    timeout=10,
):
    """
    Sends a request to the Soundcharts API with error handling and retries.

    :param endpoint: The API endpoint (string).
    :param params: Dictionary of query parameters to append to the URL (default: None).
    :param body: JSON Payload (default: None).
    :param max_retries: Max number of retries in case of an error 500 (default: specified in client setup).
    :param retry_delay: Time in seconds between retries for a 500 error (default: specified in client setup).
    :param method: The request method (default: POST when a body is included, GET otherwise).
    :param debug: Boolean flag to enable debug messages (default: True).
    :return: The response JSON if the request is successful.
    :raises: RuntimeError for 429, 403 errors, or after max retries for 500 errors.
    """
    global HEADERS, LOG_ERRORS
    url = f"{BASE_URL}{endpoint}"
    headers = HEADERS.copy()
    params = params or {}

    if body:
        headers["Content-Type"] = "application/json"

    for attempt in range(max_retries):
        try:
            # Select HTTP method
            if method is None:
                method_func = requests.post if body else requests.get
            elif method.lower() == "delete":
                method_func = requests.delete
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Send request
            response = method_func(
                url,
                params=params,
                headers=headers,
                data=json.dumps(body) if body else None,
                timeout=timeout,
            )

            # Ajouter la possibilité de loguer en info chaque appel
            # Success
            if response.status_code == HTTPStatus.OK:
                return response.json()

            # Handle known error formats
            try:
                error_data = response.json()
                message = (
                    error_data.get("errors", [{}])[0].get("message")
                    or error_data.get("message")
                    or response.text
                )
            except (ValueError, IndexError, KeyError):
                message = response.text

            # Error handling
            if response.status_code == HTTPStatus.NOT_FOUND:
                if debug and LOG_ERRORS:
                    logger.warning(f"404 Not Found: {url} — {message}")
                return None

            elif response.status_code in {
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
                HTTPStatus.GATEWAY_TIMEOUT,
            }:
                if debug and LOG_ERRORS:
                    logger.warning(
                        f"{response.status_code} Server Error: {message} — Retrying ({attempt + 1}/{max_retries})"
                    )
                time.sleep(retry_delay)

            elif response.status_code in {
                HTTPStatus.TOO_MANY_REQUESTS,
                HTTPStatus.FORBIDDEN,
            }:
                raise RuntimeError(f"{response.status_code} Error: {message}")

            else:
                raise RuntimeError(f"HTTP {response.status_code}: {message}")

        except requests.RequestException as e:
            if debug and LOG_ERRORS:
                logger.error(f"Request exception: {e}")
            if attempt == max_retries - 1:
                raise RuntimeError("Maximum retry attempts reached.") from e

    raise RuntimeError("Unhandled error or maximum retries exceeded.")


def request_looper(
    endpoint,
    params=None,
    body=None,
    max_retries=MAX_RETRIES,
    retry_delay=RETRY_DELAY,
    print_progress=False,
    debug=True,
):
    """
    Sends requests to the Soundcharts API, looping to cover wider periods or larger limits than normally allowed.

    :param endpoint: The API endpoint (string).
    :param params: Dictionary of query parameters to append to the URL (default: None).
    :param body: JSON Payload (default: None).
    :param max_retries: Max number of retries in case of an error 500 (default: specified in client setup).
    :param retry_delay: Time in seconds between retries for a 500 error (default: specified in client setup).
    :param print_progress: Prints an estimated progress percentage (default: False).
    :param debug: Boolean flag to enable debug messages (default: True).
    :return: The response JSON if the request is successful.
    :raises: RuntimeError for 429, 403 errors, or after max retries for 500 errors.
    """
    results, start_date, end_date, limit = None, None, None, None
    loops = 1
    progress = 0
    total = None
    period = 90

    def str_to_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")

    def str_date_add(date_str, amount):
        new_date = str_to_date(date_str) + timedelta(days=amount)
        return new_date.strftime("%Y-%m-%d")

    def date_difference(start_date, end_date):
        return (str_to_date(end_date) - str_to_date(start_date)).days

    def print_percentage(progress, total):
        if total <= 0:
            return None
        percentage = min(round(progress * 100 / total, 2), 100)
        print(f"\r{percentage}% done  ", end="", flush=True)
        if progress >= total:
            print()

    if "endDate" in params and params["endDate"] is not None:
        end_date = params["endDate"]
        if "startDate" in params and params["startDate"] is not None:
            start_date = params["startDate"]
            loops = ceil(date_difference(start_date, end_date) / period)
        else:
            start_date = str_date_add(end_date, -90)

    if "limit" in params:
        if params["limit"] is not None:
            limit = int(params["limit"])
            params["limit"] = min(limit, 100)

    while period > 0:
        if end_date is not None:
            params["endDate"] = end_date
            period = min(date_difference(start_date, end_date), 90)
            params["startDate"] = str_date_add(end_date, -period)
            end_date = str_date_add(params["startDate"], -1)

        get = endpoint
        options = params

        while get is not None:
            response = request_wrapper(
                get,
                options,
                body=body,
                max_retries=max_retries,
                retry_delay=retry_delay,
                debug=debug,
            )

            if response is None or len(response) == 0:
                return results

            if results is None:
                results = response
            else:
                results["items"].extend(response.get("items", []))

            get = response.get("page", {}).get("next")
            if "page" in response:
                results["page"]["next"] = get
                total = limit or (response["page"].get("total", 1) * loops)

                results["page"]["total"] = max(
                    results["page"].get("total", 0), len(results.get("items", []))
                )
                progress = len(results.get("items", []))
                if print_progress:
                    print_percentage(progress, total)
            options = None

            if (
                "items" in results
                and limit is not None
                and len(results["items"]) >= limit
            ):
                break

        if "items" in results and limit is not None and len(results["items"]) >= limit:
            break

        if (
            end_date is None
            or start_date == end_date
            or date_difference(start_date, end_date) < 0
        ):
            break

    if "items" in results and limit is not None:
        results["items"] = results["items"][:limit]

    return results


def json_import(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # print(f"{filename} loaded.")
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Handle missing or corrupted file
