# -*- coding: utf-8 -*-

import pandas as pd
from pandas import json_normalize
from datetime import date, datetime
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from urllib.error import HTTPError
from tqdm import tqdm

class LiveCryptoData(object):
  '''
  This class provides methods for obtaining live Cryptocurrency price
  data from CoinMarketCap.

    -------------------------------Arguments-------------------------------------------
   
    ticker: information for which the user would like to return (str).
    verbose: print progress during extraction, default = True (bool).
   -------------------------------Returns---------------------------------------------  
   
    price_data: a Pandas DataFrame which contains the requested cryptocurrency data.

  '''

  def __init__(self,
               ticker,
               verbose = False):
    
    if verbose:
      pbar = tqdm(total = 3)
      pbar.set_description("Checking if string object")

    if isinstance(ticker, str) is False:
      raise TypeError("The 'ticker' argument must be a string object.")

    if verbose:
      pbar.update()
      pbar.set_description("Checking if ticker available at Coinmarketcap.com")

    all_tickers = pd.read_html("https://coinmarketcap.com/all/views/all/")[-1]
    if ticker not in all_tickers['Symbol'].to_list():
      raise ValueError("""'{0}' was not found in the top 200 cryptocurrencies. \n
      Please search 'https://coinmarketcap.com/coins/' for the correct ticker. \n
      Alternatively, please run the 'find_all_tickers' function to return the appropriate ticker""".format(ticker))
    
    if verbose:
      pbar.update()
      self.pbar = pbar
    
    self.ticker = ticker
    self.verbose = verbose
    self.all_tickers = all_tickers

  def retrieve_market_data(self):
    '''
    This function retrieves the requested data.
    '''
    if self.verbose:
      self.pbar.set_description("Extracting market data from Coinmarketcap.com")
      self.pbar.update()
      
    for item in self.all_tickers['Symbol']:
      if item == self.ticker:
        price_data = self.all_tickers.loc[self.all_tickers['Symbol'] == item]
        return price_data[['Price', 'Market Cap', '% 1h', '% 24h']]


if __name__ == 'main':
  new = LiveCryptoData('BTC', verbose = True).retrieve_market_data()
  new
