from .api_util import request_wrapper, request_looper, sort_items_by_date


class Radio:

    @staticmethod
    def get_radios(offset=0, limit=100):
        """
        Get the listing of all radios available on Soundcharts.

        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.22/radio"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_radios_by_country(country_code, offset=0, limit=100):
        """
        Get the listing of all radios available on Soundcharts in a specific country.

        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2).
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.22/radio/by-country/{country_code}"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_live_feed(radio_slug, start_date=None, end_date=None, offset=0, limit=100):
        """
        Get a specific radio’s live feed for a specific range of dates.

        :param radio_slug: A radio slug.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/radio/{radio_slug}/live-feed"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result, True, key="airedAt")

    @staticmethod
    def get_ids(radio_slug, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this radio.

        :param radio_slug: A radio slug.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/radio/{radio_slug}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}
