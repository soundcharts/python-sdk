from .api_util import request_wrapper, request_looper


class User:
    @staticmethod
    def get_blocklist_artists(email, offset=0, limit=100):
        """
        Get a dashboard user’s blocklists for artist profiles.

        :param email: An url-encoded user email.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/user/{email}/blocklist/artists"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_blocklist_songs(email, offset=0, limit=100):
        """
        Get a dashboard user’s blocklists for song profiles.

        :param email: An url-encoded user email.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/user/{email}/blocklist/songs"
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_blocklist_labels(email, offset=0, limit=100):
        """
        Get a dashboard user’s blocklists for labels profiles.

        :param email: An url-encoded user email.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        params = {"offset": offset, "limit": limit}

        endpoint = f"/api/v2/user/{email}/blocklist/labels"
        result = request_looper(endpoint, params)
        return result if result is not None else {}
