"""Offline contract tests for the SDK's documented query parameters."""
import asyncio
import copy
import importlib
import inspect
import unittest
from unittest.mock import AsyncMock, Mock, patch


class ContractTest(unittest.TestCase):
    def invoke(self, module, method, args=(), kwargs=None, asynchronous=False, response=None):
        module = importlib.import_module('soundcharts.' + module)
        cls = getattr(module, module.__name__.split('.')[-1].title() + ('Async' if asynchronous else ''))
        function = getattr(cls, method)
        mock_type = AsyncMock if asynchronous else Mock
        suffix = '_async' if asynchronous else ''
        response = {'items': []} if response is None else response
        with patch.object(module, 'request_looper' + suffix, mock_type(return_value=copy.deepcopy(response))) as looper, \
             patch.object(module, 'request_wrapper' + suffix, mock_type(return_value=copy.deepcopy(response))) as wrapper:
            result = function(*args, **(kwargs or {}))
            if asynchronous:
                result = asyncio.run(result)
            used = looper if looper.called else wrapper
            self.assertEqual(looper.call_count + wrapper.call_count, 1)
            return result, used.call_args


class PlaylistDatesTests(ContractTest):
    def test_period_and_existing_arguments(self):
        for asynchronous in (False, True):
            for args, expected in [(('uuid',), {'period': 30, 'endDate': None, 'offset': 0, 'limit': 100}),
                                   (('uuid', 60, '2026-01-10', 5, 20), {'period': 60, 'endDate': '2026-01-10', 'offset': 5, 'limit': 20})]:
                with self.subTest(asynchronous=asynchronous, args=args):
                    _, call = self.invoke('playlist', 'get_tracklisting_dates', args, asynchronous=asynchronous)
                    self.assertEqual(call.args[1], expected)
            with self.subTest(asynchronous=asynchronous, keyword=True):
                _, call = self.invoke('playlist', 'get_tracklisting_dates', ('uuid',), {'period': 90}, asynchronous)
                self.assertEqual(call.args[1]['period'], 90)
                with self.assertRaises(TypeError):
                    self.invoke('playlist', 'get_tracklisting_dates', ('uuid',), {'start_date': '2026-01-01'}, asynchronous)


class AlbumMetadataTests(ContractTest):
    def test_metadata_versions(self):
        cases = [('get_album_metadata', ('uuid',), 'by-uuid/uuid'),
                 ('get_album_by_upc', ('upc',), 'by-upc/upc'),
                 ('get_album_by_platform_id', ('spotify', 'id'), 'by-platform/spotify/id')]
        for asynchronous in (False, True):
            for method, args, path in cases:
                with self.subTest(asynchronous=asynchronous, method=method):
                    result, call = self.invoke('album', method, args, asynchronous=asynchronous, response={'name': 'album'})
                    self.assertEqual(call.args, ('/api/v2.51/album/' + path,))
                    self.assertEqual(result, {'name': 'album'})


class AlbumIdentifiersTests(ContractTest):
    def test_optional_boolean_preserves_false(self):
        for asynchronous in (False, True):
            for kwargs, expected in [({}, None), ({'only_default': None}, None),
                                     ({'only_default': False}, 'false'), ({'only_default': True}, 'true')]:
                with self.subTest(asynchronous=asynchronous, kwargs=kwargs):
                    _, call = self.invoke('album', 'get_ids', ('uuid', 'spotify', 4, 12), kwargs, asynchronous)
                    self.assertEqual(call.args[0], '/api/v2.26/album/uuid/identifiers')
                    params = call.args[1]
                    self.assertEqual(params.get('onlyDefault'), expected)
                    self.assertEqual({k: v for k, v in params.items() if k != 'onlyDefault'},
                                     {'platform': 'spotify', 'offset': 4, 'limit': 12})
                    if expected is not None:
                        self.assertIsInstance(params['onlyDefault'], str)


# None means the method preserves the API's order; booleans are its legacy
# local reverse-sort setting. Only endpoints documenting `sort` belong here.
SORT_METHODS = {
    'album': {'get_audience': None, 'get_popularity': None},
    'artist': {'get_soundcharts_score': None, 'get_local_audience': False,
               'get_streaming_audience': False, 'get_local_streaming_audience': False,
               'get_retention': False, 'get_popularity': False,
               'get_short_video_audience': True, 'get_playlist_reach': None},
    'playlist': {'get_audience': True},
    'radio': {'get_live_feed': True},
    'song': {'get_soundcharts_score': True, 'get_local_streaming_audience': True,
             'get_audience': True, 'get_popularity': True, 'get_radio_spins': False},
}


class SortTests(ContractTest):
    pass


def sort_test(module_name, method, asynchronous, legacy_reverse):
    def test(self):
        module = importlib.import_module('soundcharts.' + module_name)
        cls = getattr(module, module_name.title() + ('Async' if asynchronous else ''))
        function = getattr(cls, method)
        key = 'airedAt' if method in ('get_live_feed', 'get_radio_spins') else 'date'
        items = [{key: '2026-01-02'}, {key: '2026-01-01'}, {key: '2026-01-03'}]
        for kwargs in ({}, {'sort': None}, {'sort': 'asc'}, {'sort': 'desc'}):
            with self.subTest(kwargs=kwargs):
                sort = kwargs.get('sort')
                # An API-ordered response for pass-through methods, deliberately
                # shuffled data for methods that sort locally.
                supplied = items
                if legacy_reverse is None and sort is not None:
                    supplied = sorted(items, key=lambda item: item[key], reverse=sort == 'desc')
                result, call = self.invoke(module_name, method, ('uuid',), kwargs, asynchronous,
                                           {'items': supplied, 'total': 3})
                self.assertEqual(call.args[1].get('sort'), sort)
                expected = supplied if legacy_reverse is None else sorted(
                    items, key=lambda item: item[key],
                    reverse=legacy_reverse if sort is None else sort == 'desc')
                self.assertEqual(result, {'items': expected, 'total': 3})
        parameters = list(inspect.signature(function).parameters.values())
        self.assertEqual(parameters[-1].name, 'sort')
        self.assertIsNone(parameters[-1].default)
        # Existing arguments can still all be passed positionally.
        args = tuple('uuid' if p.default is inspect.Parameter.empty else p.default
                     for p in parameters[:-1])
        _, positional = self.invoke(module_name, method, args, {'sort': 'desc'}, asynchronous)
        _, keyword = self.invoke(module_name, method, (),
                                  dict(zip((p.name for p in parameters), args + ('desc',))), asynchronous)
        self.assertEqual(positional, keyword)
    return test


for _module, _methods in SORT_METHODS.items():
    for _method, _reverse in _methods.items():
        for _async in (False, True):
            setattr(SortTests, f'test_{_module}_{_method}_{"async" if _async else "sync"}',
                    sort_test(_module, _method, _async, _reverse))
