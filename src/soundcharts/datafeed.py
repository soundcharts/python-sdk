from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
)


class DataFeed:

    @staticmethod
    def get_available_feeds(entity_type):
        """
        Retrieve the catalog of subscribable data streams.

        :param entity_type: Entity type. Values are : artist, album, song, playlist.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/data-feed/available"
        params = {"entityType": entity_type}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_active_feeds(entity_type, code, storage_code, offset, limit):
        """
        Retrieve all currently running data feed subscriptions.

        :param entity_type: Entity type. Values are : artist, album, song, playlist.
        :param code: Feed code.
        :param storage_code: Feed connector code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/data-feed/configured"
        params = {
            "entityType": entity_type,
            "code": code,
            "storageCode": storage_code,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def subscribe_to_a_feed(uuid, code, storage_code, push_interval=86400):
        """
        Subscribe to a specific data stream for targeted entities.

        :param uuid: An entity UUID.
        :param code: Feed code.
        :param storage_code: Feed connector code.
        :param push_interval: Push interval. From 1h to 1 week defined in seconds. Default: 86400.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/data-feed/configured"
        params = {
            "uuid": uuid,
            "code": code,
            "storageCode": storage_code,
            "pushInterval": push_interval,
        }
        result = request_wrapper(endpoint, params, method="POST")
        return result if result is not None else {}

    @staticmethod
    def unsubscribe_from_feed(uuid, code, storage_code):
        """
        Unsubscribe from an active data feed to halt delivery.

        :param uuid: An entity UUID.
        :param code: Feed code.
        :param storage_code: Feed connector code.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/data-feed/configured"
        params = {
            "uuid": uuid,
            "code": code,
            "storageCode": storage_code,
        }
        result = request_wrapper(endpoint, params, method="DELETE")
        return result if result is not None else {}


class DataFeedAsync:

    @staticmethod
    async def get_available_feeds(entity_type):
        """
        Retrieve the catalog of subscribable data streams.

        :param entity_type: Entity type. Values are : artist, album, song, playlist.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/data-feed/available"
        params = {"entityType": entity_type}
        result = await request_wrapper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_active_feeds(entity_type, code, storage_code, offset, limit):
        """
        Retrieve all currently running data feed subscriptions.

        :param entity_type: Entity type. Values are : artist, album, song, playlist.
        :param code: Feed code.
        :param storage_code: Feed connector code.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/data-feed/configured"
        params = {
            "entityType": entity_type,
            "code": code,
            "storageCode": storage_code,
            "offset": offset,
            "limit": limit,
        }
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def subscribe_to_a_feed(uuid, code, storage_code, push_interval=86400):
        """
        Subscribe to a specific data stream for targeted entities.

        :param uuid: An entity UUID.
        :param code: Feed code.
        :param storage_code: Feed connector code.
        :param push_interval: Push interval. From 1h to 1 week defined in seconds. Default: 86400.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/data-feed/configured"
        params = {
            "uuid": uuid,
            "code": code,
            "storageCode": storage_code,
            "pushInterval": push_interval,
        }
        result = await request_wrapper_async(endpoint, params, method="POST")
        return result if result is not None else {}

    @staticmethod
    async def unsubscribe_from_feed(uuid, code, storage_code):
        """
        Unsubscribe from an active data feed to halt delivery.

        :param uuid: An entity UUID.
        :param code: Feed code.
        :param storage_code: Feed connector code.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/data-feed/configured"
        params = {
            "uuid": uuid,
            "code": code,
            "storageCode": storage_code,
        }
        result = await request_wrapper_async(endpoint, params, method="DELETE")
        return result if result is not None else {}
