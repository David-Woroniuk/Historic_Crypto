# -*- coding: utf-8 -*-

import requests
import json
import time
from random import randint
import pandas as pd
import sys
from datetime import datetime, timedelta
# from pandas import json_normalize
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# from urllib.error import HTTPError

#     PLEASE NOTE THAT HISTORICAL RATE DATA MAY BE INCOMPLETE AS NO DATA IS PUBLISHED
#     FOR INTERVALS WHERE THERE ARE NO TICKS.


class HistoricalData(object):
    """
    This class provides methods for gathering historical price data of a specified
    Cryptocurrency between user specified time periods. The class utilises the CoinBase Pro
    API to extract historical data, providing a performant method of data extraction.

    :param: ticker: a singular Cryptocurrency ticker. (str)
    :param: granularity: the price data frequency in seconds, one of: 60, 300, 900, 3600, 21600, 86400. (int)
    :param: start_date: a date string in the format YYYY-MM-DD-HH-MM. (str)
    :param: end_date: a date string in the format YYYY-MM-DD-HH-MM,  Default=Now. (str)
    :param: verbose: printing during extraction, Default=True. (bool)
    :returns: data: a Pandas DataFrame which contains requested cryptocurrency data. (pd.DataFrame)
    """
    def __init__(self,
                 ticker,
                 granularity,
                 start_date,
                 end_date=None,
                 verbose=True):

        if verbose:
            print("Checking input parameters are in the correct format.")
        if not all(isinstance(v, str) for v in [ticker, start_date]):
            raise TypeError("The 'ticker' and 'start_date' arguments must be strings or None types.")
        if not isinstance(end_date, (str, type(None))):
            raise TypeError("The 'end_date' argument must be a string or None type.")
        if not isinstance(verbose, bool):
            raise TypeError("The 'verbose' argument must be a boolean.")
        if isinstance(granularity, int) is False:
            raise TypeError("'granularity' must be an integer object.")
        if granularity not in [60, 300, 900, 3600, 21600, 86400]:
            raise ValueError("'granularity' argument must be one of 60, 300, 900, 3600, 21600, 86400 seconds.")

        if not end_date:
            end_date = datetime.today().strftime("%Y-%m-%d-%H-%M")
        else:
            end_date_datetime = datetime.strptime(end_date, '%Y-%m-%d-%H-%M')
            start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d-%H-%M')
            while start_date_datetime >= end_date_datetime:
                raise ValueError("'end_date' argument cannot occur prior to the start_date argument.")

        self.ticker = ticker
        self.granularity = granularity
        self.start_date = start_date
        self.start_date_string = None
        self.end_date = end_date
        self.end_date_string = None
        self.verbose = verbose

    def _ticker_checker(self):
        """This helper function checks if the ticker is available on the CoinBase Pro API."""
        if self.verbose:
            print("Checking if user supplied is available on the CoinBase Pro API.")

        tkr_response = requests.get("https://api.pro.coinbase.com/products")
        if tkr_response.status_code in [200, 201, 202, 203, 204]:
            if self.verbose:
                print('Connected to the CoinBase Pro API...')
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

    def _date_cleaner(self, date_time: (datetime, str)):
        """This helper function presents the input as a datetime in the API required format."""
        if not isinstance(date_time, (datetime, str)):
            raise TypeError("The 'date_time' argument must be a datetime type.")
        if isinstance(date_time, str):
            output_date = datetime.strptime(date_time, '%Y-%m-%d-%H-%M').isoformat()
        else:
            output_date = date_time.strftime("%Y-%m-%d, %H:%M:%S")
            output_date = output_date[:10] + 'T' + output_date[12:]
        return output_date

    def retrieve_data(self):
        """This function returns the data."""
        if self.verbose:
            print("Formatting Dates...")

        self._ticker_checker()
        self.start_date_string = self._date_cleaner(self.start_date)
        self.end_date_string = self._date_cleaner(self.end_date)
        start = datetime.strptime(self.start_date, "%Y-%m-%d-%H-%M")
        end = datetime.strptime(self.end_date, "%Y-%m-%d-%H-%M")

        request_volume = abs((end - start).total_seconds()) / self.granularity

        if request_volume <= 300:
            response = requests.get(
                "https://api.pro.coinbase.com/products/{0}/candles?start={1}&end={2}&granularity={3}".format(
                    self.ticker,
                    self.start_date_string,
                    self.end_date_string,
                    self.granularity))
            if response.status_code == 200 and self.verbose:
                print('Data Extracted from API...')
            elif response.status_code == 404 and self.verbose:
                raise TypeError("Error status code: 404.")

            response_lists = json.loads(response.text)
            data = pd.DataFrame(response_lists)
            data.columns = ["time", "low", "high", "open", "close", "volume"]
            data["time"] = pd.to_datetime(data["time"], unit='s')
            data.set_index("time", drop=True, inplace=True)
            data.sort_index(inplace=True)
            return data

        else:
            # The api limit:
            requests_per_message = 300
            data = pd.DataFrame()

            for i in range(int(request_volume / requests_per_message) + 1):
                provisional_start = start + timedelta(0, i * (self.granularity * requests_per_message))
                provisional_start = self._date_cleaner(provisional_start)
                provisional_end = start + timedelta(0, (i + 1) * (self.granularity * requests_per_message))
                provisional_end = self._date_cleaner(provisional_end)
                response = requests.get(
                    "https://api.pro.coinbase.com/products/{0}/candles?start={1}&end={2}&granularity={3}".format(
                        self.ticker,
                        provisional_start,
                        provisional_end,
                        self.granularity))
                if response.status_code == 200 and self.verbose:
                    print(
                        'Data for chunk {0} of {1} extracted'.format(i, int(request_volume / requests_per_message)))
                elif response.status_code == 404 and self.verbose:
                    raise TypeError("Data for chunk {0} received error status code: 404.".format(i))

                if response.status_code == 200:
                    response_lists = json.loads(response.text)
                    dataset = pd.DataFrame(response_lists)
                    if not dataset.empty:
                        data = data.append(dataset)
                        time.sleep(randint(0, 3))
                    else:
                        print(
                            """CoinBase Pro API did not have any data available for '{0}' beginning at {1}. 
                            Trying a later date:'{2}'""".format(
                                self.ticker,
                                self.start_date,
                                provisional_start))
                else:
                    if self.verbose:
                        print("Error on chunk {}".format(i))

            data.columns = ["time", "low", "high", "open", "close", "volume"]
            data["time"] = pd.to_datetime(data["time"], unit='s')
            data.set_index("time", drop=True, inplace=True)
            data.sort_index(inplace=True)
            data.drop_duplicates(subset=None, keep='first', inplace=True)
            return data


new = HistoricalData('BTC-USD', 3600, '2021-06-01-00-00', '2021-07-01-00-00').retrieve_data()
print(new.head())
print(new.tail())
