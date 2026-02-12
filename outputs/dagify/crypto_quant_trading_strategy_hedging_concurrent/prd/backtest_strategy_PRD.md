# backtest_strategy PRD

## Description
Backtest the trading strategy using historical price and volume data, and produce key performance metrics.


## Conceptual Info

Evaluates the viability of a trading strategy by simulating execution against historical price/volume data, quantifying performance via risk-adjusted returns, drawdown patterns, and trade frequency.

## Docstring

### Summary
Executes a backtest of the defined trading strategy using historical market data, calculating CAGR, Sharpe Ratio, and drawdown metrics to assess performance.

### Parameters

- **strategy_config** (dict): Trading strategy configuration containing parameters like coin_list, buy_threshold, sell_threshold, and max_drawdown from develop_trading_strategy
- **historical_prices** (dict): Processed price history for BTC, ETH, and stablecoins formatted as {dates, prices_btc, prices_eth, prices_stable}
- **historical_volumes** (dict): Volume data for market activity including BTC, ETH, and stablecoin volumes over time

### Returns

dict[str, float | int]: Performance metrics including compound annual growth rate, risk-adjusted return ratio, maximum capital loss, total trade count, and net profitability

### Raises

- ValueError: If historical data timelines don't align with strategy evaluation period
- KeyError: If required strategy parameters or market data fields are missing

### Examples

```python
>>> backtest_strategy({
...     'coin_list': ['BTC', 'ETH'],
...     'buy_threshold': 0.05,
...     'sell_threshold': 0.02
>>> }, price_data, volume_data)
>>> {
{'cagr': 12.4, 'sharpe_ratio': 1.7, 'max_drawdown': -18.2, 'total_trades': 24, 'net_profit': 12500.0}
```

```python
>>> try:
...     backtest_strategy(invalid_config, price_data, volume_data)
>>> except ValueError as e:
...     print(e)
>>> }
'Historical price data missing for required evaluation period'
```
