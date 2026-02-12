# gather_data PRD

## Description
Collect historical price and volume data for BTC, stable and ETH


## Conceptual Info

The gather_data node serves as the foundational data ingestion step for the cryptocurrency trading workflow. It downloads aligned historical price and volume time series for three key assets—Bitcoin (BTC), a stablecoin (e.g., USDT), and Ethereum (ETH)—from a reliable external provider such as CoinMarketCap or Quandl. These time series are later used for statistical analysis, trend identification, strategy development, backtesting, and hedging.

## Docstring

### Summary
Download and consolidate historical price and volume data for BTC, stable and ETH.

### Parameters

- **source** (str): The name of the data provider (e.g., 'CoinMarketCap', 'Quandl'). The function selects the appropriate API credentials and endpoints based on this value.
- **start_date** (str): ISO 8601 start date for the requested data (e.g., '2022-01-01').
- **end_date** (str): ISO 8601 end date for the requested data (e.g., '2023-01-01').
- **assets** (List[str]): List of asset symbols to fetch (must include 'BTC', 'ETH', and a stablecoin symbol such as 'USDT').

### Returns

Dict[str, List[Union[str, float]]]: A dictionary containing four keys: 'price_dates', 'prices', 'volume_dates', and 'volumes'. The lists are aligned such that the i-th element of each list corresponds to the same calendar day. Dates are ISO 8601 strings; price and volume values are floats.

### Raises

- ConnectionError: Raised if the API endpoint cannot be reached or network issues occur.
- ValueError: Raised if required parameters are missing, the asset list does not contain the mandatory symbols, or the date range is invalid.
- KeyError: Raised if the API response does not include data for one or more requested assets.

### Examples

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
