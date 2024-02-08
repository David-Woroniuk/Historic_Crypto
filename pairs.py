from Cryptocurrencies import Cryptocurrencies

# Instantiate the class without a specific coin search
crypto = Cryptocurrencies(extended_output=True)
pairs = crypto.find_crypto_pairs()

# Print the resulting DataFrame
print(pairs)
