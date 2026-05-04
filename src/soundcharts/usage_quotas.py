from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
)


class UsageQuotas:

    @staticmethod
    def monitor_api_quota_and_rate_limits():
        """
        Retrieve your current billing quota and technical rate limit consumption.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/team/usage"
        result = request_wrapper(endpoint)
        return result if result is not None else {}


class UsageQuotasAsync:

    @staticmethod
    async def monitor_api_quota_and_rate_limits():
        """
        Retrieve your current billing quota and technical rate limit consumption.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/team/usage"
        result = await request_wrapper_async(endpoint)
        return result if result is not None else {}
