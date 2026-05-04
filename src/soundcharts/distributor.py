from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
)


class Distributor:

    @staticmethod
    def get_distributor_upc_prefixes(distributor_uuid, offset=0, limit=100):
        """
        Retrieve all UPC prefixes mapped to a specific distributor for accurate catalog attribution.

        :param distributor_uuid: A distributor UUID.
        :param offset: Pagination offset.  Default: 0.
        :param limit: Number of results to retrieve.  None: no limit.  Default: 100.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/distributor/{distributor_uuid}/upc-roots"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def add_upc_to_a_distributor(distributor_uuid, upc):
        """
        Assign a missing UPC to a distributor.

        :param distributor_uuid: A distributor UUID.
        :param upc: An album UPC.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/distributor/{distributor_uuid}/upcs/{upc}"
        result = request_wrapper(endpoint, method="POST")
        return result if result is not None else {}

    @staticmethod
    def remove_upc_from_a_distributor(distributor_uuid, upc):
        """
        Unlink an incorrect UPC from a distributor to fix mapping errors.

        :param distributor_uuid: A distributor UUID.
        :param upc: An album UPC.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/distributor/{distributor_uuid}/upcs/{upc}"

        result = request_wrapper(endpoint, method="DELETE")
        return result if result is not None else {}


class DistributorAsync:

    @staticmethod
    async def get_distributor_upc_prefixes(distributor_uuid, offset=0, limit=100):
        """
        Retrieve all UPC prefixes mapped to a specific distributor for accurate catalog attribution.

        :param distributor_uuid: A distributor UUID.
        :param offset: Pagination offset.  Default: 0.
        :param limit: Number of results to retrieve.  None: no limit.  Default: 100.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/distributor/{distributor_uuid}/upc-roots"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def add_upc_to_a_distributor(distributor_uuid, upc):
        """
        Assign a missing UPC to a distributor.

        :param distributor_uuid: A distributor UUID.
        :param upc: An album UPC.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/distributor/{distributor_uuid}/upcs/{upc}"
        result = await request_wrapper_async(endpoint, method="POST")
        return result if result is not None else {}

    @staticmethod
    async def remove_upc_from_a_distributor(distributor_uuid, upc):
        """
        Unlink an incorrect UPC from a distributor to fix mapping errors.

        :param distributor_uuid: A distributor UUID.
        :param upc: An album UPC.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/distributor/{distributor_uuid}/upcs/{upc}"

        result = await request_wrapper_async(endpoint, method="DELETE")
        return result if result is not None else {}
