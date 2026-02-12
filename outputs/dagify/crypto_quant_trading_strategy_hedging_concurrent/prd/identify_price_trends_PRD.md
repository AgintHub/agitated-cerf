# identify_price_trends PRD

## Description
Identify price-driven trending coins using statistical patterns.


## Conceptual Info

The `identify_price_trends` node analyzes clean, normalized price time series alongside regression and correlation metrics to flag cryptocurrencies that are exhibiting statistically significant upward trends. It outputs a ranked list of trending coins, a quantitative score per coin reflecting trend strength, and a count of identified trends. These results are then passed to downstream nodes for volume‑based trend synthesis and strategy development.

## Docstring

### Summary
Identify price‑driven trending coins using statistical analysis.

### Parameters

- **preprocessed_prices** (Dict[str, List[float]]): Dictionary mapping coin identifiers to their normalized price series. Keys are coin symbols (e.g., 'BTC', 'ETH'). Each list aligns with the global date index supplied by `preprocess_price_data`.
- **analysis_results** (Dict[str, Any]): Output of `perform_statistical_analysis`, containing regression slopes, R² scores, and correlation coefficients for each feature against the price target. The node uses the regression slope and R² to quantify trend strength.

### Returns

Tuple[List[str], List[float], int]: A tuple containing (`trending_coins`, `trend_scores`, `num_coins`). `trending_coins` is ordered by descending `trend_scores`.

### Raises

- ValueError: Raised if any input list is empty or if required keys are missing from the analysis results.
- TypeError: Raised if input types do not match the expected signatures (e.g., prices not numeric).

### Examples

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
