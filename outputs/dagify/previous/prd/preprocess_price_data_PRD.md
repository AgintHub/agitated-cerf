# preprocess_price_data PRD

## Description
Clean and transform price data for analysis by imputing missing values, normalizing price series, and scaling features.


## Conceptual Info

The `preprocess_price_data` node transforms raw historical price data into a clean, consistent, and analysis‑ready format. It fills gaps, scales the series for comparability across assets, and records key metadata such as how many values were imputed and whether normalization was applied. This processed output feeds statistical analysis and trend‑identification steps downstream.

## Docstring

### Summary
Preprocesses raw historical price data for downstream analysis.

### Parameters

- **dates** (List[str]): List of ISO‑formatted dates (YYYY-MM-DD) for which price data was retrieved.
- **prices_btc** (List[float]): List of closing prices for BTC aligned with the dates list.
- **prices_eth** (List[float]): List of closing prices for ETH aligned with the dates list.
- **prices_stable** (List[float]): List of closing prices for the chosen stablecoin (e.g., USDT) aligned with the dates list.

### Returns

Dict[str, Any]: A dictionary containing the cleaned and transformed price series, including dates, a unified price list, the count of imputed values, and a flag indicating whether normalization was performed.

### Raises

- ValueError: If the input price lists are of unequal length or contain non‑numeric entries.
- TypeError: If any input parameter is not of the expected type.

### Examples

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
