from .api_util import request_wrapper


def search_by_type(search_type, term, offset=0, limit=20):
    """
    Generic search function for different types of entities.

    :param search_type: Type of entity to search (e.g., 'artist', 'song', 'playlist', 'radio').
    :param term: Search term.
    :param offset: Pagination offset. Default: 0.
    :param limit: Number of results to retrieve (max 20).
    :return: JSON response or an empty dictionary.
    """
    params = {"offset": offset, "limit": min(limit, 20)}
    endpoint = f"/api/v2/{search_type}/search/{term}"
    result = request_wrapper(endpoint, params)
    return result if result is not None else {}


class Search:

    # Specific search functions
    @staticmethod
    def search_artist_by_name(term, offset=0, limit=20):
        return search_by_type("artist", term, offset, limit)

    @staticmethod
    def search_song_by_name(term, offset=0, limit=20):
        return search_by_type("song", term, offset, limit)

    @staticmethod
    def search_playlist_by_name(term, offset=0, limit=20):
        return search_by_type("playlist", term, offset, limit)

    @staticmethod
    def search_radio_by_name(term, offset=0, limit=20):
        return search_by_type("radio", term, offset, limit)

    @staticmethod
    def search_festival_by_name(term, offset=0, limit=20):
        return search_by_type("festival", term, offset, limit)

    @staticmethod
    def search_venue_by_name(term, offset=0, limit=20):
        return search_by_type("venue", term, offset, limit)
    
    @staticmethod
    def get_soundcharts_url_from_platform_url(platform_url):
        """
        This endpoint returns the Soundcharts URL and the type (artist, song, playlist).
        Available platforms for songs/artists are listed in the Get all platforms endpoint.
        Available platforms for playlists are listed in the Get platforms for playlist data endpoint.
        :param platform_url: A platform URL.
        :return: JSON response or an empty dictionary.
        """
        endpoint = "/api/v2/search/external/url"
        params = {"platformUrl": platform_url}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}
