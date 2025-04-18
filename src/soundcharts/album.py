from .api_util import request_wrapper, request_looper


class Album:
    @staticmethod
    def get_album_metadata(album_uuid):
        """
        Get an album's metadata using their UUID.

        :param album_uuid: An album UUID.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.36/album/by-uuid/{album_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_album_by_upc(upc):
        """
        Get Soundcharts’ UUID & the album's metadata.

        :param upc: An UPC code.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.36/album/by-upc/{upc}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_album_by_platform_id(platform, identifier):
        """
        Get Soundcharts’ UUID & the album's metadata.

        :param platform: A platform code.
        :param identifier: An album platform identifier.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.36/album/by-platform/{platform}/{identifier}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_ids(album_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs/ISNI associated with a specific album.

        :param album_uuid: An album UUID.
        :param platform: A platform code. Default: None.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2.26/album/{album_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_tracklisting(album_uuid):
        """
        Get an album's tracklisting using their UUID.

        :param album_uuid: An album UUID.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.36/album/{album_uuid}/tracks"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_chart_entries(
        album_uuid,
        platform="spotify",
        current_only=1,
        offset=0,
        limit=100,
        sort_by="position",
        sort_order="asc",
    ):
        """
        Get current/past chart entries for a specific album.

        :param album_uuid: An album UUID.
        :param platform: An Artist Chart platform code. Default: spotify.
        :param current_only: Get only the current positions in charts with 1, or the current and past positions with 0. Default: 1.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : position, rankDate. Default: position.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.26/album/{album_uuid}/charts/ranks/{platform}"
        params = {
            "currentOnly": current_only,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}
