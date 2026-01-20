from .api_util import request_wrapper, request_looper, sort_items_by_date


class Publisher:

    @staticmethod
    def get_publisher_metadata(publisher_uuid):
        """
        Retrieve detailed profile information and contact metadata for a specific music publisher.

        :param publisher_uuid: A publisher uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/publisher/{publisher_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_publisher_by_ipi(ipi):
        """
        Retrieve detailed profile information and contact metadata for a specific music publisher.

        :param ipi: A Publisher platform identifier.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/publisher/by-ipi/{ipi}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_publisher_by_platform_id(platform, identifier):
        """
        Retrieve detailed profile information and contact metadata for a specific music publisher.

        :param platform: A platform code.
        :param identifier: A Publisher platform Identifier.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/publisher/by-platform/{platform}/{identifier}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_ids(publisher_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this publisher.

        :param publisher_uuid: A publisher uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/publisher/{publisher_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}
