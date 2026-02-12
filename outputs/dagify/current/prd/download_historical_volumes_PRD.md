# download_historical_volumes PRD

## Description
Retrieve historical volume data for BTC, stable and ETH from a reputable data source such as CoinMarketCap or Quandl.


## Conceptual Info

The node fetches historical daily trading volume data for Bitcoin (BTC), a stablecoin (e.g., USDT), and Ethereum (ETH) from a trusted data provider such as CoinMarketCap or Quandl. It aligns the data by date, ensuring that each list of volumes corresponds to the same chronological sequence. The output is structured to support downstream preprocessing and statistical analysis.

## Docstring

### Summary
Download daily trading volumes for BTC, stablecoin, and ETH from an external API.

### Parameters

- **api_key** (str): API key for authenticating with the data provider.
- **start_date** (str): ISO 8601 start date (YYYY-MM-DD) for the historical period to retrieve.
- **end_date** (str): ISO 8601 end date (YYYY-MM-DD) for the historical period to retrieve.
- **base_url** (str): Base endpoint URL of the data provider API.

### Returns

dict: A dictionary containing six keys:
- btc_dates: List[str] of dates for BTC volume records
- btc_volumes: List[float] of daily BTC volumes
- stablecoin_dates: List[str] of dates for stablecoin volume records
- stablecoin_volumes: List[float] of daily stablecoin volumes
- eth_dates: List[str] of dates for ETH volume records
- eth_volumes: List[float] of daily ETH volumes

### Raises

- ValueError: If start_date is after end_date or dates are not in ISO format.
- ConnectionError: If the API endpoint is unreachable or returns a network error.
- HTTPError: If the API returns a non‑200 HTTP status code.
- KeyError: If the expected volume fields are missing from the API response.

### Examples

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
