# Historic Crypto

[![Downloads](https://pepy.tech/badge/historic-crypto)](https://pepy.tech/project/historic-crypto) [![Downloads](https://pepy.tech/badge/historic-crypto/month)](https://pepy.tech/project/historic-crypto)

An open source Python library for scraping Historical Cryptocurrency data.

This library scrapes [coinmarketcap.com][website] to collect historical Cryptocurrency data, returning a Pandas DataFrame. 
The HistoricalData class returns all attributes (Open, Close, High, Low, Volume, Market_Cap) of the selected cryptocurrency, whilst the MultipleHistoricalData accepts a list of cryptocurrencies and returns a single attribute of the corresponding cryptocurrencies.

## Installation

From Python:
```python
pip install Historic-Crypto
from Historic_Crypto import HistoricalData
from Historic_Crypto import MultipleHistoricalData
```

## Usage

If you are unsure of the correct 'ticker' to scrape:
```python
pip install Historic-Crypto
from Historic_Crypto import HistoricalData
HistoricalData(start_date = '', ticker = '').find_all_tickers()
```
Returns a Pandas DataFrame containing the columns "Name" and "Symbol", which indicate the Name - Symbol pairs of available cryptocurrencies. The "Symbol" is required as the corresponding 'ticker' input argument of other class methods:

```python
pip install Historic-Crypto
from Historic_Crypto import HistoricalData

dataset = HistoricalData(start_date = '2013-06-06',
                        end_date = '2015-01-01',
                        ticker = 'BTC').retrieve_data()
```

Returns a Pandas DataFrame 'dataset', which contains the Open, Close, High, Low, Volume and Market Capitalisation of Bitcoin between 2013-06-06 and 2015-01-01, indexed by Date.

```python
pip install Historic-Crypto
from Historic_Crypto import HistoricalData

dataset = HistoricalData(start_date = '2013-06-06',
                        ticker = 'BTC').retrieve_data()
```

Returns a Pandas DataFrame 'dataset', which contains the Open, Close, High, Low, Volume and Market Capitalisation of Bitcoin between 2013-06-06 and today, indexed by Date.

```python
pip install Historic-Crypto
from Historic_Crypto import MultipleHistoricalData

dataset = MultipleHistoricalData(tickers = ['BTC','ETH'], 
                                attribute = 'Open', 
                                start_date = '2015-01-01', 
                                end_date = '2019-01-01').retrieve_data()
```

Returns a Pandas DataFrame 'dataset', which contains the Open 'attribute' of Bitcoin and Etherium between 2015-01-01 and today, indexed by Date. Please note that 'NaN' rows are present in the output, which can be subsequently processed.

## Input Arguments

| Argument | Description |
| ------ | --------- |
| ticker | information for cryptocurrencies which the user would like to return (str). |
| tickers | information for which cryptocurrencies the user would like to return (list). |
| attribute | a string representing the attribute to be returned (From: 'Open','Close','High','Low','Volume','Market_Cap'  (str).  |
| start_date | a string in the format YYYY-MM-DD (str). [optional] |
| end_date | a string in the format YYYY-MM-DD (str). [optional] |


   [website]: <https://coinmarketcap.com/>
