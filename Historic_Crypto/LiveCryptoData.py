# -*- coding: utf-8 -*-

import pandas as pd
import requests
import json
import sys


class LiveCryptoData(object):
    """
    This class provides methods for obtaining live Cryptocurrency price data,
    including the Bid/Ask spread from the COinBase Pro API.

    :param: ticker: information for which the user would like to return. (str)
    :param: verbose: print progress during extraction, default = True (bool)
    :returns: response_data: a Pandas DataFrame which contains the requested cryptocurrency data. (pd.DataFrame)
    """
    def __init__(self,
                 ticker,
                 verbose=True):

        if verbose:
            print("Checking inputs...")

        if not isinstance(ticker, str):
            raise TypeError("The 'ticker' argument must be a string object.")
        if not isinstance(verbose, (bool, type(None))):
            raise TypeError("The 'verbose' argument must be a boolean or None type.")

        self.verbose = verbose
        self.ticker = ticker

    def _ticker_checker(self):
        """This helper function checks if the ticker is available on the CoinBase Pro API."""
        if self.verbose:
            print("Checking if user supplied is available on the CoinBase Pro API...")

        tkr_response = requests.get("https://api.pro.coinbase.com/products")
        if tkr_response.status_code in [200, 201, 202, 203, 204]:
            if self.verbose:
                print('Connected to the CoinBase Pro API.')
            response_data = pd.json_normalize(json.loads(tkr_response.text))
            ticker_list = response_data["id"].tolist()

        elif tkr_response.status_code in [400, 401, 404]:
            if self.verbose:
                print("Status Code: {}, malformed request to the CoinBase Pro API.".format(tkr_response.status_code))
            sys.exit()
        elif tkr_response.status_code in [403, 500, 501]:
            if self.verbose:
                print("Status Code: {}, could not connect to the CoinBase Pro API.".format(tkr_response.status_code))
            sys.exit()
        else:
            if self.verbose:
                print("Status Code: {}, error in connecting to the CoinBase Pro API.".format(tkr_response.status_code))
            sys.exit()

        if self.ticker in ticker_list:
            if self.verbose:
                print("Ticker '{}' found at the CoinBase Pro API, continuing to extraction.".format(self.ticker))
        else:
            raise ValueError("""Ticker: '{}' not available through CoinBase Pro API. Please use the Cryptocurrencies 
            class to identify the correct ticker.""".format(self.ticker))

    def return_data(self):
        """This function returns the desired output."""
        if self.verbose:
            print("Collecting data for '{}'".format(self.ticker))

        self._ticker_checker()
        response = requests.get("https://api.pro.coinbase.com/products/{}/ticker".format(self.ticker))

        if response.status_code in [200, 201, 202, 203, 204]:
            if self.verbose:
                print("Status Code: {}, successful API call.".format(response.status_code))
            response_data = pd.json_normalize(json.loads(response.text))
            response_data["time"] = pd.to_datetime(response_data["time"])
            response_data.set_index("time", drop=True, inplace=True)
            return response_data
        elif response.status_code in [400, 401, 404]:
            if self.verbose:
                print("Status Code: {}, malformed request to the CoinBase Pro API.".format(response.status_code))
            sys.exit()
        elif response.status_code in [403, 500, 501]:
            if self.verbose:
                print("Status Code: {}, error in connecting to the CoinBase Pro API.".format(response.status_code))
            sys.exit()
        else:
            if self.verbose:
                print("Status Code: {}, error in connecting to the CoinBase Pro API.".format(response.status_code))
            sys.exit()


new = LiveCryptoData('BTC-USD').return_data()
print(new)
