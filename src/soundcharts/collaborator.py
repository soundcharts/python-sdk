from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
    list_join,
)


class Collaborator:
    @staticmethod
    def get_collaborators(
        role=None,
        offset=0,
        limit=100,
        body=None,
        print_progress=False,
    ):
        """
        Get a list of collaborators ranked by global metrics and filtered by attributes and stats.

        :param role: A collaborator role.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit (warning: can take up to 100,000 calls - you may want to use parallel processing). Default: 100.
        :param body: JSON Payload. If none, the default sorting will apply (descending spotify followers) and there will be no filters.
        :param print_progress: Prints an estimated progress percentage (default: False).
        :return: JSON response or an empty dictionary.
        """

        if body == None:
            body = {
                "sort": {
                    "platform": "spotify",
                    "metricType": "followers",
                    "period": "month",
                    "sortBy": "total",
                    "order": "desc",
                },
                "filters": [],
            }

        endpoint = f"/api/v2/top/collaborators"
        params = {
            "role": role,
            "offset": offset,
            "limit": limit,
        }

        result = request_looper(endpoint, params, body, print_progress=print_progress)
        return result if result is not None else {}

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
    def get_collaborator_metadata_batch(collaborator_uuids):
        """
        Get the metadata of several collaborators using their UUIDs.

        :param collaborator_uuids: A list of artist UUIDs.
        :return: JSON response or an empty dictionary.
        """
        if not isinstance(collaborator_uuids, list):
            raise TypeError("artist_uuids must be a list")
        endpoint = f"/api/v2.9/artist/{list_join(collaborator_uuids)}"
        result = request_looper(endpoint)
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
    def get_ids(collaborator_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this collaborator.

        :param collaborator_uuid: A collaborator uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/collaborator/{collaborator_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_songs(collaborator_uuid, offset=0, limit=100):
        """
        Get songs by a specific collaborator.

        :param collaborator_uuid: A collaborator uuid.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/collaborator/{collaborator_uuid}/songs"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_albums(collaborator_uuid, offset=0, limit=100):
        """
        Get albums by a specific collaborator.

        :param collaborator_uuid: A collaborator uuid.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/collaborator/{collaborator_uuid}/albums"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_audience(
        collaborator_uuid,
        platform="instagram",
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
        sort="asc",
    ):
        """
        Get a collaborator's followers across services.

        :param collaborator_uuid: A collaborator UUID.
        :param platform: A social platform code. Default: instagram.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort: Sort. Available value asc|desc. Default: asc.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/collaborator/{collaborator_uuid}/audience/{platform}"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        result = request_looper(endpoint, params)
        return {} if result is None or len(result) == 0 else sort_items_by_date(result)


class CollaboratorAsync:
    @staticmethod
    async def get_collaborators(
        role=None,
        offset=0,
        limit=100,
        body=None,
        print_progress=False,
    ):
        """
        Get a list of collaborators ranked by global metrics and filtered by attributes and stats.

        :param role: A collaborator role.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit (warning: can take up to 100,000 calls - you may want to use parallel processing). Default: 100.
        :param body: JSON Payload. If none, the default sorting will apply (descending spotify followers) and there will be no filters.
        :param print_progress: Prints an estimated progress percentage (default: False).
        :return: JSON response or an empty dictionary.
        """

        if body == None:
            body = {
                "sort": {
                    "platform": "spotify",
                    "metricType": "followers",
                    "period": "month",
                    "sortBy": "total",
                    "order": "desc",
                },
                "filters": [],
            }

        endpoint = f"/api/v2/top/collaborators"
        params = {
            "role": role,
            "offset": offset,
            "limit": limit,
        }

        result = await request_looper_async(
            endpoint, params, body, print_progress=print_progress
        )
        return result if result is not None else {}

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
    async def get_collaborator_metadata_batch(collaborator_uuids):
        """
        Get the metadata of several collaborators using their UUIDs.

        :param collaborator_uuids: A list of artist UUIDs.
        :return: JSON response or an empty dictionary.
        """
        if not isinstance(collaborator_uuids, list):
            raise TypeError("artist_uuids must be a list")
        endpoint = f"/api/v2.9/artist/{list_join(collaborator_uuids)}"
        result = await request_looper_async(endpoint)
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
    async def get_ids(collaborator_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs belonging to this collaborator.

        :param collaborator_uuid: A collaborator uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/collaborator/{collaborator_uuid}/identifiers"
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_songs(collaborator_uuid, offset=0, limit=100):
        """
        Get songs by a specific collaborator.

        :param collaborator_uuid: A festival uuid.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/collaborator/{collaborator_uuid}/songs"
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_albums(collaborator_uuid, offset=0, limit=100):
        """
        Get albums by a specific collaborator.

        :param collaborator_uuid: A collaborator uuid.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/collaborator/{collaborator_uuid}/albums"
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_audience(
        collaborator_uuid,
        platform="instagram",
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
        sort="asc",
    ):
        """
        Get a collaborator's followers across services.

        :param collaborator_uuid: A collaborator UUID.
        :param platform: A social platform code. Default: instagram.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort: Sort. Available value asc|desc. Default: asc.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/collaborator/{collaborator_uuid}/audience/{platform}"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        result = await request_looper_async(endpoint, params)
        return {} if result is None or len(result) == 0 else sort_items_by_date(result)
