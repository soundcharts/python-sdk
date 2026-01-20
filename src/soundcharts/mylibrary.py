from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
)
import json


class MyLibrary:

    @staticmethod
    def get_artist_list(offset=0, limit=100):
        """
        Get all artists in your personal library.

        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/library/artist"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def add_artists_ids(identifiers):
        """
        Add artists to your personal library. This endpoint is restricted to specific plans.

        :param identifiers: A list of dicts structured like :
            [{
                "identifier": "9635624",
                "platformCode": "deezer"
            },
            ...
            ]
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/library/artist"

        body = json.dumps({"identifiers": identifiers})

        result = request_wrapper(endpoint, body=body)
        return result if result is not None else {}

    @staticmethod
    def delete_artists_ids(identifiers):
        """
        Add artists to your personal library. This endpoint is restricted to specific plans.

        :param identifiers: A list of dicts structured like :
            [{
                "identifier": "9635624",
                "platformCode": "deezer"
            },
            ...
            ]
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/library/artist"

        body = json.dumps({"identifiers": identifiers})

        result = request_wrapper(endpoint, body=body, method="delete")
        return result if result is not None else {}

    @staticmethod
    def get_song_list(offset=0, limit=100):
        """
        Get all songs in your personal library.

        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/library/song"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def add_songs_ids(identifiers):
        """
        Add songs to your personal library. This endpoint is restricted to specific plans.

        :param identifiers: A list of dicts structured like :
            [{
                "identifier": "9635624",
                "platformCode": "deezer"
            },
            ...
            ]
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/library/song"

        body = json.dumps({"identifiers": identifiers})

        result = request_wrapper(endpoint, body=body)
        return result if result is not None else {}

    @staticmethod
    def delete_songs_ids(identifiers):
        """
        Add songs to your personal library. This endpoint is restricted to specific plans.

        :param identifiers: A list of dicts structured like :
            [{
                "identifier": "1577594494",
                "platformCode": "apple-music"
            },
            ...
            ]
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/library/song"

        body = json.dumps({"identifiers": identifiers})

        result = request_wrapper(endpoint, body=body, method="delete")
        return result if result is not None else {}


class MyLibraryAsync:

    @staticmethod
    async def get_artist_list(offset=0, limit=100):
        """
        Get all artists in your personal library.

        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/library/artist"
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def add_artists_ids(identifiers):
        """
        Add artists to your personal library. This endpoint is restricted to specific plans.

        :param identifiers: A list of dicts structured like :
            [{
                "identifier": "9635624",
                "platformCode": "deezer"
            },
            ...
            ]
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/library/artist"

        body = json.dumps({"identifiers": identifiers})

        result = await request_wrapper_async(endpoint, body=body)
        return result if result is not None else {}

    @staticmethod
    async def delete_artists_ids(identifiers):
        """
        Add artists to your personal library. This endpoint is restricted to specific plans.

        :param identifiers: A list of dicts structured like :
            [{
                "identifier": "9635624",
                "platformCode": "deezer"
            },
            ...
            ]
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/library/artist"

        body = json.dumps({"identifiers": identifiers})

        result = await request_wrapper_async(endpoint, body=body, method="delete")
        return result if result is not None else {}

    @staticmethod
    async def get_song_list(offset=0, limit=100):
        """
        Get all songs in your personal library.

        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/library/song"
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def add_songs_ids(identifiers):
        """
        Add songs to your personal library. This endpoint is restricted to specific plans.

        :param identifiers: A list of dicts structured like :
            [{
                "identifier": "9635624",
                "platformCode": "deezer"
            },
            ...
            ]
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/library/song"

        body = json.dumps({"identifiers": identifiers})

        result = await request_wrapper_async(endpoint, body=body)
        return result if result is not None else {}

    @staticmethod
    async def delete_songs_ids(identifiers):
        """
        Add songs to your personal library. This endpoint is restricted to specific plans.

        :param identifiers: A list of dicts structured like :
            [{
                "identifier": "1577594494",
                "platformCode": "apple-music"
            },
            ...
            ]
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/library/song"

        body = json.dumps({"identifiers": identifiers})

        result = await request_wrapper_async(endpoint, body=body, method="delete")
        return result if result is not None else {}
