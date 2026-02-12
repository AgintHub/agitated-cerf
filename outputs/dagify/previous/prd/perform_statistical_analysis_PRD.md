# perform_statistical_analysis PRD

## Description
Conduct regression and correlation analyses on cleaned price and volume datasets, producing numerical metrics and descriptive summaries for downstream trend identification.


## Conceptual Info

This node performs statistical exploration on pre‑processed price and volume time series. It fits simple linear regressions of each feature against a chosen target (typically price) and calculates Pearson correlation coefficients, R² scores, and p‑values. The resulting metrics help downstream nodes (price/volume trend identification) to rank coins and set threshold scores.

## Docstring

### Summary
Perform regression and correlation analyses on cleaned price and volume datasets to extract statistical metrics for trend detection.

### Parameters

- **price_data** (dict): Dictionary returned by `preprocess_price_data`, containing keys `dates`, `prices`, `missing_values_count`, and `is_normalized`.
- **volume_data** (dict): Dictionary returned by `preprocess_volume_data`, containing keys `dates`, `raw_volumes`, `normalized_volumes`, `missing_value_count`, and `is_valid`.
- **target_feature** (str): Name of the feature to predict (default: `'prices'`). It must exist in `price_data`.

### Returns

dict: A dictionary mapping the output field names to their computed values, matching the node's output_structure.

### Raises

- ValueError: If `price_data` or `volume_data` is missing required keys, or if `target_feature` is not present.
- RuntimeError: If regression or correlation calculation fails due to insufficient data.

### Examples

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
