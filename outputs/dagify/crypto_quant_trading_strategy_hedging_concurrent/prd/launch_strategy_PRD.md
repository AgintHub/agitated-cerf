# launch_strategy PRD

## Description
Launch the validated trading strategy by allocating capital, setting entry/exit conditions, applying hedging ratios, defining cumulative loss limits, and specifying monitoring metrics.


## Conceptual Info

The launch_strategy node takes validated strategy metrics and hedging information to instantiate a live trading configuration. It determines how much capital to commit, when to enter and exit trades, how much Tether to allocate for hedging, sets a hard stop based on cumulative loss, and specifies performance indicators to track.

## Docstring

### Summary
Instantiate a trading strategy configuration from validated metrics and hedging parameters.

### Parameters

- **is_valid** (bool): Flag indicating whether the strategy passed validation.
- **cagr** (float): Compound Annual Growth Rate of the validated strategy.
- **sharpe_ratio** (float): Risk-adjusted return metric of the strategy.
- **max_drawdown** (float): Maximum drawdown observed during backtesting.
- **net_profit** (float): Net profit after hedging, in USD.
- **total_trades** (int): Number of trades executed during backtesting.
- **hedging_ratio** (float): Optimal ratio of Tether to crypto holdings determined by hedge_strategy.
- **entry_conditions** (str): Conditions under which the hedge should be initiated (from hedge_strategy).
- **exit_conditions** (str): Conditions under which the hedge should be closed (from hedge_strategy).

### Returns

dict: Dictionary containing configuration keys: initial_capital, entry_condition, exit_condition, hedging_ratio, risk_limit_cumulative_loss, monitoring_metrics.

### Raises

- ValueError: Raised if the strategy is invalid (is_valid is False).

### Examples

```python
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
{'initial_capital': 100000.0, 'entry_condition': 'BTC price rises 3% above 7-day SMA', 'exit_condition': 'BTC falls 2% below 7-day SMA', 'hedging_ratio': 0.25, 'risk_limit_cumulative_loss': 20000.0, 'monitoring_metrics': ['P&L', 'Sharpe Ratio', 'Drawdown']}
```

```python
>>> launch_strategy(is_valid=False, cagr=0.0, sharpe_ratio=0.0, max_drawdown=0.0, net_profit=0.0, total_trades=0, hedging_ratio=0.0, entry_conditions='', exit_conditions='')
ValueError: Strategy validation failed. Cannot launch strategy.
```
