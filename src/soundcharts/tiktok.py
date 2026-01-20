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
