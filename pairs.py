from Cryptocurrencies import Cryptocurrencies

# Instantiate the class without a specific coin search
crypto = Cryptocurrencies(extended_output=True)
pairs = crypto.find_crypto_pairs()

# Output the resulting DataFrame to a CSV file
pairs.to_csv('crypto_pairs.csv', index=False)
