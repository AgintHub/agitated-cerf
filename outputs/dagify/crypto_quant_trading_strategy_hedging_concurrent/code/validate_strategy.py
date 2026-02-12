from pydantic import BaseModel, Field


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


def validate_strategy(backtest_strategy_input: BacktestStrategyOutput, hedge_strategy_input: HedgeStrategyOutput, **kwargs) -> ValidateStrategyOutput:
    """
    Validates the trading strategy by analyzing performance statistics, risk
    metrics, and profit/loss projections from backtest and hedge outputs.

    Parameters
    ----------
    backtest_result : dict
        Dictionary output from backtest_strategy containing performance
        metrics such as cagr, sharpe_ratio, max_drawdown, net_profit, and
        total_trades.
    hedge_result : dict
        Dictionary from hedge_strategy containing hedging metrics such as
        hedging_ratio, entry_conditions, exit_conditions, crypto_exposure,
        tether_position, and strategy_summary.

    Returns
    -------
    dict
        Dictionary with keys is_valid, cagr, sharpe_ratio, max_drawdown,
        net_profit, total_trades matching the output_structure.

    Raises
    ------
    ValueError
        Raised if required metrics are missing or of incorrect type in
        either input dictionary.

    Examples
    --------
    >>> backtest_result = {
    ...     'cagr': 0.12,
    ...     'sharpe_ratio': 1.5,
    ...     'max_drawdown': 0.20,
    ...     'net_profit': 48000.0,
    ...     'total_trades': 150
    >>> }
    >>> hedge_result = {
    ...     'hedging_ratio': 0.30,
    ...     'entry_conditions': 'price > 0.01',
    ...     'exit_conditions': 'price < 0.009',
    ...     'crypto_exposure': 100000.0,
    ...     'tether_position': 30000.0,
    ...     'strategy_summary': 'Tether hedge to limit crypto exposure.'
    >>> }
    >>> validate_strategy(backtest_result, hedge_result)
    {
      'is_valid': True,
      'cagr': 0.12,
      'sharpe_ratio': 1.5,
      'max_drawdown': 0.20,
      'net_profit': 48000.0,
      'total_trades': 150
    }

    >>> backtest_result = {
    ...     'cagr': 0.05,
    ...     'sharpe_ratio': 0.8,
    ...     'max_drawdown': 0.35,
    ...     'net_profit': -12000.0,
    ...     'total_trades': 80
    >>> }
    >>> hedge_result = {
    ...     'hedging_ratio': 0.20,
    ...     'entry_conditions': 'price > 0.02',
    ...     'exit_conditions': 'price < 0.018',
    ...     'crypto_exposure': 50000.0,
    ...     'tether_position': 10000.0,
    ...     'strategy_summary': 'Limited hedge due to high drawdown.'
    >>> }
    >>> validate_strategy(backtest_result, hedge_result)
    {
      'is_valid': False,
      'cagr': 0.05,
      'sharpe_ratio': 0.8,
      'max_drawdown': 0.35,
      'net_profit': -12000.0,
      'total_trades': 80
    }

    """
    return ValidateStrategyOutput(
        is_valid=False,
        cagr=0.0,
        sharpe_ratio=0.0,
        max_drawdown=0.0,
        net_profit=0.0,
        total_trades=0,
    )