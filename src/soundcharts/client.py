import importlib.util
import logging
from .api_util import setup as api_setup
from .search import Search
from .artist import Artist
from .song import Song
from .album import Album
from .charts import Charts
from .playlist import Playlist
from .radio import Radio
from .festival import Festival
from .venue import Venue
from .tiktok import Tiktok
from .user import User
from .mylibrary import MyLibrary
from .referential import Referential


class SoundchartsClient:
    """
    Main client for interacting with the Soundcharts API.
    """

    def __init__(
        self,
        app_id,
        api_key,
        base_url="https://customer.api.soundcharts.com",
        max_retries=5,
        retry_delay=10,
        console_log_level=logging.INFO,
        file_log_level=logging.WARNING,
        exception_log_level=logging.ERROR,
    ):
        """
        Initialize the Soundcharts client. Use the logging python library to specify the logging level.
        Logging levels : DEBUG, INFO, WARNING, ERROR, CRITICAL.

        :param app_id: Soundcharts App ID
        :param api_key: Soundcharts API Key
        :param base_url: Base URL for API. Default: production.
        :param max_retries: Max number of retries in case of an error 500. Default: 5.
        :param retry_delay: Time in seconds between retries for a 500 error. Default: 10.
        :param console_log_level: The severity of issues written to the console. Default: logging.INFO.
        :param file_log_level: The severity of issues written to the logging file. Default: logging.WARNING.
        :param exception_log_level: The severity of issues that cause exceptions. Default: logging.ERROR.
        """

        api_setup(
            app_id,
            api_key,
            base_url,
            max_retries,
            retry_delay,
            console_log_level,
            file_log_level,
            exception_log_level,
        )

        # Initialize submodules
        self.search = Search()
        self.artist = Artist()
        self.song = Song()
        self.album = Album()
        self.charts = Charts()
        self.playlist = Playlist()
        self.radio = Radio()
        self.festival = Festival()
        self.venue = Venue()
        self.tiktok = Tiktok()
        self.user = User()
        self.mylibrary = MyLibrary()
        self.referential = Referential()

        # Conditionally import 'test' submodule if test.py exists
        try:
            test_module = importlib.import_module("soundcharts.test")
            self.test = test_module.Test()
        except ModuleNotFoundError:
            self.test = None

        # Conditionally import 'deprecated' submodule if deprecated.py exists
        try:
            test_module = importlib.import_module("soundcharts.deprecated")
            self.deprecated = test_module.Deprecated()
        except ModuleNotFoundError:
            self.deprecated = None

    def __repr__(self):
        return f"SoundchartsClient(base_url={self.base_url})"
