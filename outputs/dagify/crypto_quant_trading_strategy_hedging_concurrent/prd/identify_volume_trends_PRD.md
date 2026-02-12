# identify_volume_trends PRD

## Description
Identify volume-activated trending coins using transaction patterns.


## Conceptual Info

This node processes cleaned volume data and statistical metrics to flag cryptocurrencies that are currently experiencing significant trading volume trends.

## Docstring

### Summary
Identify volume-activated trending coins based on preprocessed volume data and statistical analysis.

### Parameters

- **volume_data** (dict): Output from preprocess_volume_data containing normalized volume series and related metadata.
- **analysis_results** (dict): Output from perform_statistical_analysis containing correlation coefficients, regression slopes, etc.

### Returns

dict: Dictionary with keys:
- trending_coin_symbols (List[str])
- volume_scores (List[float])
- volume_thresholds (List[float])

### Raises

- ValueError: Raised when volume_data or analysis_results are missing required fields or contain inconsistent lengths.

### Examples

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
