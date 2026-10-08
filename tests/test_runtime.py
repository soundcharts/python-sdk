import inspect
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from soundcharts import api_util
from soundcharts.artist import Artist, ArtistAsync
from soundcharts.datafeed import DataFeed, DataFeedAsync
from soundcharts.distributor import Distributor, DistributorAsync
from soundcharts.favorite import Favorite, FavoriteAsync
from soundcharts.city import CityAsync
from soundcharts.collaborator import CollaboratorAsync
from soundcharts.label import LabelAsync
from soundcharts.referential import ReferentialAsync
from soundcharts.song import SongAsync
from soundcharts.search import Search
from soundcharts.client import SoundchartsClient, SoundchartsClientAsync


class TransportTest(unittest.TestCase):
    def setUp(self):
        api_util.setup(app_id="test", api_key="test", base_url="https://example.invalid")
        self.payload = {"items": [{"uuid": "result"}], "page": {"total": 1, "next": None}}
        self.response = MagicMock(status=200, headers={"x-quota-remaining": "42"})
        self.response.text = AsyncMock(return_value="response")
        self.response.json = AsyncMock(side_effect=lambda: dict(self.payload))
        self.session = MagicMock()
        self.session.request.return_value.__aenter__ = AsyncMock(return_value=self.response)
        self.session.__aenter__ = AsyncMock(return_value=self.session)
        self.session.close = AsyncMock()
        transport = patch("soundcharts.api_util.aiohttp.ClientSession", return_value=self.session)
        transport.start()
        self.addCleanup(transport.stop)

    def assert_request(self, method, endpoint, params=None, body=None):
        headers = {"x-app-id": "test", "x-api-key": "test"}
        if body:
            headers["Content-Type"] = "application/json"
        self.session.request.assert_called_once_with(
            method, "https://example.invalid" + endpoint, params=params or {},
            headers=headers, data=json.dumps(body) if body else None,
        )
        self.session.request.reset_mock()

    def assert_result(self, result):
        self.assertEqual(result, dict(self.payload, quota_remaining=42))


class WrapperTests(TransportTest, unittest.IsolatedAsyncioTestCase):
    async def test_methods(self):
        for method, body, expected in [
            ("POST", None, "POST"), ("pOsT", {"uuid": "one"}, "POST"),
            (None, None, "GET"), (None, {}, "GET"),
            (None, {"uuid": "one"}, "POST"), ("dElEtE", None, "DELETE"),
        ]:
            with self.subTest(method=method, body=body):
                result = await api_util.request_wrapper_async(
                    "/test", params={"enabled": True, "offset": 0}, body=body, method=method,
                )
                self.assert_result(result)
                self.assert_request(expected, "/test", {"enabled": "true"}, body)

    async def test_unsupported_methods(self):
        for method in ["GET", "PUT", "PATCH", "HEAD", "OPTIONS"]:
            with self.subTest(method=method), self.assertRaisesRegex(ValueError, "Unsupported HTTP method"):
                await api_util.request_wrapper_async("/test", method=method)
        self.session.request.assert_not_called()


def mutation_cases(feed, distributor, favorite, artist):
    params = {"uuid": "id", "code": "feed", "storageCode": "store"}
    return [
        (feed.subscribe_to_a_feed, ("id", "feed", "store"), "POST", "/api/v2/data-feed/configured", dict(params, pushInterval=86400)),
        (feed.unsubscribe_from_feed, ("id", "feed", "store"), "DELETE", "/api/v2/data-feed/configured", params),
        (distributor.add_upc_to_a_distributor, ("id", "123"), "POST", "/api/v2/distributor/id/upcs/123", {}),
        (distributor.remove_upc_from_a_distributor, ("id", "123"), "DELETE", "/api/v2/distributor/id/upcs/123", {}),
        (favorite.add_artist_to_favorites, ("id",), "POST", "/api/v2/favorite/artist/id", {}),
        (favorite.remove_artist_from_favorites, ("id",), "DELETE", "/api/v2/favorite/artist/id", {}),
        (artist.unlock_audience_report, ("id", "instagram"), "POST", "/api/v2/artist/id/audience/instagram/report", {}),
    ]


class SyncCallerTests(TransportTest):
    def test_mutations(self):
        for method, args, verb, endpoint, params in mutation_cases(DataFeed, Distributor, Favorite, Artist):
            with self.subTest(method=method.__qualname__):
                self.assert_result(method(*args))
                self.assert_request(verb, endpoint, params)


class AsyncCallerTests(TransportTest, unittest.IsolatedAsyncioTestCase):
    async def test_mutations(self):
        for method, args, verb, endpoint, params in mutation_cases(DataFeedAsync, DistributorAsync, FavoriteAsync, ArtistAsync):
            with self.subTest(method=method.__qualname__):
                self.assert_result(await method(*args))
                self.assert_request(verb, endpoint, params)


class AsyncHelperTests(TransportTest, unittest.IsolatedAsyncioTestCase):
    async def check_method(self, method, args, endpoint, params, **kwargs):
        self.assert_result(await method(*args, **kwargs))
        self.assert_request("GET", endpoint, params)
        self.response.json.side_effect = None
        self.response.json.return_value = None
        self.assertEqual(await method(*args, **kwargs), {})
        self.assert_request("GET", endpoint, params)

    async def test_city_concerts(self):
        await self.check_method(CityAsync.get_concerts_by_citykey, ("paris",),
                                "/api/v2/venue/concerts/by-city-key", {"cityKey": "paris"})

    async def test_city_concerts_filters(self):
        await self.check_method(CityAsync.get_concerts_by_citykey, ("paris",),
                                "/api/v2/venue/concerts/by-city-key",
                                {"cityKey": "paris", "startDate": "2026-01-01", "endDate": "2026-02-01", "offset": 3, "limit": 5},
                                start_date="2026-01-01", end_date="2026-02-01", offset=3, limit=5)

    async def test_city_festivals(self):
        await self.check_method(CityAsync.get_festivals_by_citykey, ("paris",),
                                "/api/v2/festival/by-city-key", {"cityKey": "paris"})

    async def test_city_venues(self):
        await self.check_method(CityAsync.get_venues_by_citykey, ("paris",),
                                "/api/v2/venue/by-city-key", {"cityKey": "paris"})

    async def test_collaborator_songs(self):
        await self.check_method(CollaboratorAsync.get_songs, ("id",),
                                "/api/v2/collaborator/id/songs", {"limit": 100})

    async def test_label_ids(self):
        await self.check_method(LabelAsync.get_ids, ("id",),
                                "/api/v2/label/id/identifiers", {"limit": 100})

    async def test_label_ids_filters(self):
        await self.check_method(LabelAsync.get_ids, ("id",),
                                "/api/v2/label/id/identifiers", {"platform": "spotify", "offset": 2, "limit": 10},
                                platform="spotify", offset=2, limit=10)

    async def test_referential_cities(self):
        await self.check_method(ReferentialAsync.get_cities_for_venue_festival, ("FR",),
                                "/api/v2/referential/venue/cities/FR", {"limit": 100})

    async def test_referential_cities_filters(self):
        await self.check_method(ReferentialAsync.get_cities_for_venue_festival, ("FR",),
                                "/api/v2/referential/venue/cities/FR", {"searchCity": "Paris", "offset": 2, "limit": 10},
                                search_city="Paris", offset=2, limit=10)

    async def test_song_related_tracks(self):
        await self.check_method(SongAsync.get_related_tracks, ("id",),
                                "/api/v2/song/id/related", {})


class SearchTests(TransportTest):
    def check_search(self, method, entity):
        for kwargs, params in [({}, {"limit": 20}), ({"offset": 2, "limit": 50}, {"offset": 2, "limit": 20})]:
            with self.subTest(kwargs=kwargs):
                result = method("Blue", **kwargs)
                if inspect.iscoroutine(result):
                    result.close()
                self.assert_result(result)
                self.assert_request("GET", f"/api/v2/{entity}/search/Blue", params)
        self.response.json.side_effect = None
        self.response.json.return_value = None
        self.assertEqual(method("Blue"), {})
        self.assert_request("GET", f"/api/v2/{entity}/search/Blue", {"limit": 20})

    def test_album(self):
        self.check_search(Search.search_album_by_name, "album")

    def test_collaborator(self):
        self.check_search(Search.search_collaborator_by_name, "collaborator")


class ClientTests(unittest.TestCase):
    def test_sync_aliases(self):
        client = SoundchartsClient(app_id="test", api_key="test")
        self.assertIsInstance(client.data_feed, DataFeed)
        self.assertIs(client.data_feed, client.datafeed)

    def test_async_aliases(self):
        client = SoundchartsClientAsync(app_id="test", api_key="test")
        self.assertIsInstance(client.datafeed, DataFeedAsync)
        self.assertIs(client.datafeed, client.data_feed)
