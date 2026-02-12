from pydantic import BaseModel, Field
from typing import List


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


class PerformStatisticalAnalysisOutput(BaseModel):
    """Pydantic model for perform_statistical_analysis node outputs."""
    feature_names: List[str] = (
        Field(..., description="Names of the features used in the analysis")
    )
    correlation_coefficients: List[float] = (
        Field(..., description="Pearson correlation coefficients between each pair of features")
    )
    regression_slopes: List[float] = (
        Field(..., description="Slope coefficients from linear regressions for each feature against the target variable")
    )
    regression_intercepts: List[float] = (
        Field(..., description="Intercept terms from linear regressions for each feature")
    )
    regression_r2_scores: List[float] = (
        Field(..., description="Coefficient of determination (R^2) for each regression model")
    )
    regression_p_values: List[float] = (
        Field(..., description="p-values for the slope coefficients in each regression model")
    )
    analysis_summary: str = (
        Field(..., description="Concise textual summary of the key statistical findings")
    )


def perform_statistical_analysis(preprocess_price_data_input: PreprocessPriceDataOutput, preprocess_volume_data_input: PreprocessVolumeDataOutput, **kwargs) -> PerformStatisticalAnalysisOutput:
    """
    Perform regression and correlation analyses on cleaned price and volume
    datasets to extract statistical metrics for trend detection.

    Parameters
    ----------
    price_data : dict
        Dictionary returned by `preprocess_price_data`, containing keys
        `dates`, `prices`, `missing_values_count`, and `is_normalized`.
    volume_data : dict
        Dictionary returned by `preprocess_volume_data`, containing keys
        `dates`, `raw_volumes`, `normalized_volumes`, `missing_value_count`,
        and `is_valid`.
    target_feature : str
        Name of the feature to predict (default: `'prices'`). It must exist
        in `price_data`.

    Returns
    -------
    dict
        A dictionary mapping the output field names to their computed
        values, matching the node's output_structure.

    Raises
    ------
    ValueError
        If `price_data` or `volume_data` is missing required keys, or if
        `target_feature` is not present.
    RuntimeError
        If regression or correlation calculation fails due to insufficient
        data.

    Examples
    --------
    >>> # Mock preprocessed price data
    >>> price_data = {
    ...     'dates': ['2024-01-01', '2024-01-02', '2024-01-03'],
    ...     'prices': [100.0, 102.5, 101.0],
    ...     'missing_values_count': 0,
    ...     'is_normalized': True
    >>> }
    >>> # Mock preprocessed volume data
    >>> volume_data = {
    ...     'dates': ['2024-01-01', '2024-01-02', '2024-01-03'],
    ...     'raw_volumes': [5000, 5200, 5100],
    ...     'normalized_volumes': [0.0, 0.2, 0.1],
    ...     'missing_value_count': 0,
    ...     'is_valid': True
    >>> }
    {feature_names: [prices, normalized_volumes], correlation_coefficients:
    [0.98], regression_slopes: [2.5, -0.5], regression_intercepts: [50.0, 1.0],
    regression_r2_scores: [0.97, 0.9], regression_p_values: [0.001, 0.05],
    analysis_summary: Strong positive correlation between price and volume;
    price increases with volume.}

    >>> # Using default target feature
    >>> result = perform_statistical_analysis(price_data, volume_data)
    >>> print(result['analysis_summary'])
    "Strong positive correlation between price and volume; price increases with
    volume."

    """
    return PerformStatisticalAnalysisOutput(
        feature_names=[],
        correlation_coefficients=[],
        regression_slopes=[],
        regression_intercepts=[],
        regression_r2_scores=[],
        regression_p_values=[],
        analysis_summary="",
    )