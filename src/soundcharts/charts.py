from .api_util import request_wrapper, request_looper


class Charts:

    @staticmethod
    def get_radio_ranking(
        platform="instagram",
        metric_type="followers",
        sort_by="total",
        period="month",
        radio_country_code=None,
        min_value=None,
        max_value=None,
        min_change=None,
        max_change=None,
        token=None,
    ):
        """
        Get a listing of radios, ranked by a specific platform metric.

        :param platform: A platform code. Global, instagram, facebook, tiktok, twitter, youtube. Default: instagram.
        :param metric_type: fan, followers, reach. Default: followers.
        :param sort_by: total, change, percent. Default: total.
        :param period: month, quarter. Default: month.
        :param radio_country_code: Radio nationality (Country code of 2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2)
        :param min_value: Total audience (min value)
        :param max_value: Total audience (max value)
        :param min_change: Change percentage audience (min value)
        :param max_change: Change percentage audience (max value)
        :param token: Page token
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/top-song/{platform}/{metric_type}"

        params = {
            "sortBy": sort_by,
            "period": period,
            "songCountryCode": radio_country_code,
            "minValue": min_value,
            "maxValue": max_value,
            "minChange": min_change,
            "maxChange": max_change,
            "token": token,
        }

        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_song_chart_list_by_platform(
        platform, country_code=None, offset=0, limit=100
    ):
        """
        Get a listing of available song charts for a specific platform (and a specific country).

        :param platform: A song chart platform code.
        :param country_code: Optional country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2).
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/chart/song/by-platform/{platform}"
        params = {"countryCode": country_code, "offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_song_ranking_latest(chart_slug, offset=0, limit=100):
        """
        Get the latest song ranking for a specific chart.

        :param chart_slug: A song chart slug.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.14/chart/song/{chart_slug}/ranking/latest"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_song_ranking_dates(chart_slug, offset=0, limit=100):
        """
        Get the available song chart ranking dates.

        :param chart_slug: A song chart slug.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/chart/song/{chart_slug}/available-rankings"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_song_ranking_for_a_date(chart_slug, datetime, offset=0, limit=100):
        """
        Get the ranking for a song chart on a specific date.

        :param chart_slug: A song chart slug.
        :param datetime: A ranking date (ATOM format)
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.14/chart/song/{chart_slug}/ranking/{datetime}"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_album_chart_list_by_platform(
        platform, country_code=None, offset=0, limit=100
    ):
        """
        Get a listing of available album charts for a specific platform (and a specific country).

        :param platform: An album chart platform code.
        :param country_code: Optional country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2).
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/chart/album/by-platform/{platform}"
        params = {"countryCode": country_code, "offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_album_ranking_latest(chart_slug, offset=0, limit=100):
        """
        Get the latest album ranking for a specific chart.

        :param chart_slug: An album chart slug.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.26/chart/album/{chart_slug}/ranking/latest"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_album_ranking_dates(chart_slug, offset=0, limit=100):
        """
        Get the available album chart ranking dates.

        :param chart_slug: An album chart slug.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/chart/album/{chart_slug}/available-rankings"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_album_ranking_for_a_date(chart_slug, datetime, offset=0, limit=100):
        """
        Get the ranking for an album chart on a specific date.

        :param chart_slug: An album chart slug.
        :param datetime: A ranking date (ATOM format)
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.26/chart/album/{chart_slug}/ranking/{datetime}"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_tiktok_music_links_ranking_latest(offset=0, limit=100):
        """
        Get the latest ranking of trending TikTok music links. This endpoint is restricted to specific plans.

        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/chart/tiktok/music/weekly/ranking/latest"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_tiktok_music_links_ranking_dates(offset=0, limit=100):
        """
        Get the available TikTok music links chart ranking dates. This endpoint is restricted to specific plans.

        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/chart/tiktok/music/weekly/available-rankings"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_tiktok_music_links_ranking_for_a_date(datetime, offset=0, limit=100):
        """
        Get the ranking of trending TikTok music links for a specific date. This endpoint is restricted to specific plans.

        :param datetime: A ranking date (ATOM format)
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/chart/tiktok/music/weekly/ranking/{datetime}"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}
