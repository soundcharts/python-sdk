import importlib.util
import logging
from .api_util import setup as api_setup
from .search import Search, SearchAsync
from .artist import Artist, ArtistAsync
from .song import Song, SongAsync
from .album import Album, AlbumAsync
from .charts import Charts, ChartsAsync
from .playlist import Playlist, PlaylistAsync
from .radio import Radio, RadioAsync
from .festival import Festival, FestivalAsync
from .venue import Venue, VenueAsync
from .tiktok import Tiktok, TiktokAsync
from .user import User, UserAsync
from .mylibrary import MyLibrary, MyLibraryAsync
from .referential import Referential, ReferentialAsync
from .publisher import Publisher, PublisherAsync
from .work import Work, WorkAsync


class SoundchartsClient:
    """
    Main client for interacting with the Soundcharts API.
    """

    def __init__(
        self,
        app_id,
        api_key,
        base_url="https://customer.api.soundcharts.com",
        parallel_requests=5,
        max_retries=5,
        retry_delay=10,
        timeout=10,
        console_log_level=logging.WARNING,
        file_log_level=logging.WARNING,
        exception_log_level=logging.ERROR,
    ):
        """
        Initialize the Soundcharts client. Use the logging python library to specify the logging level.
        Logging levels : DEBUG, INFO, WARNING, ERROR, CRITICAL.

        :param app_id: Soundcharts App ID
        :param api_key: Soundcharts API Key
        :param base_url: Base URL for API. Default: production.
        :param parallel_requests: How many queries can run in parallel. Default: 5.
        :param max_retries: Max number of retries in case of an error 500. Default: 5.
        :param retry_delay: Time in seconds between retries for a 500 error. Default: 10.
        :param console_log_level: The severity of issues written to the console. Default: logging.WARNING.
        :param file_log_level: The severity of issues written to the logging file. Default: logging.WARNING.
        :param exception_log_level: The severity of issues that cause exceptions. Default: logging.ERROR.
        """
        self.base_url = base_url

        api_setup(
            app_id,
            api_key,
            base_url,
            parallel_requests,
            max_retries,
            retry_delay,
            timeout,
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
        self.publisher = Publisher()
        self.work = Work()

        # Conditionally import 'test' submodule if test.py exists
        try:
            test_module = importlib.import_module("soundcharts.test")
            self.test = test_module.Test()
        except ModuleNotFoundError:
            self.test = None

    def __repr__(self):
        return f"SoundchartsClient(base_url={self.base_url})"


class SoundchartsClientAsync:
    """
    Main client for interacting with the Soundcharts API.
    """

    def __init__(
        self,
        app_id,
        api_key,
        base_url="https://customer.api.soundcharts.com",
        parallel_requests=5,
        max_retries=5,
        retry_delay=10,
        timeout=10,
        console_log_level=logging.WARNING,
        file_log_level=logging.WARNING,
        exception_log_level=logging.ERROR,
    ):
        """
        Initialize the Soundcharts client. Use the logging python library to specify the logging level.
        Logging levels : DEBUG, INFO, WARNING, ERROR, CRITICAL.

        :param app_id: Soundcharts App ID
        :param api_key: Soundcharts API Key
        :param base_url: Base URL for API. Default: production.
        :param parallel_requests: How many queries can run in parallel. Default: 5.
        :param max_retries: Max number of retries in case of an error 500. Default: 5.
        :param retry_delay: Time in seconds between retries for a 500 error. Default: 10.
        :param console_log_level: The severity of issues written to the console. Default: logging.WARNING.
        :param file_log_level: The severity of issues written to the logging file. Default: logging.WARNING.
        :param exception_log_level: The severity of issues that cause exceptions. Default: logging.ERROR.
        """

        self.base_url = base_url

        api_setup(
            app_id,
            api_key,
            base_url,
            parallel_requests,
            max_retries,
            retry_delay,
            timeout,
            console_log_level,
            file_log_level,
            exception_log_level,
        )

        # Initialize submodules
        self.search = SearchAsync()
        self.artist = ArtistAsync()
        self.song = SongAsync()
        self.album = AlbumAsync()
        self.charts = ChartsAsync()
        self.playlist = PlaylistAsync()
        self.radio = RadioAsync()
        self.festival = FestivalAsync()
        self.venue = VenueAsync()
        self.tiktok = TiktokAsync()
        self.user = UserAsync()
        self.mylibrary = MyLibraryAsync()
        self.referential = ReferentialAsync()
        self.publisher = PublisherAsync()
        self.work = WorkAsync()

        # Conditionally import 'test' submodule if test.py exists
        try:
            test_module = importlib.import_module("soundcharts.test")
            self.test = test_module.TestAsync()
        except ModuleNotFoundError:
            self.test = None

    def __repr__(self):
        return f"SoundchartsClientAsync(base_url={self.base_url})"
