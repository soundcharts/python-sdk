from .api_util import request_wrapper, request_looper, sort_items_by_date


class Venue:

    @staticmethod
    def get_venue_metadata(venue_uuid):
        """
        Get the venue’s metadata.

        :param venue_uuid: A venue uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/venue/{venue_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_ids(venue_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this venue.

        :param venue_uuid: A venue uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/venue/{venue_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_concerts(venue_uuid, start_date=None, end_date=None, offset=0, limit=100):
        """
        Get the list of concerts of a venue.

        :param venue_uuid: A venue uuid.
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

        endpoint = f"/api/v2/venue/{venue_uuid}/concerts"
        result = request_looper(endpoint, params, handle_period=False)
        return {} if result is None else sort_items_by_date(result, True)

    @staticmethod
    def get_concert_details(concert_uuid):
        """
        Get a specific concert's details, including the list of programmed artists.

        :param venue_uuid: A concert uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/venue/concert/{concert_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}
