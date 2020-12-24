# -*- coding: utf-8 -*-

!pip install requests
import requests
import json
import time
from random import randint
import pandas as pd
from pandas import json_normalize
from datetime import date, datetime, timedelta
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from urllib.error import HTTPError

class HistoricalData(object):
  '''
  This class provides methods for gathering historical price data of a specified 
  Cryptocurrency between specific time periods. The class utilises the CoinBase Pro
  API to extract historical data, providing a performant method of iteratively calling
  the API. 
  
  PLEASE NOTE THAT HISTORICAL RATE DATA MAY BE INCOMPLETE AS NO DATA IS PUBLISHED
  FOR INTERVALS WHERE THERE ARE NO TICKS.
  
  -------------------------------Arguments-------------------------------------------
   
  ticker: supply the ticker information which you want to return (str).
  granularity: please supply a granularity in seconds (60, 300, 900, 3600, 21600, 86400) (int).
  start_date: a string in the format YYYY-MM-DD-HH-MM (str).
  end_date: a string in the format YYYY-MM-DD-HH-MM (str). (Default: Now)
  verbose: printing during extraction. (Default: True)
   -------------------------------Returns---------------------------------------------  
   
  data: a Pandas DataFrame which contains requested cryptocurrency data.
  '''
  def __init__(self,
               ticker,
               granularity,
               start_date,
               end_date=None,
               verbose = True):
    
    if verbose:
      print("Checking input parameters are in the correct format...")
    
    if isinstance(ticker, str) is False:
      raise TypeError("'ticker' argument must be a string object.")

    if isinstance(granularity, int) is False:
      raise TypeError("'granularity' must be an integer object.")
    while granularity not in [60, 300, 900, 3600, 21600, 86400]:
      raise ValueError("'granularity' argument (seconds) must be selected from 60, 300, 900, 3600, 21600, 86400.")

    if isinstance(start_date, str) is False:
      raise TypeError("'start_date' argument must be a string object.")

    if end_date is None:
      today = date.today()
      end_date = today.strftime("%Y-%m-%d-%H-%M")
    elif isinstance(end_date, str) is False:
      raise TypeError("'end_date' must be a string object.")
    else:
      end_date_datetime = datetime.strptime(end_date, '%Y-%m-%d-%H-%M')
      start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d-%H-%M')
      while start_date_datetime >= end_date_datetime:
        raise ValueError("'end_date' argument cannot occur prior to the start_date argument.")
    
    self.ticker = ticker
    self.granularity = granularity
    self.start_date = start_date
    self.start_datestring = None
    self.end_date = end_date
    self.end_datestring = None
    self.verbose = verbose
   
    
  def _ticker_checker(self):
    '''This internal funciton checks if the ticker is available within the list of tickers.'''
    if self.verbose:
      print("Checking if ticker supplied is available on the CoinBase Pro API...")
    
    ticker_response = requests.get("https://api.pro.coinbase.com/products")
    if ticker_response.status_code == 200 and self.verbose:
      print('Connected to the CoinBase Pro API...')
    elif ticker_response.status_code == 404 and self.verbose:
      print('Error code 404, could not connect to the CoinBase API.')
    
    ticker_response_lists = json.loads(ticker_response.text)
    ticker_data = pd.DataFrame(ticker_response_lists)
    ticker_list = ticker_data["id"].tolist()
    if self.ticker in ticker_list:
      if self.verbose:
        print("Ticker '{0}' found at the CoinBase Pro API, continuing to extraction...".format(self.ticker))
    else:
      raise ValueError("""Ticker: '{0}' not available at the CoinBase Pro API. \n
      Please use the Cryptocurrencies class to identify the correct ticker. \n""".format(self.ticker))


  def _date_cleaner(self, date):
    '''This internal function presents the dates in the format required by the API.'''
    output_line = date[:10] + "T" + date[10:]
    output_line = output_line[:11] + output_line[12:]
    output_line = output_line[:13] + ':' + output_line[14:] + ':00'
    return output_line


  def _date_structurer(self, date):
    '''This internal function acts as a date helper function for data extraction.'''
    date = date.strftime("%Y-%m-%d, %H:%M:%S")
    date = date[:10] +'T'+ date[12:]
    return date


  def retrieve_data(self):
    '''
    This function returns the data.
    '''
    if self.verbose:
      print("Formatting Dates...")

    self._ticker_checker()
    self.start_datestring = self._date_cleaner(self.start_date)
    self.end_datestring = self._date_cleaner(self.end_date)

    start = datetime.strptime(self.start_date, "%Y-%m-%d-%H-%M")
    end = datetime.strptime(self.end_date, "%Y-%m-%d-%H-%M")
    out = abs((end - start).total_seconds())
    number_of_requests = out/self.granularity

    if number_of_requests <= 300:
      response = requests.get("https://api.pro.coinbase.com/products/{0}/candles?start={1}&end={2}&granularity={3}".format(
                                                                                                                      self.ticker,
                                                                                                                      self.start_datestring,
                                                                                                                      self.end_datestring,
                                                                                                                      self.granularity))
      if response.status_code == 200 and self.verbose:
        print('Data Extracted from API...')
      elif response.status_code == 404 and self.verbose:
        raise TypeError("Error status code: 404.")

      response_lists = json.loads(response.text)
      data = pd.DataFrame(response_lists)
      data.columns = ["time","low","high","open","close","volume"]
      data["time"] = pd.to_datetime(data["time"], unit='s')
      data.set_index("time", drop = True, inplace = True)
      data.sort_index(inplace=True)
      return data


    else:
      # The api limit:
      requests_per_message = 300
      data = pd.DataFrame()

      for i in range(int(number_of_requests/requests_per_message)+1):
        provisional_start = start + timedelta(0, (i)*(self.granularity * requests_per_message))
        provisional_start = self._date_structurer(provisional_start)
        provisional_end = start + timedelta(0, (i+1)*(self.granularity * requests_per_message))
        provisional_end = self._date_structurer(provisional_end)
        response = requests.get("https://api.pro.coinbase.com/products/{0}/candles?start={1}&end={2}&granularity={3}".format(
                                                                                                                      self.ticker,
                                                                                                                      provisional_start,
                                                                                                                      provisional_end,
                                                                                                                      self.granularity))
        if response.status_code == 200 and self.verbose:
          print('Data for chunk {0} of {1} extracted'.format(i,int(number_of_requests/requests_per_message)))
        elif response.status_code == 404 and self.verbose:
          raise TypeError("Data for chunk {0} recieved error status code: 404.".format(i))

        if response.status_code == 200:
          response_lists = json.loads(response.text)
          dataset = pd.DataFrame(response_lists)
          if dataset.empty == False:
            data = data.append(dataset)
            time.sleep(randint(0, 3))            
          else:
            print("""CoinBase Pro API did not have any data available for '{0}' beginning at {1}. Trying a later date:'{2}'""".format(self.ticker, 
                                                                                                                                      self.start_date, 
                                                                                                                                      provisional_start))
        else:
          if self.verbose:
            print("Error on chunk {}".format(i))
      
      data.columns = ["time","low","high","open","close","volume"]
      data["time"] = pd.to_datetime(data["time"], unit='s')
      data.set_index("time", drop = True, inplace = True)
      data.sort_index(inplace=True)
      data.drop_duplicates(subset=None, keep='first', inplace=True)
      return data


new = HistoricalData('ETH-USD',300,'2020-06-01-00-00').retrieve_data()
