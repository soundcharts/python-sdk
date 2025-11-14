from .api_util import request_wrapper, request_looper, sort_items_by_date


class Song:
    @staticmethod
    def get_songs(offset=0, limit=100, body=None, print_progress=False):
        """
        You can sort songs in our database using specific parameters such as platform, metric type, or time period, and filter them based on attributes like artist nationality, ISRC country, song genre, release date, attributes from lyrics analysis, etc. or performance metrics.
        Available platfom/metricType combinations can be found in the documentation: https://developers.soundcharts.com/documentation/reference/song/get-songs

        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit (warning: can take thousands of calls - you may want to use parallel processing). Default: 100.
        :param body: JSON Payload. If none, the default sorting will apply (descending spotify streams) and there will be no filters.
        :param print_progress: Prints an estimated progress percentage (default: False).
        :return: JSON response or an empty dictionary.
        """

        if body == None:
            body = {
                "sort": {
                    "platform": "spotify",
                    "metricType": "streams",
                    "period": "month",
                    "sortBy": "total",
                    "order": "desc",
                },
                "filters": [],
            }

        endpoint = f"/api/v2/top/songs"
        params = {
            "offset": offset,
            "limit": limit,
        }

        result = request_looper(endpoint, params, body, print_progress=print_progress)
        return result if result is not None else {}

    @staticmethod
    def get_song_metadata(song_uuid):
        """
        Get song metadata/ISRC using their UUID.

        :param song_uuid: A song UUID.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.25/song/{song_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_song_by_isrc(isrc):
        """
        Get Soundcharts’ UUID & the song's metadata.

        :param isrc: An ISRC code.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.25/song/by-isrc/{isrc}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_song_by_platform_id(platform, identifier):
        """
        Get Soundcharts’ UUID & the song's metadata.

        :param platform: A platform code.
        :param identifier: A song platform identifier.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.25/song/by-platform/{platform}/{identifier}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_lyrics_analysis(song_uuid):
        """
        Access detailed insights from song lyrics.

        :param song_uuid: A song UUID.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/song/{song_uuid}/lyrics-analysis"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_ids(song_uuid, platform=None, only_default=False, offset=0, limit=100):
        """
        Get platform URLs/ISNI associated with a specific song.

        :param song_uuid: A song UUID.
        :param platform: A platform code.
        :param only_default: Only return default identifiers. Default: False.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {
            "platform": platform,
            "onlyDefault": only_default,
            "offset": offset,
            "limit": limit,
        }

        endpoint = f"/api/v2/song/{song_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_albums(
        song_uuid,
        album_type="all",
        offset=0,
        limit=100,
        sort_by="title",
        sort_order="asc",
    ):
        """
        Get a list of albums containing a specific song.

        :param song_uuid: A song UUID.
        :param album_type: Filter result album list. Available values are : all, album, single, compil. Default: all.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : title, releaseDate. Default: "title".
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/song/{song_uuid}/albums"
        params = {
            "type": album_type,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_audience(
        song_uuid, platform="spotify", start_date=None, end_date=None, identifier=None
    ):
        """
        Get the value of streams/plays/favorites/views for a specific song.

        :param song_uuid: A song UUID.
        :param platform: A social platform code. Default: spotify.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param identifier: Optional song identifier.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/song/{song_uuid}/audience/{platform}"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "identifier": identifier,
        }
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result, True)

    @staticmethod
    def get_popularity(song_uuid, platform="spotify", start_date=None, end_date=None):
        """
        Song popularity metric indicates how popular a song is on a specific platform. It is calculated by the platform.

        :param song_uuid: A song UUID.
        :param platform: A social platform code. Available values : spotify, deezer, tidal. Default: spotify.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/song/{song_uuid}/popularity/{platform}"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result, True)

    @staticmethod
    def get_chart_entries(
        song_uuid,
        platform="spotify",
        current_only=1,
        offset=0,
        limit=100,
        sort_by="position",
        sort_order="asc",
    ):
        """
        Get current/past chart entries for a specific song.

        :param song_uuid: A song UUID.
        :param platform: An Artist Chart platform code. Default: spotify.
        :param current_only: Get only the current positions in charts with 1, or the current and past positions with 0. Default: 1.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : position, rankDate. Default: position.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/song/{song_uuid}/charts/ranks/{platform}"
        params = {
            "currentOnly": current_only,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_playlist_entries(
        song_uuid,
        platform="spotify",
        playlist_type="all",
        current_only=False,
        country_code=None,
        playlist_uuids=[],
        offset=0,
        limit=100,
        sort_by="entryDate",
        sort_order="desc",
    ):
        """
        Get current playlist entries for a specific song.

        :param song_uuid: A song UUID.
        :param platform: A playlist platform code. Default: spotify.
        :param playlist_type: A playlist type. Available values are : 'all' or one of editorial, algorithmic, algotorial, major, charts, curators_listeners, radios, this_is.
        :param current_only: Get only the current positions in playlist (True), or the current and past positions (False). Default : False.
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2).
        :param playlist_uuids: A list of playlist UUIDs.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : position, positionDate, entryDate, subscriberCount.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/song/{song_uuid}/playlist/current/{platform}"
        params = {
            "type": playlist_type,
            "currentOnly": current_only,
            "countryCode": country_code,
            "playlistUuids": playlist_uuids,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_playlist_reach(
        song_uuid,
        platform="spotify",
        playlist_type="all",
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
    ):
        """
        Get playlist reach & count for a specific song.

        :param song_uuid: A song UUID.
        :param platform: A playlist platform code. Default: spotify. Available platforms are listed in the Get platforms for playlist data endpoint. While the playlist count is available for all of these, playlist reach is only available for spotify, youtube, deezer, jiosaavn and boomplay.
        :param playlist_type: A playlist type. Available values are : 'all' or one of editorial, algorithmic, user.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/song/{song_uuid}/playlist/reach/{platform}"

        params = {
            "type": playlist_type,
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_radio_spins(
        song_uuid,
        radio_slugs=None,
        country_code=None,
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
    ):
        """
        Get radio spins for all tracks of a specific song.

        :param song_uuid: A song UUID.
        :param radio_slugs: Optional radio slugs filter (comma separated).
        :param country_code: Optional country code filter (2 letters ISO 3166-2, full list on https://en.wikipedia.org/wiki/ISO_3166-2).
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/song/{song_uuid}/broadcasts"
        params = {
            "radioSlugs": radio_slugs,
            "countryCode": country_code,
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result, key="airedAt")

    @staticmethod
    def get_radio_spin_count(
        song_uuid,
        radio_slugs=None,
        country_code=None,
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
    ):
        """
        Get radio spins for all tracks of a specific song.

        :param song_uuid: A song UUID.
        :param radio_slugs: Optional radio slugs filter (comma separated).
        :param country_code: Optional country code filter (2 letters ISO 3166-2, full list on https://en.wikipedia.org/wiki/ISO_3166-2).
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/song/{song_uuid}/broadcast-groups"
        params = {
            "radioSlugs": radio_slugs,
            "countryCode": country_code,
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def add_links(song_uuid, links):
        """
        Add/submit missing links to song profiles.

        :param song_uuid: A song UUID.
        :param links: A list of links.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/song/{song_uuid}/sources/add"

        body = {"urls": links}

        result = request_wrapper(endpoint, body=body)
        return result if result is not None else {}
