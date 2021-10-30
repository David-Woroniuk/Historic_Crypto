from ..Cyptocurrencies import Cryptocurrencies
data = Cryptocurrencies(coin_search='^BTC-USD$', extended_output=False).find_crypto_pairs()
print(data)