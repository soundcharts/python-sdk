import importlib.util
import logging
from .api_util import setup as api_setup
from .album import Album, AlbumAsync
from .artist import Artist, ArtistAsync
from .charts import Charts, ChartsAsync
from .collaborator import Collaborator, CollaboratorAsync
from .datafeed import DataFeed, DataFeedAsync
from .distributor import Distributor, DistributorAsync
from .favorite import Favorite, FavoriteAsync
from .festival import Festival, FestivalAsync
from .label import Label, LabelAsync
from .playlist import Playlist, PlaylistAsync
from .publisher import Publisher, PublisherAsync
from .radio import Radio, RadioAsync
from .referential import Referential, ReferentialAsync
from .search import Search, SearchAsync
from .song import Song, SongAsync
from .usage_quotas import UsageQuotas, UsageQuotasAsync
from .venue import Venue, VenueAsync
from .work import Work, WorkAsync


class SoundchartsClient:
    """
    Main client for interacting with the Soundcharts API.
    """

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        team_id=None,
        base_url="https://customer.api.soundcharts.com",
        auth_url="https://account.soundcharts.com",
        app_id=None,
        api_key=None,
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

        Provide either (client_id, client_secret) for OAuth 2.1 or (app_id, api_key) for legacy auth.
        """
        self.base_url = base_url

        if not ((app_id and api_key) or (client_id and client_secret)):
            raise ValueError(
                "SDK configuration invalid: Provide either OAuth credentials or legacy API keys."
            )

        api_setup(
            app_id=app_id,
            api_key=api_key,
            client_id=client_id,
            client_secret=client_secret,
            team_id=team_id,
            base_url=base_url,
            auth_url=auth_url,
            parallel_requests=parallel_requests,
            max_retries=max_retries,
            retry_delay=retry_delay,
            timeout=timeout,
            console_log_level=console_log_level,
            file_log_level=file_log_level,
            exception_log_level=exception_log_level,
        )

        # Initialize submodules
        self.album = Album()
        self.artist = Artist()
        self.charts = Charts()
        self.collaborator = Collaborator()
        self.data_feed = DataFeed()
        self.distributor = Distributor()
        self.favorite = Favorite()
        self.festival = Festival()
        self.label = Label()
        self.playlist = Playlist()
        self.publisher = Publisher()
        self.radio = Radio()
        self.referential = Referential()
        self.search = Search()
        self.song = Song()
        self.usage_quotas = UsageQuotas()
        self.venue = Venue()
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
    Main async client for interacting with the Soundcharts API.
    """

    def __init__(
        self,
        app_id=None,
        api_key=None,
        client_id=None,
        client_secret=None,
        team_id=None,
        base_url="https://customer.api.soundcharts.com",
        auth_url="https://account.soundcharts.com",
        parallel_requests=5,
        max_retries=5,
        retry_delay=10,
        timeout=10,
        console_log_level=logging.WARNING,
        file_log_level=logging.WARNING,
        exception_log_level=logging.ERROR,
    ):
        """
        Initialize the Soundcharts client.
        Provide either (client_id, client_secret) for OAuth 2.1 or (app_id, api_key) for legacy auth.
        """
        self.base_url = base_url

        if not ((app_id and api_key) or (client_id and client_secret)):
            raise ValueError(
                "SDK configuration invalid: Provide either OAuth credentials or legacy API keys."
            )

        api_setup(
            app_id=app_id,
            api_key=api_key,
            client_id=client_id,
            client_secret=client_secret,
            team_id=team_id,
            base_url=base_url,
            auth_url=auth_url,
            parallel_requests=parallel_requests,
            max_retries=max_retries,
            retry_delay=retry_delay,
            timeout=timeout,
            console_log_level=console_log_level,
            file_log_level=file_log_level,
            exception_log_level=exception_log_level,
        )

        # Initialize submodules
        self.album = AlbumAsync()
        self.artist = ArtistAsync()
        self.charts = ChartsAsync()
        self.collaborator = CollaboratorAsync()
        self.datafeed = DataFeedAsync()
        self.distributor = DistributorAsync()
        self.favorite = FavoriteAsync()
        self.festival = FestivalAsync()
        self.label = LabelAsync()
        self.playlist = PlaylistAsync()
        self.publisher = PublisherAsync()
        self.radio = RadioAsync()
        self.referential = ReferentialAsync()
        self.search = SearchAsync()
        self.song = SongAsync()
        self.usage_quotas = UsageQuotasAsync()
        self.venue = VenueAsync()
        self.work = WorkAsync()

        # Conditionally import 'test' submodule if test.py exists
        try:
            test_module = importlib.import_module("soundcharts.test")
            self.test = test_module.TestAsync()
        except ModuleNotFoundError:
            self.test = None

    def __repr__(self):
        return f"SoundchartsClientAsync(base_url={self.base_url})"
