from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
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
        result = await request_looper(endpoint, params)
        return result if result is not None else {}
