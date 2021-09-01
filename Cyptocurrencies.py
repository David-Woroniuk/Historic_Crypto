# -*- coding: utf-8 -*-

import requests
import json
import sys
import pandas as pd


class Cryptocurrencies(object):
    """
    This class provides methods for finding all available Cryptocurrency products within
    the CoinBase pro API.

    :param: extended_output: displays either a condensed or extended output, Default = False (Bool).
    :param: prints status messages Default = True (Bool) .
    :param: search for a specific cryptocurrency string Default = None (str) .
    :returns: a Pandas DataFrame containing either the extended or condensed output (DataFrame).
    """
    def __init__(self,
                 extended_output=False,
                 coin_search=None,
                 verbose=True):

        if not all(isinstance(v, (bool, type(None))) for v in [extended_output, verbose]):
            raise TypeError("The 'extended_output' and 'verbose' arguments must either be empty, or boolean types.")
        if not isinstance(coin_search, (str, type(None))):
            raise TypeError("The 'coin_search' argument must either be empty, or a string type.")

        self.extended_output = extended_output
        self.coin_search = coin_search
        self.verbose = verbose

    def find_crypto_pairs(self):
        """This function returns all cryptocurrency pairs available at the CoinBase Pro API."""
        response = requests.get("https://api.pro.coinbase.com/products")
        if response.status_code in [200, 201, 202, 203, 204]:
            if self.verbose:
                print("Connected to the CoinBase Pro API.")
            response_data = pd.json_normalize(json.loads(response.text))
        elif response.status_code in [400, 401, 404]:
            if self.verbose:
                print("Status Code: {}, malformed request to the CoinBase Pro API.".format(response.status_code))
            sys.exit()
        elif response.status_code in [403, 500, 501]:
            if self.verbose:
                print("Status Code: {}, could not connect to the CoinBase Pro API.".format(response.status_code))
            sys.exit()
        else:
            if self.verbose:
                print("Status Code: {}, error in connecting to the CoinBase Pro API.".format(response.status_code))
            sys.exit()

        if self.coin_search:
            outcome = response_data[response_data['id'].str.contains(self.coin_search)]
            if not outcome.empty:
                if self.verbose:
                    print("Found {0} instances containing the term {1}.".format(outcome.shape[0], self.coin_search))
            else:
                outcome = response_data
                if self.verbose:
                    print("Unable to find specific search term, returning all available data.")
        else:
            outcome = response_data

        if self.extended_output:
            if self.verbose:
                print("Extended Output is {}, returning all data.".format(self.extended_output))
            return outcome
        else:
            if self.verbose:
                print("Extended Output is {}, returning reduced dataset.".format(self.extended_output))
            outcome = outcome[['id', 'display_name', 'fx_stablecoin', 'max_slippage_percentage', 'status']]
            return outcome


data = Cryptocurrencies(coin_search='DOGE', extended_output=False).find_crypto_pairs()
print(data)
