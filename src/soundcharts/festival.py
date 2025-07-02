from .api_util import request_wrapper, request_looper, sort_items_by_date


class Festival:

    @staticmethod
    def get_festivals(
        offset=0,
        limit=100,
        body=None,
        print_progress=False,
    ):
        """
        Get a list of festivals filtered by attributes and stats.

        You can sort and filter festivals in our database using specific parameters such as social metrics, score, capacity or name.
        You'll find available platfom/metricType combinations in the documentation: https://doc.api.soundcharts.com/api/v2/doc/reference/path/festival/get-festivals

        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit (warning: can take up to 100,000 calls - you may want to use parallel processing). Default: 100.
        :param body: JSON Payload. If none, the default sorting will apply (descending soundcharts score) and there will be no filters.
        :param print_progress: Prints an estimated progress percentage (default: False).
        :return: JSON response or an empty dictionary.
        """

        if body == None:
            platform, metric_type = "soundcharts", "score"

            body = {
                "sort": {
                    "platform": platform,
                    "metricType": metric_type,
                    "period": "month",
                    "sortBy": "total",
                    "order": "desc",
                },
                "filters": [],
            }

        endpoint = f"/api/v2/top/festivals"
        params = {
            "offset": offset,
            "limit": limit,
        }

        result = request_looper(endpoint, params, body, print_progress=print_progress)
        return result if result is not None else {}

    @staticmethod
    def get_festival_metadata(festival_uuid):
        """
        Get the festival’s metadata.

        :param festival_uuid: A festival uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/festival/{festival_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_ids(festival_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this festival.

        :param festival_uuid: A festival uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/festival/{festival_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_editions(
        festival_uuid, start_date=None, end_date=None, offset=0, limit=100
    ):
        """
        Get the list of editions of a festival.

        :param festival_uuid: A festival uuid.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD).
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }

        endpoint = f"/api/v2/festival/{festival_uuid}/editions"
        result = request_looper(endpoint, params, handle_period=False)
        return {} if result is None else sort_items_by_date(result, True, "startedAt")

    @staticmethod
    def get_edition_details(edition_uuid):
        """
        Get a specific edition’s details, including the list of programmed artists.

        :param festival_uuid: A festival edition's uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/festival/edition/{edition_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}
