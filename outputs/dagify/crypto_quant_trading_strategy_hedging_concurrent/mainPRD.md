# crypto_quant_trading_strategy_hedging_concurrent - Complete PRD Documentation

## Overview
PRDs for nodes in the 'crypto_quant_trading_strategy_hedging_concurrent' module.

## Table of Contents

- [backtest_strategy](#backtest_strategy)

- [combine_trending_coins](#combine_trending_coins)

- [develop_trading_strategy](#develop_trading_strategy)

- [download_historical_prices](#download_historical_prices)

- [download_historical_volumes](#download_historical_volumes)

- [gather_data](#gather_data)

- [hedge_strategy](#hedge_strategy)

- [identify_price_trends](#identify_price_trends)

- [identify_volume_trends](#identify_volume_trends)

- [launch_strategy](#launch_strategy)

- [perform_statistical_analysis](#perform_statistical_analysis)

- [preprocess_price_data](#preprocess_price_data)

- [preprocess_volume_data](#preprocess_volume_data)

- [validate_strategy](#validate_strategy)



---

## backtest_strategy

### Description
Backtest the trading strategy using historical price and volume data, and produce key performance metrics.

### Conceptual Info

Evaluates the viability of a trading strategy by simulating execution against historical price/volume data, quantifying performance via risk-adjusted returns, drawdown patterns, and trade frequency.

### Docstring

**Summary:** Executes a backtest of the defined trading strategy using historical market data, calculating CAGR, Sharpe Ratio, and drawdown metrics to assess performance.

**Parameters:**

- strategy_config (dict): Trading strategy configuration containing parameters like coin_list, buy_threshold, sell_threshold, and max_drawdown from develop_trading_strategy
- historical_prices (dict): Processed price history for BTC, ETH, and stablecoins formatted as {dates, prices_btc, prices_eth, prices_stable}
- historical_volumes (dict): Volume data for market activity including BTC, ETH, and stablecoin volumes over time
**Returns:** dict[str, float | int] - Performance metrics including compound annual growth rate, risk-adjusted return ratio, maximum capital loss, total trade count, and net profitability

**Raises:**

- ValueError: If historical data timelines don't align with strategy evaluation period
- KeyError: If required strategy parameters or market data fields are missing
**Examples:**

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



---

## combine_trending_coins

### Description
Synthesize price and volume indicators into unified coin selection

### Conceptual Info

This node merges price and volume trend analysis by calculating a composite score that weights price trend strength and volume activity. The output list prioritizes coins exhibiting synergistic price-volume dynamics.

### Docstring

**Summary:** Merge price and volume-based trending coins into a weighted prioritized list

**Parameters:**

- price_trend_coins (List[str]): Coins identified by price analysis (output of identify_price_trends)
- price_trend_scores (List[float]): Normalized price trend scores from identify_price_trends
- volume_trend_coins (List[str]): Coins identified by volume analysis (output of identify_volume_trends)
- volume_trend_scores (List[float]): Normalized volume scores from identify_volume_trends
**Returns:** Tuple[List[str], List[float], List[str], List[float]] - Returns (price_trend_coins, volume_trend_coins, combined_coins, composite_scores) where combined_coins is sorted by composite_scores

**Raises:**

- ValueError: If input lists contain duplicate coins or mismatched coin-score lengths
- AttributeError: If parent nodes haven't completed their analysis
**Examples:**

```python
>>> combine_trending_coins(['ADA', 'DOGE'], [0.45],
...                 ['ADA', 'XMR'], [0.62, 0.77])
{'price_trend_coins': ['ADA', 'DOGE'], 'volume_trend_coins': ['ADA', 'XMR'], 'combined_coins': ['ADA', 'XMR', 'DOGE'], 'composite_scores': [0.535, 0.77, 0.45]}
```



---

## develop_trading_strategy

### Description
Develop a trading strategy based on trending coins

### Conceptual Info

This node synthesizes price-volume trending coins into a quantifiable trading strategy by defining entry/exit thresholds, risk limits, and drawdown constraints. It integrates market data from the combine_trending_coins node to build a capitalized structure adaptable to trend volatility.

### Docstring

**Summary:** Generates a parameterized trading strategy from composite coin trend data

**Parameters:**

- combined_coins (List[str]): Prioritized list of price-volume synergized coins from combine_trending_coins
- composite_scores (List[float]): Weighted scores reflecting price-volume trend synergy for each coin
**Returns:** Dict[str, Any] - Trading strategy configuration with explicit thresholds, risk parameters, and coin selections

**Raises:**

- ValueError: If combined_coins has fewer than 3 valid coin entries
- ValueError: If composite_scores length does not match combined_coins
**Examples:**

```python
>>> develop_trading_strategy(['BTC', 'ETH'], [0.85, 0.72])
>>> {'strategy_name': 'TrendArb-2024', 'max_drawdown': 15.5}
{'strategy_name': 'TrendArb-2024', 'coin_list': ['BTC', 'ETH'], 'buy_threshold': 0.05, 'sell_threshold': 0.10, 'max_drawdown': 15.5, 'risk_per_trade': 2.0}
```

```python
>>> develop_trading_strategy(['ADA'], [0.67])
>>> ValueError: combined_coins requires at least 3 valid entries
ValueError: combined_coins requires at least 3 valid entries
```



---

## download_historical_prices

### Description
Retrieve historical price data for BTC, stable and ETH

### Conceptual Info

This node fetches raw historical closing price series for Bitcoin (BTC), Ethereum (ETH), and a selected stablecoin (typically USDT) from a public cryptocurrency data provider such as CoinMarketCap or Quandl. The data is returned in aligned lists of ISO‑8601 date strings and corresponding float price values, enabling downstream preprocessing and analysis steps.

### Docstring

**Summary:** Download historical price data for BTC, ETH, and a stablecoin from a public API.

**Parameters:**

- api_key (str): API key for the chosen data provider (e.g., CoinMarketCap).
- start_date (str): ISO 8601 start date for the historical period (inclusive).
- end_date (str): ISO 8601 end date for the historical period (inclusive).
- symbols (List[str]): List of cryptocurrency symbols to query, e.g., ['BTC', 'ETH', 'USDT'].
**Returns:** Dict[str, List[Union[str, float]]] - A dictionary with keys 'dates', 'prices_btc', 'prices_eth', and 'prices_stable', each mapping to a list of values aligned by index. The 'dates' list contains ISO 8601 date strings; the price lists contain the closing price in USD for the corresponding date.

**Raises:**

- ValueError: If any of the input parameters are missing or empty.
- ConnectionError: If the API endpoint cannot be reached.
- RuntimeError: If the API returns an error status or malformed data.
**Examples:**

```python
>>> api_key = 'YOUR_CMC_API_KEY'
>>> start_date = '2023-01-01'
>>> end_date = '2023-01-10'
>>> symbols = ['BTC', 'ETH', 'USDT']
>>> prices = download_historical_prices(api_key, start_date, end_date, symbols)
{
  'dates': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10'],
  'prices_btc': [32000.1, 32200.5, 31500.0, 33000.2, 33500.7, 34000.0, 34500.3, 35000.6, 35500.1, 36000.4],
  'prices_eth': [2000.5, 2025.3, 1980.7, 2050.2, 2100.6, 2150.1, 2200.4, 2250.8, 2300.3, 2350.7],
  'prices_stable': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
}
```

```python
>>> # If the API key is invalid or missing, the function raises ValueError
>>> download_historical_prices('', '2023-01-01', '2023-01-10', ['BTC'])
ValueError: API key must be provided.
```



---

## download_historical_volumes

### Description
Retrieve historical volume data for BTC, stable and ETH from a reputable data source such as CoinMarketCap or Quandl.

### Conceptual Info

The node fetches historical daily trading volume data for Bitcoin (BTC), a stablecoin (e.g., USDT), and Ethereum (ETH) from a trusted data provider such as CoinMarketCap or Quandl. It aligns the data by date, ensuring that each list of volumes corresponds to the same chronological sequence. The output is structured to support downstream preprocessing and statistical analysis.

### Docstring

**Summary:** Download daily trading volumes for BTC, stablecoin, and ETH from an external API.

**Parameters:**

- api_key (str): API key for authenticating with the data provider.
- start_date (str): ISO 8601 start date (YYYY-MM-DD) for the historical period to retrieve.
- end_date (str): ISO 8601 end date (YYYY-MM-DD) for the historical period to retrieve.
- base_url (str): Base endpoint URL of the data provider API.
**Returns:** dict - A dictionary containing six keys:
- btc_dates: List[str] of dates for BTC volume records
- btc_volumes: List[float] of daily BTC volumes
- stablecoin_dates: List[str] of dates for stablecoin volume records
- stablecoin_volumes: List[float] of daily stablecoin volumes
- eth_dates: List[str] of dates for ETH volume records
- eth_volumes: List[float] of daily ETH volumes

**Raises:**

- ValueError: If start_date is after end_date or dates are not in ISO format.
- ConnectionError: If the API endpoint is unreachable or returns a network error.
- HTTPError: If the API returns a non‑200 HTTP status code.
- KeyError: If the expected volume fields are missing from the API response.
**Examples:**

```python
>>> volumes = download_historical_volumes(
...     api_key='my_api_key',
...     start_date='2023-01-01',
...     end_date='2023-01-05',
...     base_url='https://api.coinmarketcap.com/v1/'
>>> )
>>> print(volumes['btc_volumes'])
[12000000.0, 11500000.5, 12345678.9, 11000000.0, 11800000.2]
```

```python
>>> volumes = download_historical_volumes(
...     api_key='my_api_key',
...     start_date='2023-01-01',
...     end_date='2023-01-01',
...     base_url='https://api.coinmarketcap.com/v1/'
>>> )
>>> print(volumes['eth_dates'])
['2023-01-01']
```



---

## gather_data

### Description
Collect historical price and volume data for BTC, stable and ETH

### Conceptual Info

The gather_data node serves as the foundational data ingestion step for the cryptocurrency trading workflow. It downloads aligned historical price and volume time series for three key assets—Bitcoin (BTC), a stablecoin (e.g., USDT), and Ethereum (ETH)—from a reliable external provider such as CoinMarketCap or Quandl. These time series are later used for statistical analysis, trend identification, strategy development, backtesting, and hedging.

### Docstring

**Summary:** Download and consolidate historical price and volume data for BTC, stable and ETH.

**Parameters:**

- source (str): The name of the data provider (e.g., 'CoinMarketCap', 'Quandl'). The function selects the appropriate API credentials and endpoints based on this value.
- start_date (str): ISO 8601 start date for the requested data (e.g., '2022-01-01').
- end_date (str): ISO 8601 end date for the requested data (e.g., '2023-01-01').
- assets (List[str]): List of asset symbols to fetch (must include 'BTC', 'ETH', and a stablecoin symbol such as 'USDT').
**Returns:** Dict[str, List[Union[str, float]]] - A dictionary containing four keys: 'price_dates', 'prices', 'volume_dates', and 'volumes'. The lists are aligned such that the i-th element of each list corresponds to the same calendar day. Dates are ISO 8601 strings; price and volume values are floats.

**Raises:**

- ConnectionError: Raised if the API endpoint cannot be reached or network issues occur.
- ValueError: Raised if required parameters are missing, the asset list does not contain the mandatory symbols, or the date range is invalid.
- KeyError: Raised if the API response does not include data for one or more requested assets.
**Examples:**

```python
>>> data = gather_data(
...     source='CoinMarketCap',
...     start_date='2022-01-01',
...     end_date='2022-01-10',
...     assets=['BTC', 'ETH', 'USDT']
>>> )
{'price_dates': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-06', '2022-01-07', '2022-01-08', '2022-01-09', '2022-01-10'], 'prices': [47000.0, 47500.0, 47200.0, 48000.0, 47800.0, 48500.0, 49000.0, 49500.0, 50000.0, 50500.0], 'volume_dates': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-06', '2022-01-07', '2022-01-08', '2022-01-09', '2022-01-10'], 'volumes': [3500000000.0, 3600000000.0, 3550000000.0, 3650000000.0, 3600000000.0, 3700000000.0, 3750000000.0, 3800000000.0, 3850000000.0, 3900000000.0]}
```

```python
>>> data = gather_data(
...     source='Quandl',
...     start_date='2023-06-01',
...     end_date='2023-06-05',
...     assets=['BTC', 'ETH', 'USDT']
>>> )
{'price_dates': ['2023-06-01', '2023-06-02', '2023-06-03', '2023-06-04', '2023-06-05'], 'prices': [25000.0, 25100.0, 24900.0, 25200.0, 25300.0], 'volume_dates': ['2023-06-01', '2023-06-02', '2023-06-03', '2023-06-04', '2023-06-05'], 'volumes': [2000000000.0, 2100000000.0, 2050000000.0, 2150000000.0, 2200000000.0]}
```



---

## hedge_strategy

### Description
Creates a Tether‑based hedging plan that specifies how much USDT to hold relative to crypto exposure, when to enter and exit hedges, and provides a concise strategy summary.

### Conceptual Info

The hedge_strategy node generates a dynamic, data‑driven hedging plan that balances the portfolio’s crypto exposure with a Tether position. It calculates the optimal hedging ratio based on risk appetite and market volatility, defines precise entry and exit triggers, and outputs a concise strategy summary for downstream execution.

### Docstring

**Summary:** Generate a Tether‑based hedging plan for a crypto trading strategy.

**Parameters:**

- strategy_name (str): Name of the trading strategy produced by develop_trading_strategy.
- coin_list (list[str]): List of coin symbols included in the strategy.
- buy_threshold (float): Threshold value used to trigger a buy signal in the strategy.
- sell_threshold (float): Threshold value used to trigger a sell signal in the strategy.
- max_drawdown (float): Maximum acceptable drawdown percentage for the strategy.
- risk_per_trade (float): Percentage of capital risked per trade.
**Returns:** dict - A dictionary containing hedging_ratio, entry_conditions, exit_conditions, crypto_exposure, tether_position, and strategy_summary.

**Raises:**

- ValueError: If any numeric input is non‑positive or if coin_list is empty.
**Examples:**

```python
>>> # Example 1: Basic hedging for a high‑risk strategy
>>> hedge_strategy(
...     strategy_name='MomentumTrader',
...     coin_list=['BTC', 'ETH'],
...     buy_threshold=0.05,
...     sell_threshold=0.07,
...     max_drawdown=0.20,
...     risk_per_trade=0.02
>>> )
{'hedging_ratio': 0.15, 'entry_conditions': 'BTC price drops >5% or ETH drops >7%', 'exit_conditions': 'Price recovers 3% from entry or volatility drops below threshold', 'crypto_exposure': 150000.0, 'tether_position': 22500.0, 'strategy_summary': 'High‑risk momentum strategy hedged 15% with USDT to cap losses.'}
```

```python
>>> # Example 2: Conservative hedge with low volatility
>>> hedge_strategy(
...     strategy_name='StableTrend',
...     coin_list=['BTC'],
...     buy_threshold=0.02,
...     sell_threshold=0.03,
...     max_drawdown=0.05,
...     risk_per_trade=0.01
>>> )
{'hedging_ratio': 0.10, 'entry_conditions': 'BTC drops >2% or 3% for sell', 'exit_conditions': 'Price recovers 1% or volatility <0.5%', 'crypto_exposure': 50000.0, 'tether_position': 5000.0, 'strategy_summary': 'Conservative strategy hedged 10% with USDT to protect against small dips.'}
```



---

## identify_price_trends

### Description
Identify price-driven trending coins using statistical patterns.

### Conceptual Info

The `identify_price_trends` node analyzes clean, normalized price time series alongside regression and correlation metrics to flag cryptocurrencies that are exhibiting statistically significant upward trends. It outputs a ranked list of trending coins, a quantitative score per coin reflecting trend strength, and a count of identified trends. These results are then passed to downstream nodes for volume‑based trend synthesis and strategy development.

### Docstring

**Summary:** Identify price‑driven trending coins using statistical analysis.

**Parameters:**

- preprocessed_prices (Dict[str, List[float]]): Dictionary mapping coin identifiers to their normalized price series. Keys are coin symbols (e.g., 'BTC', 'ETH'). Each list aligns with the global date index supplied by `preprocess_price_data`.
- analysis_results (Dict[str, Any]): Output of `perform_statistical_analysis`, containing regression slopes, R² scores, and correlation coefficients for each feature against the price target. The node uses the regression slope and R² to quantify trend strength.
**Returns:** Tuple[List[str], List[float], int] - A tuple containing (`trending_coins`, `trend_scores`, `num_coins`). `trending_coins` is ordered by descending `trend_scores`.

**Raises:**

- ValueError: Raised if any input list is empty or if required keys are missing from the analysis results.
- TypeError: Raised if input types do not match the expected signatures (e.g., prices not numeric).
**Examples:**

```python
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
```

```python
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
```



---

## identify_volume_trends

### Description
Identify volume-activated trending coins using transaction patterns.

### Conceptual Info

This node processes cleaned volume data and statistical metrics to flag cryptocurrencies that are currently experiencing significant trading volume trends.

### Docstring

**Summary:** Identify volume-activated trending coins based on preprocessed volume data and statistical analysis.

**Parameters:**

- volume_data (dict): Output from preprocess_volume_data containing normalized volume series and related metadata.
- analysis_results (dict): Output from perform_statistical_analysis containing correlation coefficients, regression slopes, etc.
**Returns:** dict - Dictionary with keys:
- trending_coin_symbols (List[str])
- volume_scores (List[float])
- volume_thresholds (List[float])

**Raises:**

- ValueError: Raised when volume_data or analysis_results are missing required fields or contain inconsistent lengths.
**Examples:**

```python
>>> result = identify_volume_trends(
...     volume_data={
...         'normalized_volumes': [120.0, 150.0, 80.0],
...         'dates': ['2024-01-01', '2024-01-02', '2024-01-03']
...     },
...     analysis_results={
...         'correlation_coefficients': [0.92, 0.88, 0.45],
...         'feature_names': ['volume', 'price']
...     }
>>> )
{
  "trending_coin_symbols": ["BTC", "ETH"],
  "volume_scores": [0.92, 0.88],
  "volume_thresholds": [100.0, 130.0]
}
```

```python
>>> result = identify_volume_trends(
...     volume_data={
...         'normalized_volumes': [200.0, 210.0],
...         'dates': ['2024-01-01', '2024-01-02']
...     },
...     analysis_results={
...         'correlation_coefficients': [0.95, 0.93],
...         'feature_names': ['volume', 'price']
...     }
>>> )
{
  "trending_coin_symbols": ["BTC"],
  "volume_scores": [0.95],
  "volume_thresholds": [190.0]
}
```



---

## launch_strategy

### Description
Launch the validated trading strategy by allocating capital, setting entry/exit conditions, applying hedging ratios, defining cumulative loss limits, and specifying monitoring metrics.

### Conceptual Info

The launch_strategy node takes validated strategy metrics and hedging information to instantiate a live trading configuration. It determines how much capital to commit, when to enter and exit trades, how much Tether to allocate for hedging, sets a hard stop based on cumulative loss, and specifies performance indicators to track.

### Docstring

**Summary:** Instantiate a trading strategy configuration from validated metrics and hedging parameters.

**Parameters:**

- is_valid (bool): Flag indicating whether the strategy passed validation.
- cagr (float): Compound Annual Growth Rate of the validated strategy.
- sharpe_ratio (float): Risk-adjusted return metric of the strategy.
- max_drawdown (float): Maximum drawdown observed during backtesting.
- net_profit (float): Net profit after hedging, in USD.
- total_trades (int): Number of trades executed during backtesting.
- hedging_ratio (float): Optimal ratio of Tether to crypto holdings determined by hedge_strategy.
- entry_conditions (str): Conditions under which the hedge should be initiated (from hedge_strategy).
- exit_conditions (str): Conditions under which the hedge should be closed (from hedge_strategy).
**Returns:** dict - Dictionary containing configuration keys: initial_capital, entry_condition, exit_condition, hedging_ratio, risk_limit_cumulative_loss, monitoring_metrics.

**Raises:**

- ValueError: Raised if the strategy is invalid (is_valid is False).
**Examples:**

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



---

## perform_statistical_analysis

### Description
Conduct regression and correlation analyses on cleaned price and volume datasets, producing numerical metrics and descriptive summaries for downstream trend identification.

### Conceptual Info

This node performs statistical exploration on pre‑processed price and volume time series. It fits simple linear regressions of each feature against a chosen target (typically price) and calculates Pearson correlation coefficients, R² scores, and p‑values. The resulting metrics help downstream nodes (price/volume trend identification) to rank coins and set threshold scores.

### Docstring

**Summary:** Perform regression and correlation analyses on cleaned price and volume datasets to extract statistical metrics for trend detection.

**Parameters:**

- price_data (dict): Dictionary returned by `preprocess_price_data`, containing keys `dates`, `prices`, `missing_values_count`, and `is_normalized`.
- volume_data (dict): Dictionary returned by `preprocess_volume_data`, containing keys `dates`, `raw_volumes`, `normalized_volumes`, `missing_value_count`, and `is_valid`.
- target_feature (str): Name of the feature to predict (default: `'prices'`). It must exist in `price_data`.
**Returns:** dict - A dictionary mapping the output field names to their computed values, matching the node's output_structure.

**Raises:**

- ValueError: If `price_data` or `volume_data` is missing required keys, or if `target_feature` is not present.
- RuntimeError: If regression or correlation calculation fails due to insufficient data.
**Examples:**

```python
>>> # Mock preprocessed price data
>>> price_data = {
...     'dates': ['2024-01-01', '2024-01-02', '2024-01-03'],
...     'prices': [100.0, 102.5, 101.0],
...     'missing_values_count': 0,
...     'is_normalized': True
>>> }
>>> # Mock preprocessed volume data
>>> volume_data = {
...     'dates': ['2024-01-01', '2024-01-02', '2024-01-03'],
...     'raw_volumes': [5000, 5200, 5100],
...     'normalized_volumes': [0.0, 0.2, 0.1],
...     'missing_value_count': 0,
...     'is_valid': True
>>> }
{feature_names: [prices, normalized_volumes], correlation_coefficients: [0.98], regression_slopes: [2.5, -0.5], regression_intercepts: [50.0, 1.0], regression_r2_scores: [0.97, 0.9], regression_p_values: [0.001, 0.05], analysis_summary: Strong positive correlation between price and volume; price increases with volume.}
```

```python
>>> # Using default target feature
>>> result = perform_statistical_analysis(price_data, volume_data)
>>> print(result['analysis_summary'])
"Strong positive correlation between price and volume; price increases with volume."
```



---

## preprocess_price_data

### Description
Clean and transform price data for analysis by imputing missing values, normalizing price series, and scaling features.

### Conceptual Info

The `preprocess_price_data` node transforms raw historical price data into a clean, consistent, and analysis‑ready format. It fills gaps, scales the series for comparability across assets, and records key metadata such as how many values were imputed and whether normalization was applied. This processed output feeds statistical analysis and trend‑identification steps downstream.

### Docstring

**Summary:** Preprocesses raw historical price data for downstream analysis.

**Parameters:**

- dates (List[str]): List of ISO‑formatted dates (YYYY-MM-DD) for which price data was retrieved.
- prices_btc (List[float]): List of closing prices for BTC aligned with the dates list.
- prices_eth (List[float]): List of closing prices for ETH aligned with the dates list.
- prices_stable (List[float]): List of closing prices for the chosen stablecoin (e.g., USDT) aligned with the dates list.
**Returns:** Dict[str, Any] - A dictionary containing the cleaned and transformed price series, including dates, a unified price list, the count of imputed values, and a flag indicating whether normalization was performed.

**Raises:**

- ValueError: If the input price lists are of unequal length or contain non‑numeric entries.
- TypeError: If any input parameter is not of the expected type.
**Examples:**

```python
>>> # Example 1: Simple preprocessing with no missing values
>>> output = preprocess_price_data(
...     dates=['2023-01-01', '2023-01-02'],
...     prices_btc=[20000.0, 21000.0],
...     prices_eth=[1200.0, 1250.0],
...     prices_stable=[1.0, 1.0]
>>> )
>>> print(output)
{'dates': ['2023-01-01', '2023-01-02'], 'prices': [20000.0, 21000.0], 'missing_values_count': 0, 'is_normalized': False}
```

```python
>>> # Example 2: Handling missing values and normalizing
>>> output = preprocess_price_data(
...     dates=['2023-01-01', '2023-01-02', '2023-01-03'],
...     prices_btc=[20000.0, None, 21000.0],
...     prices_eth=[1200.0, 1250.0, None],
...     prices_stable=[1.0, 1.0, 1.0]
>>> )
>>> print(output)
{'dates': ['2023-01-01', '2023-01-02', '2023-01-03'], 'prices': [20000.0, 20000.0, 21000.0], 'missing_values_count': 2, 'is_normalized': True}
```



---

## preprocess_volume_data

### Description
Clean and transform volume data for analysis by removing missing entries, normalizing volumes to a common scale, and preparing the dataset for downstream statistical analysis.

### Conceptual Info

This node takes raw historical volume data for BTC, stablecoins, and ETH, cleans it by handling missing entries, and normalizes the volumes to a uniform scale. The resulting dataset is ready for statistical trend analysis and further trading strategy development.

### Docstring

**Summary:** Preprocesses historical cryptocurrency volume data by handling missing values and normalizing the series.

**Parameters:**

- btc_dates (List[str]): ISO 8601 formatted dates for BTC volume records.
- btc_volumes (List[float]): Daily trading volumes for BTC aligned with btc_dates.
- stablecoin_dates (List[str]): ISO 8601 formatted dates for stablecoin volume records.
- stablecoin_volumes (List[float]): Daily trading volumes for stablecoins aligned with stablecoin_dates.
- eth_dates (List[str]): ISO 8601 formatted dates for ETH volume records.
- eth_volumes (List[float]): Daily trading volumes for ETH aligned with eth_dates.
- normalization_method (str): Method used for scaling volumes: 'minmax' for 0-1 scaling or 'standard' for mean‑zero/std‑one standardization.
**Returns:** Dict[str, Any] - A dictionary containing cleaned dates, raw volumes, normalized volumes, missing value count, and a validity flag.

**Raises:**

- ValueError: If any of the date lists are empty or lengths of dates and volumes do not match.
- TypeError: If volume inputs contain non‑numeric values.
**Examples:**

```python
>>> result = preprocess_volume_data(
...     btc_dates=['2023-01-01', '2023-01-02'],
...     btc_volumes=[1000.0, 1100.0],
...     stablecoin_dates=['2023-01-01', '2023-01-02'],
...     stablecoin_volumes=[2000.0, 2100.0],
...     eth_dates=['2023-01-01', '2023-01-02'],
...     eth_volumes=[1500.0, 1600.0],
...     normalization_method='minmax')
{'dates': ['2023-01-01', '2023-01-02'], 'raw_volumes': [1000.0, 1100.0, 2000.0, 2100.0, 1500.0, 1600.0], 'normalized_volumes': [0.0, 0.1, 0.7, 0.8, 0.4, 0.5], 'missing_value_count': 0, 'is_valid': True}
```

```python
>>> result = preprocess_volume_data(
...     btc_dates=['2023-01-01', None],
...     btc_volumes=[1000.0, None],
...     stablecoin_dates=['2023-01-01'],
...     stablecoin_volumes=[2000.0],
...     eth_dates=['2023-01-01'],
...     eth_volumes=[1500.0],
...     normalization_method='standard')
{'dates': ['2023-01-01'], 'raw_volumes': [1000.0, 2000.0, 1500.0], 'normalized_volumes': [-1.0, 1.0, 0.0], 'missing_value_count': 2, 'is_valid': True}
```



---

## validate_strategy

### Description
Validate the trading strategy's feasibility by evaluating key performance and risk metrics from backtesting and hedging outputs.

### Conceptual Info

Validates a trading strategy's feasibility by aggregating performance metrics from backtesting and hedging results, determining if the strategy meets predefined viability thresholds.

### Docstring

**Summary:** Validates the trading strategy by analyzing performance statistics, risk metrics, and profit/loss projections from backtest and hedge outputs.

**Parameters:**

- backtest_result (dict): Dictionary output from backtest_strategy containing performance metrics such as cagr, sharpe_ratio, max_drawdown, net_profit, and total_trades.
- hedge_result (dict): Dictionary from hedge_strategy containing hedging metrics such as hedging_ratio, entry_conditions, exit_conditions, crypto_exposure, tether_position, and strategy_summary.
**Returns:** dict - Dictionary with keys is_valid, cagr, sharpe_ratio, max_drawdown, net_profit, total_trades matching the output_structure.

**Raises:**

- ValueError: Raised if required metrics are missing or of incorrect type in either input dictionary.
**Examples:**

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

