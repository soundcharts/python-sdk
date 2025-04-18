from .api_util import request_wrapper, request_looper
import json


class Tiktok:

    @staticmethod
    def get_music(identifier):
        """
        Get metadata for the TikTok ID. This endpoint is restricted to specific plans.

        :param identifier: A TikTok identifier.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/tiktok/music/{identifier}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_music_video_count(identifier, end_date=None, period=90):
        """
        Get the video count for a specific TikTok ID. This endpoint is restricted to specific plans.

        :param identifier: A TikTok identifier.
        :param end_date: Optional period filter (YYYY-MM-DD format).
        :param period: Number of historical days (max. 90).
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/tiktok/music/{identifier}/video/volume"
        params = {"endDate": end_date, "period": period}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_music_videos(identifier, offset=0, limit=100):
        """
        Get the audience metric (comment/shares/likes/play) for this link’s top videos. This endpoint is restricted to specific plans.

        :param identifier: A TikTok identifier.
        :param offset: Pagination offset.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/tiktok/music/{identifier}/videos"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_user(username):
        """
        Get the ID and the follower count for a specific user. This endpoint is restricted to specific plans.

        :param username: A TikTok username.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/tiktok/user/{username}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_video(identifier):
        """
        Get the video’s current audience data (comments/likes/plays/shares) and the user’s ID and data. This endpoint is restricted to specific plans.

        :param identifier: A TikTok video identifier.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2/tiktok/video/{identifier}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def add_music_links(links):
        """
        Add missing TikTok music links. This endpoint is restricted to specific plans.

        :param links: A list of TikTok music links.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/tiktok/music/urls/add"

        body = json.dumps({"urls": links})

        result = request_wrapper(endpoint, body=body)
        return result if result is not None else {}

    @staticmethod
    def add_user_links(links):
        """
        Add missing TikTok users. This endpoint is restricted to specific plans.

        :param links: A list of TikTok user links.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/tiktok/user/urls/add"

        body = json.dumps({"urls": links})

        result = request_wrapper(endpoint, body=body)
        return result if result is not None else {}
