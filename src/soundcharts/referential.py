from .api_util import request_wrapper, request_looper


class Referential:

    @staticmethod
    def get_platforms():
        """
        Get all available platforms on Soundcharts.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/platforms"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_audience_data():
        """
        Get all platforms for which Soundcharts gets audience data for artists.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/platforms/social"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_streaming_data():
        """
        Get all platforms for which Soundcharts gets streaming data for artists.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/platforms/streaming"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_song_charts():
        """
        Get a listing of platforms for which Soundcharts stores song charts.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/chart/song/platforms"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_album_charts():
        """
        Get a listing of platforms for which Soundcharts stores album charts.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/chart/album/platforms"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_playlist_data():
        """
        Get all platforms for which Soundcharts tracks playlists.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/playlist/platforms"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_radio_country_list(offset=0, limit=100):
        """
        Get the listing of countries where Soundcharts tracks at least 1 radio station.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/radio/countries"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_artist_genres(genre="all", sort_order="asc"):
        """
        Get all artist genres and the associated subgenres.
        :param genre: Select a specific parent genre. Default: all.
        :param sort_order: Sort order. Available values are : asc, desc.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/artist/genres"
        params = {"genre": genre, "sortOrder": sort_order}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_cities_for_artist_ranking(
        country_code, search_city=None, offset=0, limit=100
    ):
        """
        For a specific country, get a listing of cities you can use to get an artist ranking.
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2).
        :param search_city: Optional: search city filter.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/top-artist/referential/cities/{country_code}"
        params = {"searchCity": search_city, "offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}
