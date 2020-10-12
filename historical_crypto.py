# -*- coding: utf-8 -*-

import pandas as pd
from pandas import json_normalize
from datetime import date, datetime
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from urllib.error import HTTPError

class HistoricalData(object):
  '''
  This class provides methods for scraping historical price data
  of specified crypto-currencies for specific time periods from
  CoinMarketCap.
   -------------------------------Arguments-------------------------------------------
   
    ticker: information for which the user would like to return (str).
    start_date: a string in the format YYYY-MM-DD (str).
    end_date: a string in the format YYYY-MM-DD (str).

   -------------------------------Returns---------------------------------------------  
   
    data: a Pandas DataFrame which contains requested cryptocurrency data.
  '''

  def __init__(self,
               ticker,
               start_date,
               end_date=None):

    if isinstance(start_date, str) is False:
      raise TypeError("start_date argument must be a string object")

    # Convert date into appropriate format for CoinMarketCap:
    start_date = start_date.replace("-", "")

    # set today's date == end_date unless explicitly specified by user:
    if end_date is None:
      today = date.today()
      date_time = today.strftime("%Y/%m/%d")
      end_date = date_time.replace('-', "")

    elif isinstance(end_date, str) is False:
      raise TypeError("end_date must be a string object")
    
    else:
      end_date = end_date.replace("-", "")

    # Self assign default args
    self.ticker = ticker
    self.start_date = start_date
    self.end_date = end_date

  def _ticker_checker(self, ticker):
    '''
    This internal function verifies and returns the website extension based upon the supplied crypto ticker.
    
    -------------------------------Arguments-------------------------------------------
    
    ticker: information for which the user would like to return (str). 
    
   -------------------------------Returns---------------------------------------------  
   
    N/A
    
    '''

    try:
      all_tickers = "https://coinmarketcap.com/all/views/all/"
      df = pd.read_html(all_tickers)[-1]

      all_ticker_dictionary = df[['Name', 'Symbol']].to_dict('records')

      ticker = ticker.upper()

      for item in all_ticker_dictionary:
        if item['Symbol'] == ticker:
          return item['Name'].lower()

      print("""'{0}' was not found in the top 200 cryptocurrencies. \n
      Please search `https://coinmarketcap.com/coins/` for the correct ticker. \n
      Alternatively, please run the 'find_all_tickers' function to return the appropriate ticker""".format(self.ticker))

    except Exception as e:
      raise e

  def find_all_tickers(self):
    '''
    This function enables retrieval of all cryptocurrency tickers which can be accessed through the class.
    
   -------------------------------Arguments-------------------------------------------
   
    N/A
    
   -------------------------------Returns--------------------------------------------- 

   data: a DataFrame containing the Name and Symbol of all cryptocurrency tickers available through CoinMarketCap.com.
         The 'Symbol' corresponds to the 'ticker' argument for this class.
         
    '''

    url = "https://coinmarketcap.com/all/views/all/"
    all_tickers = pd.read_html(url)[-1]
    data = all_tickers[['Name', 'Symbol']]

    return data

  def retrieve_data(self):
    '''
    This function scrapes and cleans specific data of the specified ticker.
    
   -------------------------------Arguments-------------------------------------------
   
    N/A

   -------------------------------Returns---------------------------------------------  
   
    data: a Pandas DataFrame which contains requested cryptocurrency data.
    
    '''

    collect_ticker = self._ticker_checker(self.ticker)
    custom_url = "https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}".format(collect_ticker,
                                                                                                      self.start_date,
                                                                                                      self.end_date)

    try:
      dataset = pd.read_html(custom_url)
    except:
      raise WrongCoinCode(
        "'{0}' is not available at CoinMarketCap.com. Check website for correct ticker name".format(collect_ticker))

    data = dataset[-2]
    data['Date'] = pd.to_datetime(data['Date'])
    data.rename(
      {
        "Open*": "Open",
        "Close**": "Close",
        "Market Cap": "Market_Cap"
      },
      axis='columns', inplace=True)

    data.set_index('Date', drop=True, inplace=True)
    data.sort_index(inplace=True)
    return data


if __name__ == '__main__':
  HistoricalData(start_date = '', ticker = '').find_all_tickers()

