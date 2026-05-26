from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
)


class Favorite:

    @staticmethod
    def get_favorite_artists(offset=0, limit=20):
        """
        Retrieve the artists configured for high-frequency data updates.

        :param offset: Pagination offset.  Default: 0.
        :param limit: Number of results to retrieve.  None: no limit.  Default: 20.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/favorite/artists"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def add_artist_to_favorites(artist_uuid):
        """
        Flag an artist to accelerate their audience data refresh rate.

        :param artist_uuid: An artist UUID.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/favorite/artist/{artist_uuid}"
        result = request_wrapper(endpoint, method="POST")
        return result if result is not None else {}

    @staticmethod
    def remove_artist_from_favorites(artist_uuid):
        """
        Revert an artist to the standard audience data refresh rate.

        :param artist_uuid: An artist UUID.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/favorite/artist/{artist_uuid}"

        result = request_wrapper(endpoint, method="DELETE")
        return result if result is not None else {}


class FavoriteAsync:

    @staticmethod
    async def get_favorite_artists(offset=0, limit=20):
        """
        Retrieve the artists configured for high-frequency data updates.

        :param offset: Pagination offset.  Default: 0.
        :param limit: Number of results to retrieve.  None: no limit.  Default: 20.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/favorite/artists"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def add_artist_to_favorites(artist_uuid):
        """
        Flag an artist to accelerate their audience data refresh rate.

        :param artist_uuid: An artist UUID.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/favorite/artist/{artist_uuid}"
        result = await request_wrapper_async(endpoint, method="POST")
        return result if result is not None else {}

    @staticmethod
    async def remove_artist_from_favorites(artist_uuid):
        """
        Revert an artist to the standard audience data refresh rate.

        :param artist_uuid: An artist UUID.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/favorite/artist/{artist_uuid}"

        result = await request_wrapper_async(endpoint, method="DELETE")
        return result if result is not None else {}
