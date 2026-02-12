from pydantic import BaseModel, Field
from typing import List


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


class IdentifyVolumeTrendsOutput(BaseModel):
    """Pydantic model for identify_volume_trends node outputs."""
    trending_coin_symbols: List[str] = (
        Field(..., description="List of cryptocurrency symbols identified as high-volume trending.")
    )
    volume_scores: List[float] = (
        Field(..., description="Numerical volume-based score for each trending coin, reflecting relative trading activity.")
    )
    volume_thresholds: List[float] = (
        Field(..., description="Volume threshold values used to determine if a coin qualifies as trending.")
    )


def identify_volume_trends(preprocess_volume_data_input: PreprocessVolumeDataOutput, perform_statistical_analysis_input: PerformStatisticalAnalysisOutput, **kwargs) -> IdentifyVolumeTrendsOutput:
    """
    Identify volume-activated trending coins based on preprocessed volume data
    and statistical analysis.

    Parameters
    ----------
    volume_data : dict
        Output from preprocess_volume_data containing normalized volume
        series and related metadata.
    analysis_results : dict
        Output from perform_statistical_analysis containing correlation
        coefficients, regression slopes, etc.

    Returns
    -------
    dict
        Dictionary with keys: - trending_coin_symbols (List[str]) -
        volume_scores (List[float]) - volume_thresholds (List[float])

    Raises
    ------
    ValueError
        Raised when volume_data or analysis_results are missing required
        fields or contain inconsistent lengths.

    Examples
    --------
    >>> result = identify_volume_trends(
    ...     volume_data={
    ...         'normalized_volumes': [120.0, 150.0, 80.0],
    ...         'dates': ['2024-01-01', '2024-01-02', '2024-01-03']
    ...     },
    ...     analysis_results={
    ...         'correlation_coefficients': [0.92, 0.88, 0.45],
    ...         'feature_names': ['volume', 'price']
    ...     }
    >>> )
    {
      "trending_coin_symbols": ["BTC", "ETH"],
      "volume_scores": [0.92, 0.88],
      "volume_thresholds": [100.0, 130.0]
    }

    >>> result = identify_volume_trends(
    ...     volume_data={
    ...         'normalized_volumes': [200.0, 210.0],
    ...         'dates': ['2024-01-01', '2024-01-02']
    ...     },
    ...     analysis_results={
    ...         'correlation_coefficients': [0.95, 0.93],
    ...         'feature_names': ['volume', 'price']
    ...     }
    >>> )
    {
      "trending_coin_symbols": ["BTC"],
      "volume_scores": [0.95],
      "volume_thresholds": [190.0]
    }

    """
    return IdentifyVolumeTrendsOutput(
        trending_coin_symbols=[],
        volume_scores=[],
        volume_thresholds=[],
    )