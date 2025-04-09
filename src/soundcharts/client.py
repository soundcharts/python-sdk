import importlib.util
from .api_util import setup as api_setup
from .search import Search
from .artist import Artist
from .song import Song
from .album import Album
from .charts import Charts
from .playlist import Playlist
from .radio import Radio
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
        log_errors=True,
        max_retries=5,
        retry_delay=10,
    ):
        """
        Initialize the Soundcharts client.

        :param app_id: App ID for authenticating requests.
        :param api_key: API key, or token, for authenticating requests.
        :param base_url: Base URL for the API. Defaults to the production API URL.
        :param log_errors: Decide whether or not to log errors. Default: True
        :param max_retries: Max number of retries in case of an error 500 (default: 5).
        :param retry_delay: Time in seconds between retries for a 500 error (default: 10).
        """

        api_setup(app_id, api_key, base_url, log_errors, max_retries, retry_delay)

        # Initialize submodules
        self.search = Search()
        self.artist = Artist()
        self.song = Song()
        self.album = Album()
        self.charts = Charts()
        self.playlist = Playlist()
        self.radio = Radio()
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
