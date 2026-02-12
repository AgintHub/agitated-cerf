from pydantic import BaseModel, Field
from typing import List


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


class CombineTrendingCoinsOutput(BaseModel):
    """Pydantic model for combine_trending_coins node outputs."""
    price_trend_coins: List[str] = (
        Field(..., description="List of price-driven trending coins identified from statistical price analysis")
    )
    volume_trend_coins: List[str] = (
        Field(..., description="List of volume-activated trending coins identified from transaction pattern analysis")
    )
    combined_coins: List[str] = (
        Field(..., description="Prioritized list of coins merged from price and volume trends based on composite scoring")
    )
    composite_scores: List[float] = (
        Field(..., description="Numerical composite scores corresponding to each coin in the combined list, reflecting weighted price-volume trend synergy")
    )


def combine_trending_coins(identify_price_trends_input: IdentifyPriceTrendsOutput, identify_volume_trends_input: IdentifyVolumeTrendsOutput, **kwargs) -> CombineTrendingCoinsOutput:
    """
    Merge price and volume-based trending coins into a weighted prioritized list

    Parameters
    ----------
    price_trend_coins : List[str]
        Coins identified by price analysis (output of identify_price_trends)
    price_trend_scores : List[float]
        Normalized price trend scores from identify_price_trends
    volume_trend_coins : List[str]
        Coins identified by volume analysis (output of
        identify_volume_trends)
    volume_trend_scores : List[float]
        Normalized volume scores from identify_volume_trends

    Returns
    -------
    Tuple[List[str], List[float], List[str], List[float]]
        Returns (price_trend_coins, volume_trend_coins, combined_coins,
        composite_scores) where combined_coins is sorted by composite_scores

    Raises
    ------
    ValueError
        If input lists contain duplicate coins or mismatched coin-score
        lengths
    AttributeError
        If parent nodes haven't completed their analysis

    Examples
    --------
    >>> combine_trending_coins(['ADA', 'DOGE'], [0.45],
    ...                 ['ADA', 'XMR'], [0.62, 0.77])
    {'price_trend_coins': ['ADA', 'DOGE'], 'volume_trend_coins': ['ADA', 'XMR'],
    'combined_coins': ['ADA', 'XMR', 'DOGE'], 'composite_scores': [0.535, 0.77,
    0.45]}

    """
    return CombineTrendingCoinsOutput(
        price_trend_coins=[],
        volume_trend_coins=[],
        combined_coins=[],
        composite_scores=[],
    )