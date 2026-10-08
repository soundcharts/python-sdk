from .api_util import (
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
)


class City:

    @staticmethod
    def get_concerts_by_citykey(
        city_key, start_date=None, end_date=None, offset=0, limit=None
    ):
        """
        Get the upcoming & past concerts in a given city.
        :param city_key: Add a cityKey. Available values can be found by calling referential.get_cities_for_artist_ranking.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/venue/concerts/by-city-key"
        params = {
            "cityKey": city_key,
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_festivals_by_citykey(city_key):
        """
        Get the festivals in a given city.
        :param city_key: Add a cityKey. Available values can be found by calling referential.get_cities_for_artist_ranking.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/festival/by-city-key"
        params = {
            "cityKey": city_key,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_venues_by_citykey(city_key):
        """
        Get the venues in a given city.
        :param city_key: Add a cityKey. Available values can be found by calling referential.get_cities_for_artist_ranking.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/venue/by-city-key"
        params = {
            "cityKey": city_key,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}


class CityAsync:

    @staticmethod
    async def get_concerts_by_citykey(
        city_key, start_date=None, end_date=None, offset=0, limit=None
    ):
        """
        Get the upcoming & past concerts in a given city.
        :param city_key: Add a cityKey. Available values can be found by calling referential.get_cities_for_artist_ranking.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/venue/concerts/by-city-key"
        params = {
            "cityKey": city_key,
            "startDate": start_date,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = await request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_festivals_by_citykey(city_key):
        """
        Get the festivals in a given city.
        :param city_key: Add a cityKey. Available values can be found by calling referential.get_cities_for_artist_ranking.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/festival/by-city-key"
        params = {
            "cityKey": city_key,
        }
        result = await request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_venues_by_citykey(city_key):
        """
        Get the venues in a given city.
        :param city_key: Add a cityKey. Available values can be found by calling referential.get_cities_for_artist_ranking.

        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/venue/by-city-key"
        params = {
            "cityKey": city_key,
        }
        result = await request_looper(endpoint, params)
        return result if result is not None else {}
