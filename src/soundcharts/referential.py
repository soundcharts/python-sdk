from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
)


class Referential:

    @staticmethod
    def get_platforms(offset=0, limit=100):
        """
        Get all available platforms on Soundcharts.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/platforms"
        params = {"offset": offset, "limit": limit}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_audience_data(offset=0, limit=100):
        """
        Get all platforms for which Soundcharts gets audience data for artists.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/platforms/social"
        params = {"offset": offset, "limit": limit}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_streaming_data(offset=0, limit=100):
        """
        Get all platforms for which Soundcharts gets streaming data for artists.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/platforms/streaming"
        params = {"offset": offset, "limit": limit}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_song_charts(offset=0, limit=100):
        """
        Get a listing of platforms for which Soundcharts stores song charts.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/chart/song/platforms"
        params = {"offset": offset, "limit": limit}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_album_charts(offset=0, limit=100):
        """
        Get a listing of platforms for which Soundcharts stores album charts.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/chart/album/platforms"
        params = {"offset": offset, "limit": limit}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_platforms_for_playlist_data(offset=0, limit=100):
        """
        Get all platforms for which Soundcharts tracks playlists.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/playlist/platforms"
        params = {"offset": offset, "limit": limit}
        result = request_wrapper(endpoint, params)
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

    @staticmethod
    def get_song_genres(genre="all", sort_order="asc"):
        """
        Get all song genres and the associated subgenres.
        This endpoint is useful for the Get Songs endpoint.
        :param genre: Select a specific song genre. Default: all.
        :param sort_order: Sort order. Available values are : asc, desc.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/song/genres"
        params = {"genre": genre, "sortOrder": sort_order}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_label_types(offset=0, limit=100):
        """
        Get all label types.
        This endpoint is useful for the Get Songs endpoint.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/label-types"
        params = {"offset": offset, "limit": limit}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_distributors(offset=0, limit=100):
        """
        Get all distributors.
        This endpoint is useful for the Get Songs endpoint.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/distributors"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_lyrics_attributes(attribute, term=None, offset=0, limit=100):
        """
        Get the list of available values by lyrics attribute.
        :param attribute: The type of attribute. Available values : themes, moods, culturalReferencePeople, culturalReferenceNonPeople, brands, locations.
        :param term: Search an item which contains the term. Default: None.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/lyrics-attributes"
        params = {
            "attribute": attribute,
            "term": term,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}


class ReferentialAsync:

    @staticmethod
    async def get_platforms(offset=0, limit=100):
        """
        Get all available platforms on Soundcharts.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/platforms"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_platforms_for_audience_data(offset=0, limit=100):
        """
        Get all platforms for which Soundcharts gets audience data for artists.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/platforms/social"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_platforms_for_streaming_data(offset=0, limit=100):
        """
        Get all platforms for which Soundcharts gets streaming data for artists.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/platforms/streaming"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_platforms_for_song_charts(offset=0, limit=100):
        """
        Get a listing of platforms for which Soundcharts stores song charts.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/chart/song/platforms"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_platforms_for_album_charts(offset=0, limit=100):
        """
        Get a listing of platforms for which Soundcharts stores album charts.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/chart/album/platforms"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_platforms_for_playlist_data(offset=0, limit=100):
        """
        Get all platforms for which Soundcharts tracks playlists.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/playlist/platforms"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_radio_country_list(offset=0, limit=100):
        """
        Get the listing of countries where Soundcharts tracks at least 1 radio station.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/radio/countries"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_artist_genres(genre="all", sort_order="asc"):
        """
        Get all artist genres and the associated subgenres.
        :param genre: Select a specific parent genre. Default: all.
        :param sort_order: Sort order. Available values are : asc, desc.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/artist/genres"
        params = {"genre": genre, "sortOrder": sort_order}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_cities_for_artist_ranking(
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
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_song_genres(genre="all", sort_order="asc"):
        """
        Get all song genres and the associated subgenres.
        This endpoint is useful for the Get Songs endpoint.
        :param genre: Select a specific song genre. Default: all.
        :param sort_order: Sort order. Available values are : asc, desc.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/song/genres"
        params = {"genre": genre, "sortOrder": sort_order}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_label_types(offset=0, limit=100):
        """
        Get all label types.
        This endpoint is useful for the Get Songs endpoint.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/label-types"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_distributors(offset=0, limit=100):
        """
        Get all distributors.
        This endpoint is useful for the Get Songs endpoint.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/distributors"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_lyrics_attributes(attribute, term=None, offset=0, limit=100):
        """
        Get the list of available values by lyrics attribute.
        :param attribute: The type of attribute. Available values : themes, moods, culturalReferencePeople, culturalReferenceNonPeople, brands, locations.
        :param term: Search an item which contains the term. Default: None.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/referential/lyrics-attributes"
        params = {
            "attribute": attribute,
            "term": term,
            "offset": offset,
            "limit": limit,
        }
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}
