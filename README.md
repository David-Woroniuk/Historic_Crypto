# Historic Crypto

An open source Python library for scraping Historical Cryptocurrency data.

This library scrapes [coinmarketcap.com][website] to collect historical Cryptocurrency data, returning a Pandas DataFrame. 

## Installation

From Python:
```
pip install Historic-Crypto
from Historic_Crypto import HistoricalData
```

## Usage

If you are unsure of the correct 'ticker' to scrape:

```
pip install Historic-Crypto
from Historic_Crypto import HistoricalData
HistoricalData(start_date = '', ticker = '').find_all_tickers()
```

Returns a Pandas DataFrame containing the columns "Name" and "Symbol", which indicate the Name - Symbol pairs of available cryptocurrencies. The "Symbol" is required as the corresponding 'ticker' input argument of other class methods:


```
pip install Historic-Crypto
from Historic_Crypto import HistoricalData

dataset = HistoricalData(start_date = '2013-06-06',
                        end_date = '2015-01-01',
                        ticker = 'BTC').retrieve_data()
```

Returns a Pandas DataFrame 'dataset', which contains the Open, Close, High, Low, Volume and Market Capitalisation of Bitcoin between 2013-06-06 and 2015-01-01, indexed by Date.


```
pip install Historic-Crypto
from Historic_Crypto import HistoricalData

dataset = HistoricalData(start_date = '2013-06-06',
                        ticker = 'BTC').retrieve_data()
```

Returns a Pandas DataFrame 'dataset', which contains the Open, Close, High, Low, Volume and Market Capitalisation of Bitcoin between 2013-06-06 and today, indexed by Date.

## Input Arguments

| Argument | Description |
| ------ | --------- |
| ticker | information for which the user would like to return (str). |
| start_date | a string in the format YYYY-MM-DD (str). [optional] |
| end_date | a string in the format YYYY-MM-DD (str). [optional] |


 [website]: <https://coinmarketcap.com/>
