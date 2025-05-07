from .api_util import request_wrapper, request_looper


class Deprecated:
    @staticmethod
    def get_artist_ranking(
        platform="spotify",
        metric_type="followers",
        country_code=None,
        city_key=None,
        sort_by="total",
        period="month",
        artist_country_code=None,
        min_value=None,
        max_value=None,
        min_change=None,
        max_change=None,
        token=None,
    ):
        """
        WARNING: This endpoint is now deprecated and will soon be removed for good.
        Get a listing of artists, ranked by a specific platform metric. Can possibly be filtered by country or city of the audience, with different platforms and metric types.

        :param platform: A platform code. Default: spotify.
        :param metric_type: followers, monthly_listeners, listerners, views, fans, likes, favorites, subscribers, plays, popularity. Default: followers.
        :param country_code: Optional country code for local artist audience (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2)
        :param city_key: Optional city key for local artist audience (cf referential)
        :param sort_by: total, change, percent. Default: total.
        :param period: week (global audience only), month, quarter. Default: month.
        :param artist_country_code: Optional artist nationality (Country code of 2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2)
        :param min_value: Total audience (min value)
        :param max_value: Total audience (max value)
        :param min_change: Change percentage audience (min value)
        :param max_change: Change percentage audience (max value)
        :param token: Page token
        :return: JSON response or an empty dictionary.
        """

        print(
            "WARNING: The endpoint 'Get Artist Ranking' is now deprecated. Check out the new 'Get Artists' endpoint here: https://doc.api.soundcharts.com/api/v2/doc/reference/path/artist/get-artists/"
        )
        endpoint = f"/api/v2/top-artist/{platform}/{metric_type}"

        if country_code != None:
            endpoint = (
                f"/api/v2/top-artist/country/{country_code}/{platform}/{metric_type}"
            )

        if city_key != None:
            endpoint = f"/api/v2/top-artist/city/{city_key}/{platform}/{metric_type}"

        params = {
            "sortBy": sort_by,
            "period": period,
            "artistCountryCode": artist_country_code,
            "minValue": min_value,
            "maxValue": max_value,
            "minChange": min_change,
            "maxChange": max_change,
            "token": token,
        }

        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_songs_ranking(
        platform="spotify",
        metric_type="streams",
        sort_by="total",
        period="month",
        song_country_code=None,
        min_value=None,
        max_value=None,
        min_change=None,
        max_change=None,
        token=None,
        limit=100,
    ):
        """
        WARNING: This endpoint is now deprecated and will soon be removed for good.
        Get a listing of songs, ranked by a specific platform metric

        :param platform: A platform code. Default: spotify.
        :param metric_type: streams, views, videos created, favorites, popularity, plays, likes, count. Default: streams.
        :param sort_by: total, change, percent. Default: total.
        :param period: week, month, quarter. Default: month.
        :param song_country_code: Optiona song nationality (Country code of 2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2)
        :param min_value: Total audience (min value)
        :param max_value: Total audience (max value)
        :param min_change: Change percentage audience (min value)
        :param max_change: Change percentage audience (max value)
        :param token: Page token
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        print(
            "WARNING: The endpoint 'Get Songs Ranking' is now deprecated. Check out the new 'Get Songs' endpoint here: https://doc.api.soundcharts.com/api/v2/doc/reference/path/song/get-songs/"
        )
        endpoint = f"/api/v2/top-song/{platform}/{metric_type}"

        params = {
            "sortBy": sort_by,
            "period": period,
            "songCountryCode": song_country_code,
            "minValue": min_value,
            "maxValue": max_value,
            "minChange": min_change,
            "maxChange": max_change,
            "token": token,
            "limit": limit,
        }

        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_songkick_events(
        artist_uuid,
        event_type="all",
        period_type="all",
        offset=0,
        limit=100,
        sort_by="date",
        sort_order="desc",
    ):
        """
        WARNING: This endpoint is now deprecated and will soon be removed for good.
        Get future and past event details, venue, capacity, and ticket price.

        :param artist_uuid: An artist UUID.
        :param event_type: An event type (Available values are : all, concert, festival).
        :param period_type: A period type (Available values are : all, past, upcoming).
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : date.
        :param sort_order: Sort order. Available values are : asc, desc. Default: desc.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.19/artist/{artist_uuid}/songkick/events"
        params = {
            "type": event_type,
            "periodType": period_type,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}
