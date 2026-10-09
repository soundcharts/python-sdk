from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
    list_join,
)


class Label:

    @staticmethod
    def get_label_metadata(label_uuid):
        """
        Get label metadata information using their UUID.

        :param collaborator_uuid: A collaborator uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/label/{label_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_label_metadata_batch(label_uuids):
        """
        Get the metadata of several labels using their UUIDs.

        :param label_uuids: A list of label UUIDs.
        :return: JSON response or an empty dictionary.
        """
        if not isinstance(label_uuids, list):
            raise TypeError("label_uuids must be a list")
        endpoint = f"/api/v2/label/{list_join(label_uuids)}"
        result = request_looper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_ids(label_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs and industry identifiers associated with a specific label.

        :param label_uuid: A label uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/label/{label_uuid}/identifiers"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_audience(
        label_uuid,
        platform="instagram",
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
        sort="asc",
    ):
        """
        Get a label's followers across services.

        :param label_uuid: A label UUID.
        :param platform: A social platform code. Default: instagram.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort: Sort. Available value asc|desc. Default: asc.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/label/{label_uuid}/audience/{platform}"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        result = request_looper(endpoint, params)
        return {} if result is None or len(result) == 0 else sort_items_by_date(result)


class LabelAsync:

    @staticmethod
    async def get_label_metadata(label_uuid):
        """
        Get label metadata information using their UUID.

        :param collaborator_uuid: A collaborator uuid.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/label/{label_uuid}"
        result = await request_wrapper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_label_metadata_batch(label_uuids):
        """
        Get the metadata of several labels using their UUIDs.

        :param label_uuids: A list of label UUIDs.
        :return: JSON response or an empty dictionary.
        """
        if not isinstance(label_uuids, list):
            raise TypeError("label_uuids must be a list")
        endpoint = f"/api/v2/label/{list_join(label_uuids)}"
        result = await request_looper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_ids(label_uuid, platform=None, offset=0, limit=100):
        """
        Get platform URLs and industry identifiers associated with a specific label.

        :param label_uuid: A label uuid.
        :param platform: An optional platform code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"platform": platform, "offset": offset, "limit": limit}

        endpoint = f"/api/v2/label/{label_uuid}/identifiers"
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_audience(
        label_uuid,
        platform="instagram",
        start_date=None,
        end_date=None,
        offset=0,
        limit=100,
        sort="asc",
    ):
        """
        Get a label's followers across services.

        :param label_uuid: A label UUID.
        :param platform: A social platform code. Default: instagram.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort: Sort. Available value asc|desc. Default: asc.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/label/{label_uuid}/audience/{platform}"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        result = await request_looper_async(endpoint, params)
        return {} if result is None or len(result) == 0 else sort_items_by_date(result)
