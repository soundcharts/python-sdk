from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
)


class Collaborator:

    @staticmethod
    def get_collaborator_metadata(collaborator_uuid):
        """
        Retrieve detailed profile information and contact metadata for a specific music collaborator.

        :param collaborator_uuid: A collaborator uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/collaborator/{collaborator_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_collaborator_by_ipi(ipi):
        """
        Retrieve detailed profile information and contact metadata for a specific music collaborator.

        :param ipi: An collaborator ipi.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/collaborator/by-ipi/{ipi}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_collaborator_by_platform_id(platform, identifier):
        """
        Retrieve detailed profile information and contact metadata for a specific music collaborator.

        :param platform: A platform code.
        :param identifier: An collaborator platform identifier.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/collaborator/by-platform/{platform}/{identifier}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_ids(festival_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this festival.

        :param festival_uuid: A festival uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/festival/{festival_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}


class CollaboratorAsync:

    @staticmethod
    async def get_collaborator_metadata(collaborator_uuid):
        """
        Retrieve detailed profile information and contact metadata for a specific music collaborator.

        :param collaborator_uuid: A collaborator uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/collaborator/{collaborator_uuid}"
        result = await request_wrapper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_collaborator_by_ipi(ipi):
        """
        Retrieve detailed profile information and contact metadata for a specific music collaborator.

        :param ipi: An collaborator ipi.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/collaborator/by-ipi/{ipi}"
        result = await request_wrapper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_collaborator_by_platform_id(platform, identifier):
        """
        Retrieve detailed profile information and contact metadata for a specific music collaborator.

        :param platform: A platform code.
        :param identifier: An collaborator platform identifier.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/collaborator/by-platform/{platform}/{identifier}"
        result = await request_wrapper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_ids(festival_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this festival.

        :param festival_uuid: A festival uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/festival/{festival_uuid}/identifiers"
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}
