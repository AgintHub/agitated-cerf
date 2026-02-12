from pydantic import BaseModel, Field
from typing import List


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


class PreprocessVolumeDataOutput(BaseModel):
    """Pydantic model for preprocess_volume_data node outputs."""
    dates: List[str] = (
        Field(..., description="List of dates corresponding to each volume entry.")
    )
    raw_volumes: List[float] = (
        Field(..., description="Original volume values after missing value handling.")
    )
    normalized_volumes: List[float] = (
        Field(..., description="Volume values scaled to a 0-1 range or standardized to mean 0 and std 1.")
    )
    missing_value_count: int = (
        Field(..., description="Number of missing volume entries that were imputed or removed.")
    )
    is_valid: bool = (
        Field(..., description="Indicates whether the preprocessing produced a dataset suitable for analysis.")
    )


def preprocess_volume_data(download_historical_volumes_input: DownloadHistoricalVolumesOutput, **kwargs) -> PreprocessVolumeDataOutput:
    """
    Preprocesses historical cryptocurrency volume data by handling missing
    values and normalizing the series.

    Parameters
    ----------
    btc_dates : List[str]
        ISO 8601 formatted dates for BTC volume records.
    btc_volumes : List[float]
        Daily trading volumes for BTC aligned with btc_dates.
    stablecoin_dates : List[str]
        ISO 8601 formatted dates for stablecoin volume records.
    stablecoin_volumes : List[float]
        Daily trading volumes for stablecoins aligned with stablecoin_dates.
    eth_dates : List[str]
        ISO 8601 formatted dates for ETH volume records.
    eth_volumes : List[float]
        Daily trading volumes for ETH aligned with eth_dates.
    normalization_method : str
        Method used for scaling volumes: 'minmax' for 0-1 scaling or
        'standard' for mean‑zero/std‑one standardization.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing cleaned dates, raw volumes, normalized
        volumes, missing value count, and a validity flag.

    Raises
    ------
    ValueError
        If any of the date lists are empty or lengths of dates and volumes
        do not match.
    TypeError
        If volume inputs contain non‑numeric values.

    Examples
    --------
    >>> result = preprocess_volume_data(
    ...     btc_dates=['2023-01-01', '2023-01-02'],
    ...     btc_volumes=[1000.0, 1100.0],
    ...     stablecoin_dates=['2023-01-01', '2023-01-02'],
    ...     stablecoin_volumes=[2000.0, 2100.0],
    ...     eth_dates=['2023-01-01', '2023-01-02'],
    ...     eth_volumes=[1500.0, 1600.0],
    ...     normalization_method='minmax')
    {'dates': ['2023-01-01', '2023-01-02'], 'raw_volumes': [1000.0, 1100.0,
    2000.0, 2100.0, 1500.0, 1600.0], 'normalized_volumes': [0.0, 0.1, 0.7, 0.8,
    0.4, 0.5], 'missing_value_count': 0, 'is_valid': True}

    >>> result = preprocess_volume_data(
    ...     btc_dates=['2023-01-01', None],
    ...     btc_volumes=[1000.0, None],
    ...     stablecoin_dates=['2023-01-01'],
    ...     stablecoin_volumes=[2000.0],
    ...     eth_dates=['2023-01-01'],
    ...     eth_volumes=[1500.0],
    ...     normalization_method='standard')
    {'dates': ['2023-01-01'], 'raw_volumes': [1000.0, 2000.0, 1500.0],
    'normalized_volumes': [-1.0, 1.0, 0.0], 'missing_value_count': 2,
    'is_valid': True}

    """
    return PreprocessVolumeDataOutput(
        dates=[],
        raw_volumes=[],
        normalized_volumes=[],
        missing_value_count=0,
        is_valid=False,
    )