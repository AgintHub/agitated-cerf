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


class IdentifyPriceTrendsOutput(BaseModel):
    """Pydantic model for identify_price_trends node outputs."""
    trending_coins: List[str] = (
        Field(..., description="List of coin identifiers that are identified as price trending.")
    )
    trend_scores: List[float] = (
        Field(..., description="Numerical score representing the strength of the price trend for each coin.")
    )
    num_coins: int = (
        Field(..., description="Total number of coins identified as trending.")
    )


def identify_price_trends(preprocess_price_data_input: PreprocessPriceDataOutput, perform_statistical_analysis_input: PerformStatisticalAnalysisOutput, **kwargs) -> IdentifyPriceTrendsOutput:
    """
    Identify price‑driven trending coins using statistical analysis.

    Parameters
    ----------
    preprocessed_prices : Dict[str, List[float]]
        Dictionary mapping coin identifiers to their normalized price
        series. Keys are coin symbols (e.g., 'BTC', 'ETH'). Each list aligns
        with the global date index supplied by `preprocess_price_data`.
    analysis_results : Dict[str, Any]
        Output of `perform_statistical_analysis`, containing regression
        slopes, R² scores, and correlation coefficients for each feature
        against the price target. The node uses the regression slope and R²
        to quantify trend strength.

    Returns
    -------
    Tuple[List[str], List[float], int]
        A tuple containing (`trending_coins`, `trend_scores`, `num_coins`).
        `trending_coins` is ordered by descending `trend_scores`.

    Raises
    ------
    ValueError
        Raised if any input list is empty or if required keys are missing
        from the analysis results.
    TypeError
        Raised if input types do not match the expected signatures (e.g.,
        prices not numeric).

    Examples
    --------
    >>> preprocessed_prices = {
    ...     'BTC': [0.02, 0.025, 0.03, 0.035, 0.04],
    ...     'ETH': [0.015, 0.017, 0.016, 0.018, 0.02],
    ...     'USDT': [0.001, 0.0011, 0.0012, 0.0013, 0.0014]
    >>> }
    >>> analysis_results = {
    ...     'regression_slopes': [0.015, 0.005, 0.003],
    ...     'regression_r2_scores': [0.92, 0.35, 0.10],
    ...     'feature_names': ['BTC', 'ETH', 'USDT']
    >>> }
    (['BTC'], [0.015], 1)

    >>> preprocessed_prices = {
    ...     'BTC': [0.02, 0.021, 0.023, 0.026, 0.03],
    ...     'ETH': [0.015, 0.016, 0.0165, 0.017, 0.018]
    >>> }
    >>> analysis_results = {
    ...     'regression_slopes': [0.010, 0.004],
    ...     'regression_r2_scores': [0.85, 0.60],
    ...     'feature_names': ['BTC', 'ETH']
    >>> }
    (['BTC', 'ETH'], [0.010, 0.004], 2)

    """
    return IdentifyPriceTrendsOutput(
        trending_coins=[],
        trend_scores=[],
        num_coins=0,
    )