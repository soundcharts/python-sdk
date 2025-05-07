from .api_util import request_wrapper, request_looper, sort_items_by_date
from datetime import datetime


class Artist:

    @staticmethod
    def get_artists(
        country_code=None,
        city_key=None,
        offset=0,
        limit=100,
        body=None,
        print_progress=False,
    ):
        """
        You can sort artists in our database using specific parameters such as platform, metric type, or time period, and filter them based on attributes like nationality, genre, sub-genre, career stage, etc. or performance metrics.
        Platforms and metrics depend on the data scope: global, country, or city. For example, Spotify monthly listeners are available globally and by city but not by country.
        You'll find available platfom/metricType combinations in the documentation: https://doc.api.soundcharts.com/api/v2/doc/reference/path/artist/get-artists

        :param country_code: Add a country to get artists ranked by their stats in that specific country. Avalaible values: country code of 2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2. Leave empty to get the artists list based on their global stats.
        :param city_key: Add a cityKey and a countryCode to get artists ranked by their stats in that specific city. Available values are listed in the https://doc.api.soundcharts.com/api/v2/doc/reference/path/referential/get-cities-for-artist-ranking endpoint.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit (warning: can take up to 100,000 calls - you may want to use parallel processing). Default: 100.
        :param body: JSON Payload. If none, the default sorting will apply (spotify followers for global ranking, instagram followers for country ranking, spotify monthly listeners for city ranking) and there will be no filters.
        :param print_progress: Prints an estimated progress percentage (default: False).
        :return: JSON response or an empty dictionary.
        """

        if body == None:
            platform, metric_type = "spotify", "followers"
            if country_code:
                platform = "instagram"
            if city_key:
                platform, metric_type = "spotify", "monthly_listeners"

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

        endpoint = f"/api/v2/top/artists"
        params = {
            "countryCode": country_code,
            "cityKey": city_key,
            "offset": offset,
            "limit": limit,
        }

        result = request_looper(endpoint, params, body, print_progress=print_progress)
        return result if result is not None else {}

    @staticmethod
    def get_artist_metadata(artist_uuid):
        """
        Get artist metadata/ISNI/IPI numbers using their UUID.

        :param artist_uuid: An artist UUID.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.9/artist/{artist_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_artist_by_platform_id(platform, identifier):
        """
        Get Soundcharts' UUID and artist metadata based on platform IDs.

        :param platform: A platform code.
        :param identifier: An artist platform identifier.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.9/artist/by-platform/{platform}/{identifier}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_ids(artist_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs/ISNI associated with a specific artist.

        :param artist_uuid: An artist UUID.
        :param platform: A platform code. Default: None.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/artist/{artist_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_songs(artist_uuid, offset=0, limit=100, sort_by="name", sort_order="asc"):
        """
        Get songs by a specific artist, including tracks in which the artist is featured.

        :param artist_uuid: An artist UUID.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : name, releaseDate, spotifyStream, shazamCount, youtubeViews, spotifyPopularity. Default: name
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.21/artist/{artist_uuid}/songs"
        params = {
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_albums(
        artist_uuid,
        album_type="all",
        offset=0,
        limit=100,
        sort_by="title",
        sort_order="asc",
    ):
        """
        Get a list of albums featuring a specific artist.

        :param artist_uuid: An artist UUID.
        :param album_type: Filter result album list. Available values are : all, album, single, compil. Default: all.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : title, releaseDate. Default: "title".
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.21/artist/{artist_uuid}/albums"
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
    def get_similar_artists(artist_uuid, offset=0, limit=20):
        """
        Get similar artists ("Fans Also Like") from Spotify.

        :param artist_uuid: An artist UUID.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/artist/{artist_uuid}/related"
        params = {"offset": offset, "limit": min(limit, 20)}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_current_stats(artist_uuid, period=7):
        """
        Get all the current audience, streaming, popularity, and retention stats for an artist.

        :param artist_uuid: An artist UUID.
        :param period: Period of the evolution. Default: 7.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/artist/{artist_uuid}/current/stats"
        params = {"period": period}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_soundcharts_score(artist_uuid, start_date=None, end_date=None):
        """
        This API returns 3 Soundcharts scores per artist: score, fanbase score and trending score.

        :param artist_uuid: An artist UUID.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/artist/{artist_uuid}/soundcharts/score"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_audience(artist_uuid, platform="spotify", start_date=None, end_date=None):
        """
        Get an artist's followers across services.

        :param artist_uuid: An artist UUID.
        :param platform: A social platform code. Default: spotify.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/artist/{artist_uuid}/audience/{platform}"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result)

    @staticmethod
    def get_local_audience(
        artist_uuid, platform="instagram", start_date=None, end_date=None
    ):
        """
        Get all values for artist followers for a month and located followers for a given date within that month.

        :param artist_uuid: An artist UUID.
        :param platform: A social platform code. Available platforms for located followers: instagram, tiktok & youtube. Default: instagram.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.37/artist/{artist_uuid}/social/{platform}/followers/"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result)

    @staticmethod
    def get_streaming_audience(
        artist_uuid, platform="spotify", start_date=None, end_date=None
    ):
        """
        Get the value for listeners/streams/views per artist.

        :param artist_uuid: An artist UUID.
        :param platform: A streaming platform code. Default: spotify.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/{artist_uuid}/streaming/{platform}/listening"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result)

    @staticmethod
    def get_local_streaming_audience(
        artist_uuid, platform="spotify", start_date=None, end_date=None
    ):
        """
        Get daily values for Spotify monthly listeners and YouTube views per artist.

        :param artist_uuid: An artist UUID.
        :param platform: A streaming platform code. Default: spotify.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/{artist_uuid}/streaming/{platform}"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result)

    @staticmethod
    def get_retention(artist_uuid, platform="spotify", start_date=None, end_date=None):
        """
        Get an artist's fan retention rate across platforms.

        :param artist_uuid: An artist UUID.
        :param platform: A streaming platform code. Available values: spotify, youtube, anghami, jiosaavn. Default: spotify.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/{artist_uuid}/{platform}/retention"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result)

    @staticmethod
    def get_popularity(artist_uuid, platform="spotify", start_date=None, end_date=None):
        """
        Get daily values for artist popularity (spotify and tidal).

        :param artist_uuid: An artist UUID.
        :param platform: A streaming platform code. Available values: spotify, tidal. Default: spotify.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/{artist_uuid}/popularity/{platform}"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result)

    @staticmethod
    def get_audience_report_latest(artist_uuid, platform):
        """
        Get the latest demographics reports for social/streaming platforms.

        :param artist_uuid: An artist UUID.
        :param platform: A streaming platform code. Available values: instagram, youtube, tiktok. Default: instagram.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/{artist_uuid}/audience/{platform}/report/latest"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_audience_report_dates(
        artist_uuid, platform, start_date=None, end_date=None, offset=0, limit=100
    ):
        """
        Get the latest demographics reports for social/streaming platforms.

        :param artist_uuid: An artist UUID.
        :param platform: A streaming platform code. Available values: instagram, youtube, tiktok.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = (
            f"/api/v2/artist/{artist_uuid}/audience/{platform}/report/available-dates"
        )
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result, True)

    @staticmethod
    def get_audience_report_for_a_date(artist_uuid, platform, date):
        """
        Get the demographics reports for social/streaming platforms for a specific date.

        :param artist_uuid: An artist UUID.
        :param platform: A streaming platform code. Available values: instagram, youtube, tiktok.
        :param date: A report date (YYYY-MM-DD)
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/{artist_uuid}/audience/{platform}/report/{date}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_short_videos(artist_uuid, platform="instagram", offset=0, limit=100):
        """
        Get an artist’s short videos, and the current audience of each video (comments/likes/views).

        :param artist_uuid: An artist UUID.
        :param platform: A streaming platform code. Available values: instagram, youtube. Default: instagram.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/{artist_uuid}/shorts/{platform}/videos"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_short_video_audience(identifier, start_date=None, end_date=None):
        """
        Get artist metadata/ISNI/IPI numbers using their UUID.

        :param identifier: A short/reel video identifier.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/shorts/{identifier}/audience"
        params = {"startDate": start_date, "endDate": end_date}
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result, True)

    @staticmethod
    def get_chart_song_entries(
        artist_uuid,
        platform="spotify",
        current_only=1,
        offset=0,
        limit=100,
        sort_by="position",
        sort_order="asc",
    ):
        """
        Get current/past song chart entries for a specific artist.

        :param artist_uuid: An artist UUID.
        :param platform: An Artist Chart platform code. Default: spotify.
        :param current_only: Get only the current positions in charts with 1, or the current and past positions with 0. Default: 1.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : position, rankDate. Default: position.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/{artist_uuid}/charts/song/ranks/{platform}"
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
    def get_chart_album_entries(
        artist_uuid,
        platform="spotify",
        current_only=1,
        offset=0,
        limit=100,
        sort_by="position",
        sort_order="asc",
    ):
        """
        Get current/past album chart entries for a specific artist.

        :param artist_uuid: An artist UUID.
        :param platform: An Artist Chart album platform code. Default: spotify.
        :param current_only: Get only the current positions in charts with 1, or the current and past positions with 0. Default: 1.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : position, rankDate. Default: position.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.28/artist/{artist_uuid}/charts/album/ranks/{platform}"
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
        artist_uuid,
        platform="spotify",
        playlist_type="all",
        offset=0,
        limit=100,
        sort_by="entryDate",
        sort_order="desc",
    ):
        """
        Get current playlist entries for a specific artist.

        :param artist_uuid: An artist UUID.
        :param platform: A playlist platform code. Default: spotify.
        :param playlist_type: A playlist type. Available values are : 'all' or one of editorial, algorithmic, algotorial, major, charts, curators_listeners, radios, this_is.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : position, positionDate, entryDate, subscriberCount.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/artist/{artist_uuid}/playlist/current/{platform}"
        params = {
            "type": playlist_type,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_radio_spins(
        artist_uuid,
        radio_slugs=None,
        country_code=None,
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
    ):
        """
        Get radio spins for all tracks of a specific artist.

        :param artist_uuid: An artist UUID.
        :param radio_slugs: Optional radio slugs filter (comma separated).
        :param country_code: Optional country code filter (2 letters ISO 3166-2, full list on https://en.wikipedia.org/wiki/ISO_3166-2).
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/artist/{artist_uuid}/broadcasts"
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
    def get_radio_spin_count(
        artist_uuid,
        radio_slugs=None,
        country_code=None,
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
    ):
        """
        Get radio spins for all tracks of a specific artist.

        :param artist_uuid: An artist UUID.
        :param radio_slugs: Optional radio slugs filter (comma separated).
        :param country_code: Optional country code filter (2 letters ISO 3166-2, full list on https://en.wikipedia.org/wiki/ISO_3166-2).
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty to use latest 90 days.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/artist/{artist_uuid}/broadcast-groups"
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
    def get_events(
        artist_uuid,
        event_type="all",
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
        sort_by="date",
        sort_order="asc",
    ):
        """
        Get future and past event details, venue, capacity, and ticket price.

        :param artist_uuid: An artist UUID.
        :param event_type: An event type (Available values are : all, concert, festival, online).
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD).
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : date.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.19/artist/{artist_uuid}/songkick/events"
        params = {
            "type": event_type,
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params, handle_period=False)
        return result if result is not None else {}

    @staticmethod
    def add_links(artist_uuid, links):
        """
        Add/submit missing links to artist profiles.

        :param artist_uuid: An artist UUID.
        :param links: A list of links.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/artist/{artist_uuid}/sources/add"

        body = {"urls": links}

        result = request_wrapper(endpoint, body=body)
        return result if result is not None else {}
