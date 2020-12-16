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

class Cryptocurrencies(object):
  '''
  This class provides methods for finding all available Cryptocurrency
  products within the CoinBase pro API.

  -------------------------------Arguments-------------------------------------------

  extended_output: displays either a condensed or extended output (Bool) (Default = False).
  verbose: prints status messages (Bool) (Default = True).
  coin_search: search for a specific cryptocurrency string (str) (Default = None).

  -------------------------------Returns--------------------------------------------- 

  data: a Pandas DataFrame containing either the extended or condensed output (DataFrame).
  '''

  def __init__(self,
               extended_output = False,
               coin_search = None,
               verbose = True):
    
    if coin_search is not None:
      if isinstance(coin_search, str) is False:
        raise TypeError("'coin_search' argument must either be empty, or a string type.")
    
    self.extended_output = extended_output
    self.coin_search = coin_search
    self.verbose = verbose

  def find_crypto_pairs(self):
    '''
    This function returns all cryptocurrency pairs available at the CoinBase Pro API.
    '''

    response = requests.get("https://api.pro.coinbase.com/products")
    if response.status_code == 200 and self.verbose:
      print('Connected to the CoinBase Pro API.')
    elif response.status_code == 404 and self.verbose:
      print('Error code 404, could not connect to the CoinBase API.')
    
    response_lists = json.loads(response.text)
    data = pd.DataFrame(response_lists)

    if self.coin_search != None:
      outcome = data[data['id'].str.contains(self.coin_search)]
      if outcome.empty == False:
        if self.verbose:
          print("Found {} instances containing the term {}.".format(outcome.shape[0],self.coin_search))
      else:
        if self.verbose:
          print("Unable to find specific search term, returning all available terms.")

    if self.extended_output:
      return data
    else:
      data.drop(['base_currency','quote_currency','base_min_size','base_max_size','quote_increment',
                'base_increment','min_market_funds','max_market_funds','margin_enabled','post_only',
                'limit_only','cancel_only','trading_disabled','status_message'],axis = 1, inplace = True)
      return data

    
data = Cryptocurrencies(coin_search = 'XLM', extended_output=False).find_crypto_pairs()
data
