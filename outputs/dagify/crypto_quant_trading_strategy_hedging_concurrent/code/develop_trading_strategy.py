from pydantic import BaseModel, Field
from typing import List


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


class DevelopTradingStrategyOutput(BaseModel):
    """Pydantic model for develop_trading_strategy node outputs."""
    strategy_name: str = (
        Field(..., description="Name of the developed trading strategy")
    )
    coin_list: List[str] = (
        Field(..., description="List of coin symbols included in the strategy")
    )
    buy_threshold: float = (
        Field(..., description="Threshold value used to trigger a buy signal")
    )
    sell_threshold: float = (
        Field(..., description="Threshold value used to trigger a sell signal")
    )
    max_drawdown: float = (
        Field(..., description="Maximum acceptable drawdown percentage for the strategy")
    )
    risk_per_trade: float = (
        Field(..., description="Percentage of capital risked per trade")
    )


def develop_trading_strategy(combine_trending_coins_input: CombineTrendingCoinsOutput, **kwargs) -> DevelopTradingStrategyOutput:
    """
    Generates a parameterized trading strategy from composite coin trend data

    Parameters
    ----------
    combined_coins : List[str]
        Prioritized list of price-volume synergized coins from
        combine_trending_coins
    composite_scores : List[float]
        Weighted scores reflecting price-volume trend synergy for each coin

    Returns
    -------
    Dict[str, Any]
        Trading strategy configuration with explicit thresholds, risk
        parameters, and coin selections

    Raises
    ------
    ValueError
        If combined_coins has fewer than 3 valid coin entries
    ValueError
        If composite_scores length does not match combined_coins

    Examples
    --------
    >>> develop_trading_strategy(['BTC', 'ETH'], [0.85, 0.72])
    >>> {'strategy_name': 'TrendArb-2024', 'max_drawdown': 15.5}
    {'strategy_name': 'TrendArb-2024', 'coin_list': ['BTC', 'ETH'],
    'buy_threshold': 0.05, 'sell_threshold': 0.10, 'max_drawdown': 15.5,
    'risk_per_trade': 2.0}

    >>> develop_trading_strategy(['ADA'], [0.67])
    >>> ValueError: combined_coins requires at least 3 valid entries
    ValueError: combined_coins requires at least 3 valid entries

    """
    return DevelopTradingStrategyOutput(
        strategy_name="",
        coin_list=[],
        buy_threshold=0.0,
        sell_threshold=0.0,
        max_drawdown=0.0,
        risk_per_trade=0.0,
    )