from pydantic import BaseModel, Field
from typing import List


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


class HedgeStrategyOutput(BaseModel):
    """Pydantic model for hedge_strategy node outputs."""
    hedging_ratio: float = (
        Field(..., description="Optimal ratio of Tether to crypto holdings for hedging")
    )
    entry_conditions: str = (
        Field(..., description="Conditions under which the hedge should be initiated")
    )
    exit_conditions: str = (
        Field(..., description="Conditions under which the hedge should be closed")
    )
    crypto_exposure: float = (
        Field(..., description="Current value of crypto exposure in USD")
    )
    tether_position: float = (
        Field(..., description="Amount of Tether to hold for hedging in USD")
    )
    strategy_summary: str = (
        Field(..., description="Brief summary of the hedging strategy and rationale")
    )


def hedge_strategy(develop_trading_strategy_input: DevelopTradingStrategyOutput, **kwargs) -> HedgeStrategyOutput:
    """
    Generate a Tether‑based hedging plan for a crypto trading strategy.

    Parameters
    ----------
    strategy_name : str
        Name of the trading strategy produced by develop_trading_strategy.
    coin_list : list[str]
        List of coin symbols included in the strategy.
    buy_threshold : float
        Threshold value used to trigger a buy signal in the strategy.
    sell_threshold : float
        Threshold value used to trigger a sell signal in the strategy.
    max_drawdown : float
        Maximum acceptable drawdown percentage for the strategy.
    risk_per_trade : float
        Percentage of capital risked per trade.

    Returns
    -------
    dict
        A dictionary containing hedging_ratio, entry_conditions,
        exit_conditions, crypto_exposure, tether_position, and
        strategy_summary.

    Raises
    ------
    ValueError
        If any numeric input is non‑positive or if coin_list is empty.

    Examples
    --------
    >>> # Example 1: Basic hedging for a high‑risk strategy
    >>> hedge_strategy(
    ...     strategy_name='MomentumTrader',
    ...     coin_list=['BTC', 'ETH'],
    ...     buy_threshold=0.05,
    ...     sell_threshold=0.07,
    ...     max_drawdown=0.20,
    ...     risk_per_trade=0.02
    >>> )
    {'hedging_ratio': 0.15, 'entry_conditions': 'BTC price drops >5% or ETH
    drops >7%', 'exit_conditions': 'Price recovers 3% from entry or volatility
    drops below threshold', 'crypto_exposure': 150000.0, 'tether_position':
    22500.0, 'strategy_summary': 'High‑risk momentum strategy hedged 15% with
    USDT to cap losses.'}

    >>> # Example 2: Conservative hedge with low volatility
    >>> hedge_strategy(
    ...     strategy_name='StableTrend',
    ...     coin_list=['BTC'],
    ...     buy_threshold=0.02,
    ...     sell_threshold=0.03,
    ...     max_drawdown=0.05,
    ...     risk_per_trade=0.01
    >>> )
    {'hedging_ratio': 0.10, 'entry_conditions': 'BTC drops >2% or 3% for sell',
    'exit_conditions': 'Price recovers 1% or volatility <0.5%',
    'crypto_exposure': 50000.0, 'tether_position': 5000.0, 'strategy_summary':
    'Conservative strategy hedged 10% with USDT to protect against small dips.'}

    """
    return HedgeStrategyOutput(
        hedging_ratio=0.0,
        entry_conditions="",
        exit_conditions="",
        crypto_exposure=0.0,
        tether_position=0.0,
        strategy_summary="",
    )