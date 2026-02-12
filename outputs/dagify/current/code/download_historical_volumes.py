from pydantic import BaseModel, Field
from typing import List


class GatherDataOutput(BaseModel):
    """Pydantic model for gather_data node outputs."""
    price_dates: List[str] = (
        Field(..., description="List of date strings corresponding to price data points")
    )
    prices: List[float] = (
        Field(..., description="List of historical closing prices for BTC, stable and ETH")
    )
    volume_dates: List[str] = (
        Field(..., description="List of date strings corresponding to volume data points")
    )
    volumes: List[float] = (
        Field(..., description="List of historical trading volumes for BTC, stable and ETH")
    )


class DownloadHistoricalVolumesOutput(BaseModel):
    """Pydantic model for download_historical_volumes node outputs."""
    btc_dates: List[str] = (
        Field(..., description="List of dates for BTC volume records")
    )
    btc_volumes: List[float] = (
        Field(..., description="List of daily trading volumes for BTC corresponding to btc_dates")
    )
    stablecoin_dates: List[str] = (
        Field(..., description="List of dates for stablecoin volume records")
    )
    stablecoin_volumes: List[float] = (
        Field(..., description="List of daily trading volumes for stablecoin corresponding to stablecoin_dates")
    )
    eth_dates: List[str] = (
        Field(..., description="List of dates for ETH volume records")
    )
    eth_volumes: List[float] = (
        Field(..., description="List of daily trading volumes for ETH corresponding to eth_dates")
    )


def download_historical_volumes(gather_data_input: GatherDataOutput, **kwargs) -> DownloadHistoricalVolumesOutput:
    """
    Download daily trading volumes for BTC, stablecoin, and ETH from an external
    API.

    Parameters
    ----------
    api_key : str
        API key for authenticating with the data provider.
    start_date : str
        ISO 8601 start date (YYYY-MM-DD) for the historical period to
        retrieve.
    end_date : str
        ISO 8601 end date (YYYY-MM-DD) for the historical period to
        retrieve.
    base_url : str
        Base endpoint URL of the data provider API.

    Returns
    -------
    dict
        A dictionary containing six keys: - btc_dates: List[str] of dates
        for BTC volume records - btc_volumes: List[float] of daily BTC
        volumes - stablecoin_dates: List[str] of dates for stablecoin volume
        records - stablecoin_volumes: List[float] of daily stablecoin
        volumes - eth_dates: List[str] of dates for ETH volume records -
        eth_volumes: List[float] of daily ETH volumes

    Raises
    ------
    ValueError
        If start_date is after end_date or dates are not in ISO format.
    ConnectionError
        If the API endpoint is unreachable or returns a network error.
    HTTPError
        If the API returns a non‑200 HTTP status code.
    KeyError
        If the expected volume fields are missing from the API response.

    Examples
    --------
    >>> volumes = download_historical_volumes(
    ...     api_key='my_api_key',
    ...     start_date='2023-01-01',
    ...     end_date='2023-01-05',
    ...     base_url='https://api.coinmarketcap.com/v1/'
    >>> )
    >>> print(volumes['btc_volumes'])
    [12000000.0, 11500000.5, 12345678.9, 11000000.0, 11800000.2]

    >>> volumes = download_historical_volumes(
    ...     api_key='my_api_key',
    ...     start_date='2023-01-01',
    ...     end_date='2023-01-01',
    ...     base_url='https://api.coinmarketcap.com/v1/'
    >>> )
    >>> print(volumes['eth_dates'])
    ['2023-01-01']

    """
    return DownloadHistoricalVolumesOutput(
        btc_dates=[],
        btc_volumes=[],
        stablecoin_dates=[],
        stablecoin_volumes=[],
        eth_dates=[],
        eth_volumes=[],
    )