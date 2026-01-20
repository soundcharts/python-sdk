from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
)


class Work:

    @staticmethod
    def get_work_metadata(work_uuid):
        """
        Retrieve comprehensive metadata for a specific work, including its ISWC, writers, and ownership structure.

        :param work_uuid: A work uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/work/{work_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_work_by_iswc(iswc):
        """
        Retrieve comprehensive metadata for a specific work, including its ISWC, writers, and ownership structure.

        :param iswc: A Work ISWC.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/work/by-iswc/{iswc}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_work_by_platform_id(platform, identifier):
        """
        Retrieve comprehensive metadata for a specific work, including its ISWC, writers, and ownership structure.

        :param platform: A platform code.
        :param identifier: A Work platform identifier.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/work/by-platform/{platform}/{identifier}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_ids(work_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this work.

        :param work_uuid: A work uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/work/{work_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_recordings(work_uuid, offset=0, limit=100):
        """
        Retrieve a comprehensive list of all musical recordings associated with a specific work.

        :param work_uuid: A work uuid.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/work/{work_uuid}/recordings"
        result = request_looper(endpoint, params)
        return result if result is not None else {}


class WorkAsync:

    @staticmethod
    async def get_work_metadata(work_uuid):
        """
        Retrieve comprehensive metadata for a specific work, including its ISWC, writers, and ownership structure.

        :param work_uuid: A work uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/work/{work_uuid}"
        result = await request_wrapper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_work_by_iswc(iswc):
        """
        Retrieve comprehensive metadata for a specific work, including its ISWC, writers, and ownership structure.

        :param iswc: A Work ISWC.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/work/by-iswc/{iswc}"
        result = await request_wrapper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_work_by_platform_id(platform, identifier):
        """
        Retrieve comprehensive metadata for a specific work, including its ISWC, writers, and ownership structure.

        :param platform: A platform code.
        :param identifier: A Work platform identifier.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/work/by-platform/{platform}/{identifier}"
        result = await request_wrapper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_ids(work_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this work.

        :param work_uuid: A work uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/work/{work_uuid}/identifiers"
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_recordings(work_uuid, offset=0, limit=100):
        """
        Retrieve a comprehensive list of all musical recordings associated with a specific work.

        :param work_uuid: A work uuid.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/work/{work_uuid}/recordings"
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}
