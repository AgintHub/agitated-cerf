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


class BacktestStrategyOutput(BaseModel):
    """Pydantic model for backtest_strategy node outputs."""
    cagr: float = (
        Field(..., description="Compound Annual Growth Rate of the strategy")
    )
    sharpe_ratio: float = (
        Field(..., description="Sharpe Ratio of the strategy's returns")
    )
    max_drawdown: float = (
        Field(..., description="Maximum Drawdown percentage during the backtest period")
    )
    total_trades: int = (
        Field(..., description="Total number of executed trades in the backtest")
    )
    net_profit: float = (
        Field(..., description="Net profit (or loss) in the strategy's base currency")
    )


def backtest_strategy(develop_trading_strategy_input: DevelopTradingStrategyOutput, **kwargs) -> BacktestStrategyOutput:
    """
    Executes a backtest of the defined trading strategy using historical market
    data, calculating CAGR, Sharpe Ratio, and drawdown metrics to assess
    performance.

    Parameters
    ----------
    strategy_config : dict
        Trading strategy configuration containing parameters like coin_list,
        buy_threshold, sell_threshold, and max_drawdown from
        develop_trading_strategy
    historical_prices : dict
        Processed price history for BTC, ETH, and stablecoins formatted as
        {dates, prices_btc, prices_eth, prices_stable}
    historical_volumes : dict
        Volume data for market activity including BTC, ETH, and stablecoin
        volumes over time

    Returns
    -------
    dict[str, float | int]
        Performance metrics including compound annual growth rate, risk-
        adjusted return ratio, maximum capital loss, total trade count, and
        net profitability

    Raises
    ------
    ValueError
        If historical data timelines don't align with strategy evaluation
        period
    KeyError
        If required strategy parameters or market data fields are missing

    Examples
    --------
    >>> backtest_strategy({
    ...     'coin_list': ['BTC', 'ETH'],
    ...     'buy_threshold': 0.05,
    ...     'sell_threshold': 0.02
    >>> }, price_data, volume_data)
    >>> {
    {'cagr': 12.4, 'sharpe_ratio': 1.7, 'max_drawdown': -18.2, 'total_trades':
    24, 'net_profit': 12500.0}

    >>> try:
    ...     backtest_strategy(invalid_config, price_data, volume_data)
    >>> except ValueError as e:
    ...     print(e)
    >>> }
    'Historical price data missing for required evaluation period'

    """
    return BacktestStrategyOutput(
        cagr=0.0,
        sharpe_ratio=0.0,
        max_drawdown=0.0,
        total_trades=0,
        net_profit=0.0,
    )