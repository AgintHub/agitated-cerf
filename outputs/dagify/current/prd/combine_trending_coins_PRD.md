# combine_trending_coins PRD

## Description
Synthesize price and volume indicators into unified coin selection


## Conceptual Info

This node merges price and volume trend analysis by calculating a composite score that weights price trend strength and volume activity. The output list prioritizes coins exhibiting synergistic price-volume dynamics.

## Docstring

### Summary
Merge price and volume-based trending coins into a weighted prioritized list

### Parameters

- **price_trend_coins** (List[str]): Coins identified by price analysis (output of identify_price_trends)
- **price_trend_scores** (List[float]): Normalized price trend scores from identify_price_trends
- **volume_trend_coins** (List[str]): Coins identified by volume analysis (output of identify_volume_trends)
- **volume_trend_scores** (List[float]): Normalized volume scores from identify_volume_trends

### Returns

Tuple[List[str], List[float], List[str], List[float]]: Returns (price_trend_coins, volume_trend_coins, combined_coins, composite_scores) where combined_coins is sorted by composite_scores

### Raises

- ValueError: If input lists contain duplicate coins or mismatched coin-score lengths
- AttributeError: If parent nodes haven't completed their analysis

### Examples

```python
>>> combine_trending_coins(['ADA', 'DOGE'], [0.45],
...                 ['ADA', 'XMR'], [0.62, 0.77])
{'price_trend_coins': ['ADA', 'DOGE'], 'volume_trend_coins': ['ADA', 'XMR'], 'combined_coins': ['ADA', 'XMR', 'DOGE'], 'composite_scores': [0.535, 0.77, 0.45]}
```
