<<<<<<< HEAD
# Soundcharts Module

A Python package for interacting with the Soundcharts API.

## API Documentation

Full documentation of the API is available here: [Soundcharts API Documentation](https://doc.api.soundcharts.com/api/v2/doc)

You will need a Soundcharts API subscription to use this package.

## Features

- Easily pull data from Soundcharts' API.
- Every endpoint from the documentation is available as a Python function.
  - For example, the "get audience" endpoint in the "playlist" category is accessible via `playlist.get_audience()`.
- Automatically loops through endpoints to get around API limitations, such as:
  - Periods of 90 days max.
  - Limits of 100 items per request.

## Installation

`pip install soundcharts`

## Usage

```python
from soundcharts.client import SoundchartsClient

sc = SoundchartsClient(app_id="your_app_id", api_key="your_api_key")

# Example with Billie Eilish's UUID 
billie_metadata = sc.artist.get_artist_metadata("11e81bcc-9c1c-ce38-b96b-a0369fe50396")
print(billie_metadata)
=======
# Soundcharts Module

A Python package for interacting with the Soundcharts API.

## API Documentation

Full documentation of the API is available here: [Soundcharts API Documentation](https://doc.api.soundcharts.com/api/v2/doc)

You will need a Soundcharts API subscription to use this package.

## Features

- Easily pull data from Soundcharts' API.
- Every endpoint from the documentation is available as a Python function.
  - For example, the "get audience" endpoint in the "playlist" category is accessible via `playlist.get_audience()`.
- Automatically loops through endpoints to get around API limitations, such as:
  - Periods of 90 days max.
  - Limits of 100 items per request.

## Installation

Clone this repository and include the `soundcharts` folder in your Python path.

## Usage

```python
from soundcharts.client import SoundchartsClient

sc = SoundchartsClient(app_id="your_app_id", api_key="your_api_key")

# Example with Billie Eilish's UUID 
billie_metadata = sc.artist.get_artist_metadata("11e81bcc-9c1c-ce38-b96b-a0369fe50396")
print(billie_metadata)
>>>>>>> 7fa8413 (Added setup.py)
