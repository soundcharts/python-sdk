from .api_util import request_wrapper, request_looper, sort_items_by_date


class Festival:

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
