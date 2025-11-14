# Soundcharts Module

A Python package for interacting with the Soundcharts API.

## API Documentation

Full documentation of the API is available here: [Soundcharts API Documentation](https://developers.soundcharts.com/documentation/getting-started)

You will need a Soundcharts API subscription to use this package.

## Features

- Easily pull data from Soundcharts' API.
- Every endpoint from the documentation is available as a Python function.
  - For example, the "get audience" endpoint in the "playlist" category is accessible via `playlist.get_audience()`.
- Automatically loops through endpoints to get around API limitations, such as the limit of 100 items per request.
- Configurable error handling.

## Installation

`pip install soundcharts`

## Usage

```python
from soundcharts.client import SoundchartsClient

sc = SoundchartsClient(app_id="your_app_id", api_key="your_api_key")

# Example with Billie Eilish's UUID
billie_metadata = sc.artist.get_artist_metadata("11e81bcc-9c1c-ce38-b96b-a0369fe50396")
print(billie_metadata)
```

## Error handling

You can set the severity of the console logs, file logs, and exceptions:

```python
from soundcharts.client import SoundchartsClient
import logging

sc = SoundchartsClient( app_id="your_app_id",
                        api_key="your_api_key",
                        console_log_level=logging.INFO,
                        file_log_level=logging.WARNING,
                        exception_log_level=logging.ERROR)
```

Setting the level of the console or file log to `logging.DEBUG` will log each request send to the API.

## Parallel processing

You can specify the number of requests to run in parallel. 
It's especially useful when looping through a lot of calls, like in this case fetching 3 months of Billie Eilish's radio airplay (about 3,000 calls):

```python
from soundcharts.client import SoundchartsClient
import logging

sc = SoundchartsClient( app_id="your_app_id",
                        api_key="your_api_key",
                        parallel_requests=10)

billie = "11e81bcc-9c1c-ce38-b96b-a0369fe50396"

response = sc.artist.get_radio_spins(
    billie, start_date="2025-01-01", end_date="2025-03-31", limit=None
)
```