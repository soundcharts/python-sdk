from datetime import date, datetime, timedelta, timezone

from .api_util import (
    _run_blocking,
    request_wrapper,
    request_looper,
    request_wrapper_async,
    request_looper_async,
    sort_items_by_date,
    list_join,
)


def _validate_tracklisting_period(period, end_date):
    if isinstance(period, bool) or not isinstance(period, int) or period <= 0:
        raise ValueError("period must be a positive integer")
    if end_date is not None:
        if not isinstance(end_date, str):
            raise ValueError("end_date must be a valid YYYY-MM-DD date")
        try:
            parsed = date.fromisoformat(end_date)
        except ValueError:
            raise ValueError("end_date must be a valid YYYY-MM-DD date") from None
        if parsed.isoformat() != end_date:
            raise ValueError("end_date must be a valid YYYY-MM-DD date")


async def _tracklisting_history(endpoint, period, end_date, offset, limit):
    end = date.fromisoformat(end_date) if end_date else datetime.now(timezone.utc).date()
    if period > end.toordinal():
        raise ValueError("period extends before year 1")
    start = end - timedelta(days=period - 1)
    offset = max(int(offset or 0), 0)
    limit = None if limit is None else int(limit)
    if limit is not None and limit < 0:
        raise ValueError("limit must be nonnegative")
    dates = {}
    result = {}
    for days_back in range(0, period, 90):
        window = await request_looper_async(
            endpoint,
            {
                "period": min(90, period - days_back),
                "endDate": (end - timedelta(days=days_back)).isoformat(),
                "offset": 0,
                "limit": None,
            },
            _strict=True,
        )
        if (
            not isinstance(window, dict)
            or not isinstance(window.get("items"), list)
            or window.get("errors") or window.get("error")
            or "total" not in (window.get("page") or {})
            or len(window["items"]) != window["page"]["total"]
        ):
            raise RuntimeError("Incomplete playlist tracklisting window")
        result.update(window)
        for item in window["items"]:
            try:
                instant = datetime.fromisoformat(item.replace("Z", "+00:00"))
                if instant.tzinfo is None:
                    instant = instant.replace(tzinfo=timezone.utc)
                instant = instant.astimezone(timezone.utc)
            except (AttributeError, TypeError, ValueError, OverflowError):
                raise RuntimeError("Invalid playlist tracklisting timestamp") from None
            if start <= instant.date() <= end:
                dates.setdefault(instant, item)
    items = [dates[instant] for instant in sorted(dates, reverse=True)]
    result["items"] = items[offset:None if limit is None else offset + limit]
    result["page"] = {"total": len(items), "offset": offset, "limit": limit}
    return result


class Playlist:

    @staticmethod
    def get_playlists(platform, offset=0, limit=100, body=None, print_progress=False):
        """
        You can sort playlists in our database using specific parameters such as the number of followers, 28-day adds, track count, or last updated date. Apply filters based on attributes like genre, type, country, owner, track age, percentage of adds over the last 28 days, or performance metrics.
        Please note that you can only retrieve the playlists for one platform at a time.

        :param platform: A playlist Chart platform code. Default: spotify.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit (warning: can take up to 100,000 calls - you may want to use parallel processing). Default: 100.
        :param body: JSON Payload. If none, the default sorting will apply (by metric for the platforms who have one, by 28DayAdds for others) and there will be no filters.
        :param print_progress: Prints an estimated progress percentage (default: False).
        :return: JSON response or an empty dictionary.
        """

        ref_metric_types = {
            "spotify": "likes",
            "youtube": "views",
            "deezer": "fans",
            "jiosaavn": "followers",
            "boomplay": "favorites",
        }

        if body == None:
            body = {
                "sort": {
                    "type": "28DayAdds",
                    "order": "desc",
                },
                "filters": [],
            }
            if platform in ref_metric_types:
                body = {
                    "sort": {
                        "type": "metric",
                        "platform": platform,
                        "metricType": ref_metric_types[platform],
                        "sortBy": "total",
                        "period": "month",
                        "order": "desc",
                    },
                    "filters": [],
                }

        endpoint = f"/api/v2/top/playlists/{platform}"
        params = {"offset": offset, "limit": limit}

        result = request_looper(endpoint, params, body, print_progress=print_progress)
        return result if result is not None else {}

    @staticmethod
    def get_playlist_metadata(playlist_uuid):
        """
        Get a playlist's metadata using their UUID.

        :param playlist_uuid: A playlist UUID.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.8/playlist/{playlist_uuid}"
        result = request_wrapper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_playlist_metadata_batch(playlist_uuids):
        """
        Get the metadata of several playlists using their UUIDs.

        :param playlist_uuids: A list of playlist UUIDs.
        :return: JSON response or an empty dictionary.
        """
        if not isinstance(playlist_uuids, list):
            raise TypeError("playlist_uuids must be a list")
        endpoint = f"/api/v2/playlist/{list_join(playlist_uuids)}"
        result = request_looper(endpoint)
        return result if result is not None else {}

    @staticmethod
    def get_playlist_by_platform_id(platform, identifier, country_code=None):
        """
        Get Soundcharts’ UUID & the playlist's metadata.

        :param platform: A platform code.
        :param identifier: A playlist platform identifier.
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2). Required for apple-music and amazon.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.8/playlist/by-platform/{platform}/{identifier}"
        params = {"countryCode": country_code}
        result = request_wrapper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_curators_by_platform(platform="spotify", offset=0, limit=100):
        """
        Get the listing of all playlist curators know by Soundcharts.

        :param platform: A playlist Chart platform code. Default: spotify.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/playlist/curators/{platform}"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_playlists_by_curator(
        platform,
        curator_identifier,
        country_code=None,
        offset=0,
        limit=100,
        sort_by="name",
        sort_order="asc",
    ):
        """
        Get the listing of all playlists made by a specific curator.

        :param platform: A playlist platform code.
        :param curator_identifier: A playlist curator identifier
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2). Required for apple-music and amazon.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : audience, name. Default: name.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/by-curator/{platform}/{curator_identifier}"
        params = {
            "countryCode": country_code,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_playlists_by_type(
        platform,
        playlist_type,
        country_code=None,
        offset=0,
        limit=100,
        sort_by="name",
        sort_order="asc",
    ):
        """
        Get the listing of all playlist with a specific type/nationality.

        :param platform: A playlist platform code.
        :param playlist_type: A playlist type (algorithmic, charts, curators_listeners, editorial, algotorial, major, radios, this_is.)
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2). Required for apple-music and amazon.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : audience, name. Default: name.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/by-type/{platform}/{playlist_type}"
        params = {
            "countryCode": country_code,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_audience(playlist_uuid, start_date=None, end_date=None, sort=None):
        """
        Get the playlist’s number of followers/fans/views.

        :param playlist_uuid: A playlist UUID.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param sort: Optional sort order: asc or desc. None preserves the existing ordering.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/audience"
        params = {"startDate": start_date, "endDate": end_date, "sort": sort}
        result = request_looper(endpoint, params)
        return (
            {}
            if result is None
            else sort_items_by_date(
                result, reverse=True if sort is None else sort == "desc"
            )
        )

    @staticmethod
    def get_tracklisting_latest(playlist_uuid, offset=0, limit=100):
        """
        Get the latest playlist’s tracklisting.

        :param playlist_uuid: A playlist UUID.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/tracks/latest"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    def get_tracklisting_dates(
        playlist_uuid, period=30, end_date=None, offset=0, limit=100
    ):
        """
        Get the available playlist’s tracklisting dates.

        Periods over 90 cover period UTC calendar days ending at end_date
        (inclusive), or today's UTC date captured once. All windows of at most
        90 days are fetched, even for limit=0. Timestamps are filtered and sorted
        newest-first in UTC (naive values mean UTC); equal instants keep the first
        original string. Offset/limit apply once to the combined unique results;
        None means no limit. Page total counts those results before slicing,
        offset/limit describe the slice, and next/previous are omitted.
        Related metadata is retained; quota_remaining uses the latest response.
        Failed/incomplete windows or malformed timestamps raise, without partial
        history. Periods up to 90 retain API pagination and range behavior.

        :param playlist_uuid: A playlist UUID.
        :param period: Positive integer number of historical days. Default: 30.
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        _validate_tracklisting_period(period, end_date)
        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/available-tracklistings"
        if period > 90:
            return _run_blocking(
                _tracklisting_history(endpoint, period, end_date, offset, limit)
            )
        params = {
            "period": period,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = request_looper(endpoint, params)
        return {} if result is None else sort_items_by_date(result, True, None)

    @staticmethod
    def get_tracklisting_for_a_date(playlist_uuid, datetime, offset=0, limit=100):
        """
        Get the playlist’s tracklisting for a date.

        :param playlist_uuid: A playlist UUID.
        :param datetime: A ranking date (ATOM format)
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/tracks/{datetime}"
        params = {"offset": offset, "limit": limit}
        result = request_looper(endpoint, params)
        return result if result is not None else {}


class PlaylistAsync:

    @staticmethod
    async def get_playlists(
        platform, offset=0, limit=100, body=None, print_progress=False
    ):
        """
        You can sort playlists in our database using specific parameters such as the number of followers, 28-day adds, track count, or last updated date. Apply filters based on attributes like genre, type, country, owner, track age, percentage of adds over the last 28 days, or performance metrics.
        Please note that you can only retrieve the playlists for one platform at a time.

        :param platform: A playlist Chart platform code. Default: spotify.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit (warning: can take up to 100,000 calls - you may want to use parallel processing). Default: 100.
        :param body: JSON Payload. If none, the default sorting will apply (by metric for the platforms who have one, by 28DayAdds for others) and there will be no filters.
        :param print_progress: Prints an estimated progress percentage (default: False).
        :return: JSON response or an empty dictionary.
        """

        ref_metric_types = {
            "spotify": "likes",
            "youtube": "views",
            "deezer": "fans",
            "jiosaavn": "followers",
            "boomplay": "favorites",
        }

        if body == None:
            body = {
                "sort": {
                    "type": "28DayAdds",
                    "order": "desc",
                },
                "filters": [],
            }
            if platform in ref_metric_types:
                body = {
                    "sort": {
                        "type": "metric",
                        "platform": platform,
                        "metricType": ref_metric_types[platform],
                        "sortBy": "total",
                        "period": "month",
                        "order": "desc",
                    },
                    "filters": [],
                }

        endpoint = f"/api/v2/top/playlists/{platform}"
        params = {"offset": offset, "limit": limit}

        result = await request_looper_async(
            endpoint, params, body, print_progress=print_progress
        )
        return result if result is not None else {}

    @staticmethod
    async def get_playlist_metadata(playlist_uuid):
        """
        Get a playlist's metadata using their UUID.

        :param playlist_uuid: A playlist UUID.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.8/playlist/{playlist_uuid}"
        result = await request_wrapper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_playlist_metadata_batch(playlist_uuids):
        """
        Get the metadata of several playlists using their UUIDs.

        :param playlist_uuids: A list of playlist UUIDs.
        :return: JSON response or an empty dictionary.
        """
        if not isinstance(playlist_uuids, list):
            raise TypeError("playlist_uuids must be a list")
        endpoint = f"/api/v2/playlist/{list_join(playlist_uuids)}"
        result = await request_looper_async(endpoint)
        return result if result is not None else {}

    @staticmethod
    async def get_playlist_by_platform_id(platform, identifier, country_code=None):
        """
        Get Soundcharts’ UUID & the playlist's metadata.

        :param platform: A platform code.
        :param identifier: A playlist platform identifier.
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2). Required for apple-music and amazon.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.8/playlist/by-platform/{platform}/{identifier}"
        params = {"countryCode": country_code}
        result = await request_wrapper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_curators_by_platform(platform="spotify", offset=0, limit=100):
        """
        Get the listing of all playlist curators know by Soundcharts.

        :param platform: A playlist Chart platform code. Default: spotify.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2/playlist/curators/{platform}"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_playlists_by_curator(
        platform,
        curator_identifier,
        country_code=None,
        offset=0,
        limit=100,
        sort_by="name",
        sort_order="asc",
    ):
        """
        Get the listing of all playlists made by a specific curator.

        :param platform: A playlist platform code.
        :param curator_identifier: A playlist curator identifier
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2). Required for apple-music and amazon.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : audience, name. Default: name.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/by-curator/{platform}/{curator_identifier}"
        params = {
            "countryCode": country_code,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_playlists_by_type(
        platform,
        playlist_type,
        country_code=None,
        offset=0,
        limit=100,
        sort_by="name",
        sort_order="asc",
    ):
        """
        Get the listing of all playlist with a specific type/nationality.

        :param platform: A playlist platform code.
        :param playlist_type: A playlist type (algorithmic, charts, curators_listeners, editorial, algotorial, major, radios, this_is.)
        :param country_code: Country code (2 letters ISO 3166-2, example: 'US', full list on https://en.wikipedia.org/wiki/ISO_3166-2). Required for apple-music and amazon.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :param sort_by: Sort criteria. Available values are : audience, name. Default: name.
        :param sort_order: Sort order. Available values are : asc, desc. Default: asc
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/by-type/{platform}/{playlist_type}"
        params = {
            "countryCode": country_code,
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_audience(playlist_uuid, start_date=None, end_date=None, sort=None):
        """
        Get the playlist’s number of followers/fans/views.

        :param playlist_uuid: A playlist UUID.
        :param start_date: Optional period start date (format YYYY-MM-DD).
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param sort: Optional sort order: asc or desc. None preserves the existing ordering.
        :return: JSON response or an empty dictionary.
        """

        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/audience"
        params = {"startDate": start_date, "endDate": end_date, "sort": sort}
        result = await request_looper_async(endpoint, params)
        return (
            {}
            if result is None
            else sort_items_by_date(
                result, reverse=True if sort is None else sort == "desc"
            )
        )

    @staticmethod
    async def get_tracklisting_latest(playlist_uuid, offset=0, limit=100):
        """
        Get the latest playlist’s tracklisting.

        :param playlist_uuid: A playlist UUID.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/tracks/latest"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}

    @staticmethod
    async def get_tracklisting_dates(
        playlist_uuid, period=30, end_date=None, offset=0, limit=100
    ):
        """
        Get the available playlist’s tracklisting dates.

        Periods over 90 cover period UTC calendar days ending at end_date
        (inclusive), or today's UTC date captured once. All windows of at most
        90 days are fetched, even for limit=0. Timestamps are filtered and sorted
        newest-first in UTC (naive values mean UTC); equal instants keep the first
        original string. Offset/limit apply once to the combined unique results;
        None means no limit. Page total counts those results before slicing,
        offset/limit describe the slice, and next/previous are omitted.
        Related metadata is retained; quota_remaining uses the latest response.
        Failed/incomplete windows or malformed timestamps raise, without partial
        history. Periods up to 90 retain API pagination and range behavior.

        :param playlist_uuid: A playlist UUID.
        :param period: Positive integer number of historical days. Default: 30.
        :param end_date: Optional period end date (format YYYY-MM-DD), leave empty for the latest results.
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        _validate_tracklisting_period(period, end_date)
        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/available-tracklistings"
        if period > 90:
            return await _tracklisting_history(endpoint, period, end_date, offset, limit)
        params = {
            "period": period,
            "endDate": end_date,
            "offset": offset,
            "limit": limit,
        }
        result = await request_looper_async(endpoint, params)
        return {} if result is None else sort_items_by_date(result, True, None)

    @staticmethod
    async def get_tracklisting_for_a_date(playlist_uuid, datetime, offset=0, limit=100):
        """
        Get the playlist’s tracklisting for a date.

        :param playlist_uuid: A playlist UUID.
        :param datetime: A ranking date (ATOM format)
        :param offset: Pagination offset. Default: 0.
        :param limit: Number of results to retrieve. None: no limit. Default: 100.
        :return: JSON response or an empty dictionary.
        """
        endpoint = f"/api/v2.20/playlist/{playlist_uuid}/tracks/{datetime}"
        params = {"offset": offset, "limit": limit}
        result = await request_looper_async(endpoint, params)
        return result if result is not None else {}
