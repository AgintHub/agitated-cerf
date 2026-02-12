from pydantic import BaseModel, Field
from typing import List


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


class PreprocessPriceDataOutput(BaseModel):
    """Pydantic model for preprocess_price_data node outputs."""
    dates: List[str] = (
        Field(..., description="List of dates corresponding to the price series in ISO format (YYYY-MM-DD).")
    )
    prices: List[float] = (
        Field(..., description="List of processed price values aligned with the dates list.")
    )
    missing_values_count: int = (
        Field(..., description="Number of missing price entries that were imputed.")
    )
    is_normalized: bool = (
        Field(..., description="Indicates whether the price series was normalized to a 0-1 range.")
    )


def preprocess_price_data(download_historical_prices_input: DownloadHistoricalPricesOutput, **kwargs) -> PreprocessPriceDataOutput:
    """
    Preprocesses raw historical price data for downstream analysis.

    Parameters
    ----------
    dates : List[str]
        List of ISO‑formatted dates (YYYY-MM-DD) for which price data was
        retrieved.
    prices_btc : List[float]
        List of closing prices for BTC aligned with the dates list.
    prices_eth : List[float]
        List of closing prices for ETH aligned with the dates list.
    prices_stable : List[float]
        List of closing prices for the chosen stablecoin (e.g., USDT)
        aligned with the dates list.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the cleaned and transformed price series,
        including dates, a unified price list, the count of imputed values,
        and a flag indicating whether normalization was performed.

    Raises
    ------
    ValueError
        If the input price lists are of unequal length or contain
        non‑numeric entries.
    TypeError
        If any input parameter is not of the expected type.

    Examples
    --------
    >>> # Example 1: Simple preprocessing with no missing values
    >>> output = preprocess_price_data(
    ...     dates=['2023-01-01', '2023-01-02'],
    ...     prices_btc=[20000.0, 21000.0],
    ...     prices_eth=[1200.0, 1250.0],
    ...     prices_stable=[1.0, 1.0]
    >>> )
    >>> print(output)
    {'dates': ['2023-01-01', '2023-01-02'], 'prices': [20000.0, 21000.0],
    'missing_values_count': 0, 'is_normalized': False}

    >>> # Example 2: Handling missing values and normalizing
    >>> output = preprocess_price_data(
    ...     dates=['2023-01-01', '2023-01-02', '2023-01-03'],
    ...     prices_btc=[20000.0, None, 21000.0],
    ...     prices_eth=[1200.0, 1250.0, None],
    ...     prices_stable=[1.0, 1.0, 1.0]
    >>> )
    >>> print(output)
    {'dates': ['2023-01-01', '2023-01-02', '2023-01-03'], 'prices': [20000.0,
    20000.0, 21000.0], 'missing_values_count': 2, 'is_normalized': True}

    """
    return PreprocessPriceDataOutput(
        dates=[],
        prices=[],
        missing_values_count=0,
        is_normalized=False,
    )