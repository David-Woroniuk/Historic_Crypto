# Historic Crypto

[![Downloads](https://pepy.tech/badge/historic-crypto)](https://pepy.tech/project/historic-crypto) [![Downloads](https://pepy.tech/badge/historic-crypto/month)](https://pepy.tech/project/historic-crypto)

An open source Python library for the collection of Historical Cryptocurrency data.

This library interacts with the [CoinBase Pro][website] API to:
- List the Cyptocurrency Pairs available through the API.
- Return Live Data from the API
- Return historical data from the API in a Pandas DataFrame.
 

The HistoricalData class returns all attributes (Open, Close, High, Low, Volume) of the selected Cryptocurrency, whilst the Cryptocurrencies class returns all Cryptocurrencies available through the API, with a 'coin_search' parameter if the user wishes to check if that Coin ID is available.

# Installation

From Python:
```python
pip install Historic-Crypto
from Historic_Crypto import HistoricalData
from Historic_Crypto import Cryptocurrencies
from Historic_Crypto import LiveCryptoData
```

# Usage
## Cryptocurrencies 

If you are unsure of the correct 'ticker' to search for:
```python
pip install Historic-Crypto
from Historic_Crypto import Cryptocurrencies

Cryptocurrencies().find_crypto_pairs()
```
Returns a Pandas DataFrame containing the columns "id" and "display_name" and "status", with the "id" column indicating the search term which should be queried by the other classes within the package. 

Additionally, a number of optional arguments can be added:

| Argument | Description |
| ------ | --------- |
| coin_search | search for a specific cryptocurrency string (str) **Default = None**. |
| extended_output | displays either a condensed or extended output (Bool) **Default = False**.|
| verbose | prints status messages (Bool) **Default = True**. |

```python
pip install Historic-Crypto
from Historic_Crypto import Cryptocurrencies

data = Cryptocurrencies(coin_search = 'XLM', extended_output=False).find_crypto_pairs()
```

## HistoricalData

Once you know the ticker which you would like to search for, you can search for it using the HistoricalData class. 
```python
pip install Historic-Crypto
from Historic_Crypto import HistoricalData

new = HistoricalData('ETH-USD',300,'2020-06-01-00-00').retrieve_data()
```
The arguments for the class are listed below:
| Argument | Description |
| ------ | --------- |
| ticker | supply the ticker information which you want to return (str). |
| granularity | please supply a granularity in seconds (60, 300, 900, 3600, 21600, 86400) (int). |
| start_date | a string in the format YYYY-MM-DD-HH-MM (str).  |
| end_date | a string in the format YYYY-MM-DD-HH-MM (str). **Optional, Default: Now** |
| verbose | printing during extraction. **Default: True** |


## LiveCryptoData

If you want to see the current Bid/Ask of a specific Cryptocurrency:

```python
pip install Historic-Crypto
from Historic_Crypto import LiveCryptoData

new =  LiveCryptoData('ATOM-USD').return_data()
```

Returns a Pandas DataFrame 'data', which contains the trade_id, price, size, bid, ask and volume of the previous transaction, indexed by timestamp.

The arguments for the class are listed below:

| Argument | Description |
| ------ | --------- |
| ticker | information for which the user would like to return (str). |
| verbose | print progress during extraction (bool). **Default:True** |


   [website]: <https://pro.coinbase.com/>
