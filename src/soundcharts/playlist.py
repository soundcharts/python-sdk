from .api_util import request_wrapper, request_looper, sort_items_by_date


class Playlist:

    @staticmethod
    def get_playlists(platform, offset=0, limit=100, body=None, print_progress=False):
        """
        You can sort playlists in our database using specific parameters such as the number of followers, 28-day adds, track count, or last updated date. Apply filters based on attributes like genre, type, country, owner, track age, percentage of adds over the last 28 days, or performance metrics.
        Please note that you can only retrieve the playlists for one platform at a time.

        :param platform: A playlist Chart platform code. Default: spotify.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit (warning: can take up to 100,000 calls - you may want to use parallel processing). Default: 100.
        :param body: JSON Payload. If none, the default sorting will apply (by metric for the platforms who have one, by 28DayAdds for others) and there will be no filters.
        :param print_progress: Prints an estimated progress percentage (default: False).
        :return: JSON response or an empty dictionary.
        """

        ref_metric_types = {
            "spotify": "likes",
            "youtube": "views",
            "deezer": "fans",
            "jiosaavn": "followers",
            "boomplay": "favorites",
        }

        if body == None:
            body = {
                "sort": {
                    "type": "28DayAdds",
                    "order": "desc",
                },
                "filters": [],
            }
            if platform in ref_metric_types:
                body = {
                    "sort": {
                        "type": "metric",
                        "platform": platform,
                        "metricType": ref_metric_types[platform],
                        "sortBy": "total",
                        "period": "month",
                        "order": "desc",
                    },
                    "filters": [],
                }

        endpoint = f"/api/v2/top/playlists/{platform}"
        params = {"offset": offset, "limit": limit}

        result = request_looper(endpoint, params, body, print_progress=print_progress)
        return result if result is not None else {}

    @staticmethod
    def get_playlist_metadata(playlist_uuid):
        """
        Get a playlist's metadata using their UUID.

        :param playlist_uuid: A playlist UUID.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.8/playlist/{playlist_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_playlist_by_platform_id(platform, identifier, country_code=None):
        """
        Get Soundcharts’ UUID & the playlist's metadata.

        :param platform: A platform code.
        :param identifier: A playlist platform identifier.
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2). Required for apple-music and amazon.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.8/playlist/by-platform/{platform}/{identifier}"
        params = {"countryCode": country_code}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_curators_by_platform(platform="spotify", offset=0, limit=100):
        """
        Get the listing of all playlist curators know by Soundcharts.

        :param platform: A playlist Chart platform code. Default: spotify.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/playlist/curators/{platform}"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_playlists_by_curator(
        platform,
        curator_identifier,
        country_code=None,
        offset=0,
        limit=100,
        sort_by="name",
        sort_order="asc",
    ):
        """
        Get the listing of all playlists made by a specific curator.

        :param platform: A playlist platform code.
        :param curator_identifier: A playlist curator identifier
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2). Required for apple-music and amazon.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : audience, name. Default: name.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/by-curator/{platform}/{curator_identifier}"
        params = {
            "countryCode": country_code,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_playlists_by_type(
        platform,
        playlist_type,
        country_code=None,
        offset=0,
        limit=100,
        sort_by="name",
        sort_order="asc",
    ):
        """
        Get the listing of all playlist with a specific type/nationality.

        :param platform: A playlist platform code.
        :param playlist_type: A playlist type (algorithmic, charts, curators_listeners, editorial, algotorial, major, radios, this_is.)
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2). Required for apple-music and amazon.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : audience, name. Default: name.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/by-type/{platform}/{playlist_type}"
        params = {
            "countryCode": country_code,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_audience(playlist_uuid, start_date=None, end_date=None):
        """
        Get the playlist’s number of followers/fans/views.

        :param playlist_uuid: A playlist UUID.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/audience"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result, True)

    @staticmethod
    def get_tracklisting_latest(playlist_uuid, offset=0, limit=100):
        """
        Get the latest playlist’s tracklisting.

        :param playlist_uuid: A playlist UUID.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/tracks/latest"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_tracklisting_dates(
        playlist_uuid, start_date=None, end_date=None, offset=0, limit=100
    ):
        """
        Get the available playlist’s tracklisting dates.

        :param playlist_uuid: A playlist UUID.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/available-tracklistings"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result, True)

    @staticmethod
    def get_tracklisting_for_a_date(playlist_uuid, datetime, offset=0, limit=100):
        """
        Get the playlist’s tracklisting for a date.

        :param playlist_uuid: A playlist UUID.
        :param datetime: A ranking date (ATOM format)
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/tracks/{datetime}"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}
