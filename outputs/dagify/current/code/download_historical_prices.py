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


class DownloadHistoricalPricesOutput(BaseModel):
    """Pydantic model for download_historical_prices node outputs."""
    dates: List[str] = (
        Field(..., description="List of dates for which price data was retrieved, formatted as ISO 8601 strings")
    )
    prices_btc: List[float] = (
        Field(..., description="List of historical closing prices for BTC corresponding to each date")
    )
    prices_eth: List[float] = (
        Field(..., description="List of historical closing prices for ETH corresponding to each date")
    )
    prices_stable: List[float] = (
        Field(..., description="List of historical closing prices for stablecoin (e.g., USDT) corresponding to each date")
    )


def download_historical_prices(gather_data_input: GatherDataOutput, **kwargs) -> DownloadHistoricalPricesOutput:
    """
    Download historical price data for BTC, ETH, and a stablecoin from a public
    API.

    Parameters
    ----------
    api_key : str
        API key for the chosen data provider (e.g., CoinMarketCap).
    start_date : str
        ISO 8601 start date for the historical period (inclusive).
    end_date : str
        ISO 8601 end date for the historical period (inclusive).
    symbols : List[str]
        List of cryptocurrency symbols to query, e.g., ['BTC', 'ETH',
        'USDT'].

    Returns
    -------
    Dict[str, List[Union[str, float]]]
        A dictionary with keys 'dates', 'prices_btc', 'prices_eth', and
        'prices_stable', each mapping to a list of values aligned by index.
        The 'dates' list contains ISO 8601 date strings; the price lists
        contain the closing price in USD for the corresponding date.

    Raises
    ------
    ValueError
        If any of the input parameters are missing or empty.
    ConnectionError
        If the API endpoint cannot be reached.
    RuntimeError
        If the API returns an error status or malformed data.

    Examples
    --------
    >>> api_key = 'YOUR_CMC_API_KEY'
    >>> start_date = '2023-01-01'
    >>> end_date = '2023-01-10'
    >>> symbols = ['BTC', 'ETH', 'USDT']
    >>> prices = download_historical_prices(api_key, start_date, end_date,
    symbols)
    {
      'dates': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04',
    '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09',
    '2023-01-10'],
      'prices_btc': [32000.1, 32200.5, 31500.0, 33000.2, 33500.7, 34000.0,
    34500.3, 35000.6, 35500.1, 36000.4],
      'prices_eth': [2000.5, 2025.3, 1980.7, 2050.2, 2100.6, 2150.1, 2200.4,
    2250.8, 2300.3, 2350.7],
      'prices_stable': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    }

    >>> # If the API key is invalid or missing, the function raises ValueError
    >>> download_historical_prices('', '2023-01-01', '2023-01-10', ['BTC'])
    ValueError: API key must be provided.

    """
    return DownloadHistoricalPricesOutput(
        dates=[],
        prices_btc=[],
        prices_eth=[],
        prices_stable=[],
    )