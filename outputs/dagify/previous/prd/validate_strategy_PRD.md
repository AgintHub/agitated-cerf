# validate_strategy PRD

## Description
Validate the trading strategy's feasibility by evaluating key performance and risk metrics from backtesting and hedging outputs.


## Conceptual Info

Validates a trading strategy's feasibility by aggregating performance metrics from backtesting and hedging results, determining if the strategy meets predefined viability thresholds.

## Docstring

### Summary
Validates the trading strategy by analyzing performance statistics, risk metrics, and profit/loss projections from backtest and hedge outputs.

### Parameters

- **backtest_result** (dict): Dictionary output from backtest_strategy containing performance metrics such as cagr, sharpe_ratio, max_drawdown, net_profit, and total_trades.
- **hedge_result** (dict): Dictionary from hedge_strategy containing hedging metrics such as hedging_ratio, entry_conditions, exit_conditions, crypto_exposure, tether_position, and strategy_summary.

### Returns

dict: Dictionary with keys is_valid, cagr, sharpe_ratio, max_drawdown, net_profit, total_trades matching the output_structure.

### Raises

- ValueError: Raised if required metrics are missing or of incorrect type in either input dictionary.

### Examples

```python
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
```

```python
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
```
