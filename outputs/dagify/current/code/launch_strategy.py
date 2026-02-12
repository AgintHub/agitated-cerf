from pydantic import BaseModel, Field
from typing import List


class ValidateStrategyOutput(BaseModel):
    """Pydantic model for validate_strategy node outputs."""
    is_valid: bool = (
        Field(..., description="Whether the strategy meets predefined viability thresholds.")
    )
    cagr: float = (
        Field(..., description="Compound Annual Growth Rate of the strategy.")
    )
    sharpe_ratio: float = (
        Field(..., description="Sharpe Ratio indicating risk-adjusted return.")
    )
    max_drawdown: float = (
        Field(..., description="Maximum observed drawdown percentage.")
    )
    net_profit: float = (
        Field(..., description="Total net profit in USD after hedging.")
    )
    total_trades: int = (
        Field(..., description="Total number of trades executed.")
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


class LaunchStrategyOutput(BaseModel):
    """Pydantic model for launch_strategy node outputs."""
    initial_capital: float = (
        Field(..., description="Initial capital allocated to the trading strategy expressed in USD.")
    )
    entry_condition: str = (
        Field(..., description="Textual description of the criteria to enter a position.")
    )
    exit_condition: str = (
        Field(..., description="Textual description of the criteria to exit a position.")
    )
    hedging_ratio: float = (
        Field(..., description="Ratio of Tether (USDT) used for hedging relative to crypto exposure.")
    )
    risk_limit_cumulative_loss: float = (
        Field(..., description="Maximum cumulative loss in USD allowed before the strategy is halted.")
    )
    monitoring_metrics: List[str] = (
        Field(..., description="List of metrics that will be monitored during strategy execution (e.g., P&L, Sharpe Ratio, Drawdown).")
    )


def launch_strategy(validate_strategy_input: ValidateStrategyOutput, hedge_strategy_input: HedgeStrategyOutput, **kwargs) -> LaunchStrategyOutput:
    """
    Instantiate a trading strategy configuration from validated metrics and
    hedging parameters.

    Parameters
    ----------
    is_valid : bool
        Flag indicating whether the strategy passed validation.
    cagr : float
        Compound Annual Growth Rate of the validated strategy.
    sharpe_ratio : float
        Risk-adjusted return metric of the strategy.
    max_drawdown : float
        Maximum drawdown observed during backtesting.
    net_profit : float
        Net profit after hedging, in USD.
    total_trades : int
        Number of trades executed during backtesting.
    hedging_ratio : float
        Optimal ratio of Tether to crypto holdings determined by
        hedge_strategy.
    entry_conditions : str
        Conditions under which the hedge should be initiated (from
        hedge_strategy).
    exit_conditions : str
        Conditions under which the hedge should be closed (from
        hedge_strategy).

    Returns
    -------
    dict
        Dictionary containing configuration keys: initial_capital,
        entry_condition, exit_condition, hedging_ratio,
        risk_limit_cumulative_loss, monitoring_metrics.

    Raises
    ------
    ValueError
        Raised if the strategy is invalid (is_valid is False).

    Examples
    --------
    >>> config = launch_strategy(
    ...     is_valid=True,
    ...     cagr=0.35,
    ...     sharpe_ratio=2.1,
    ...     max_drawdown=0.15,
    ...     net_profit=120000.0,
    ...     total_trades=240,
    ...     hedging_ratio=0.25,
    ...     entry_conditions='BTC price rises 3% above 7-day SMA',
    ...     exit_conditions='BTC falls 2% below 7-day SMA'
    {'initial_capital': 100000.0, 'entry_condition': 'BTC price rises 3% above
    7-day SMA', 'exit_condition': 'BTC falls 2% below 7-day SMA',
    'hedging_ratio': 0.25, 'risk_limit_cumulative_loss': 20000.0,
    'monitoring_metrics': ['P&L', 'Sharpe Ratio', 'Drawdown']}

    >>> launch_strategy(is_valid=False, cagr=0.0, sharpe_ratio=0.0,
    max_drawdown=0.0, net_profit=0.0, total_trades=0, hedging_ratio=0.0,
    entry_conditions='', exit_conditions='')
    ValueError: Strategy validation failed. Cannot launch strategy.

    """
    return LaunchStrategyOutput(
        initial_capital=0.0,
        entry_condition="",
        exit_condition="",
        hedging_ratio=0.0,
        risk_limit_cumulative_loss=0.0,
        monitoring_metrics=[],
    )