# -*- coding: utf-8 -*-

!pip install requests
import pandas as pd
import requests
import json
from tqdm import tqdm_notebook as tqdm

class LiveCryptoData(object):
  '''
  This class provides a method for obtaining live Cryptocurrency price
  data, including the bid/ask spread from the CoinBase Pro API.
  -------------------------------Arguments-------------------------------------------
   
  ticker: information for which the user would like to return (str).
  verbose: print progress during extraction, default = True (bool). (Default:True)
  -------------------------------Returns---------------------------------------------  
   
  data: a Pandas DataFrame which contains the requested cryptocurrency data.
  '''

  def __init__(self,
               ticker,
               verbose = True):
    
    if verbose:
      pbar = tqdm(range(4), desc='tqdm 400px', ncols='1000px')
      pbar.set_description("Checking if string object.")

    if isinstance(ticker, str) is False:
      raise TypeError("The 'ticker' argument must be a string object.")

    self.verbose = verbose
    if verbose:
      self.pbar = pbar
    self.ticker = ticker

  def _ticker_checker(self):
    '''This internal funciton checks if the ticker is available within the list of tickers.'''
    if self.verbose:
      self.pbar.update()
      self.pbar.set_description("Checking if ticker supplied is available on the CoinBase Pro API.")
    
    ticker_response = requests.get("https://api.pro.coinbase.com/products")
    if ticker_response.status_code == 200 and self.verbose:
      self.pbar.update()
      self.pbar.set_description('Connected to the CoinBase Pro API.')
    elif ticker_response.status_code == 404 and self.verbose:
      print('Error code 404, could not connect to the CoinBase API.')
    
    ticker_response_lists = json.loads(ticker_response.text)
    ticker_data = pd.DataFrame(ticker_response_lists)
    ticker_list = ticker_data["id"].tolist()
    if self.ticker in ticker_list:
      if self.verbose:
        self.pbar.update()
        self.pbar.set_description("Ticker '{0}' found at the CoinBase Pro API, continuing to extraction.".format(self.ticker))
    else:
      raise ValueError("""Ticker: '{0}' not available at the CoinBase Pro API. Please use the Cryptocurrencies class to identify the correct ticker.""".format(self.ticker))

  def return_data(self):
    '''This function returns the desired output.'''
    if self.verbose:
      self._ticker_checker()
      self.pbar.update()
      self.pbar.set_description("Collecting data for '{}'".format(self.ticker))
    
    response = requests.get(("https://api.pro.coinbase.com/products/{}/ticker").format(self.ticker))
    if response.status_code == 200:
      response_dictionary= json.loads(response.text)
      data = pd.DataFrame.from_dict(response_dictionary, orient='index').T
      data["time"] = pd.to_datetime(data["time"])
      data.set_index("time", drop = True, inplace = True)
    else:
      raise ValueError("API Error: {}".format(response.status_code))
    return data
      
new =  LiveCryptoData('ATOM-USD').return_data()
new
