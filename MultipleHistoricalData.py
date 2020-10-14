# -*- coding: utf-8 -*-

import pandas as pd
from pandas import json_normalize
from datetime import date, datetime
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from urllib.error import HTTPError


class MultipleHistoricalData(object):
  '''
  This class provides methods for scraping historical price data
  of a list of specified crypto-currencies for specific time periods from
  CoinMarketCap.
   -------------------------------Arguments-------------------------------------------
   
    tickers: information on the security which the user would like to return (list).
    attribute: the attribute which the user would like to return (Open, Close, High, Low, Volume, Market Cap etc.)
    start_date: a string in the format YYYY-MM-DD (str).
    end_date: a string in the format YYYY-MM-DD (str).
   -------------------------------Returns---------------------------------------------  
   
    data: a Pandas DataFrame which contains requested cryptocurrency data.
  '''

  def __init__(self,
               tickers,
               attribute,
               start_date,
               end_date=None):

    # tickers:
    if isinstance(tickers, list) is False:
      raise TypeError("tickers argument must be presented as a list of strings.") 

    all_tickers = "https://coinmarketcap.com/all/views/all/"
    df = pd.read_html(all_tickers)[-1]
    all_ticker_list = df['Symbol'].to_list()
    all_ticker_dict = df[['Name', 'Symbol']].to_dict('records')

    check = all(element in all_ticker_list for element in tickers)
    if check is True:
      print('Collecting data for the list {}.'.format(tickers))
    else:
      raise TypeError("one or more tickers are not available on CoinMarketCap.com.")

    lower_tickers = []
    for item in all_ticker_dict:
      if item['Symbol'] in tickers:
        lower_tickers.append(item['Name'].lower())    

    # attribute:
    if isinstance(attribute, str) is False:
      raise TypeError("attribute argument must be a string object.") 
    while attribute not in ['Open','High','Low','Close','Volume','Market_Cap']:
      raise TypeError("attribute argument must be 'Open','High','Low','Close', 'Volume' or 'Market_Cap'.")

    # start_date:
    if isinstance(start_date, str) is False:
      raise TypeError("start_date argument must be a string object")
    start_date = start_date.replace("-", "")

    # end_date:
    if end_date is None:
      today = date.today()
      date_time = today.strftime("%Y/%m/%d")
      end_date = date_time.replace('-', "")
    elif isinstance(end_date, str) is False:
      raise TypeError("end_date must be a string object")
    else:
      end_date = end_date.replace("-", "")

    # Self assign default args
    self.tickers = tickers
    self.lower_tickers = lower_tickers
    self.attribute = attribute
    self.start_date = start_date
    self.end_date = end_date

  def retrieve_data(self):
    urls = []
    consolidated_data = pd.DataFrame(index = pd.date_range(start = self.start_date, end = self.end_date))
    for ticker in self.lower_tickers:
      custom_url = "https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}".format(ticker,self.start_date,self.end_date)
      urls.append(custom_url)
      dataset = pd.read_html(custom_url)
      data = dataset[-2]
      data['Date'] = pd.to_datetime(data['Date'])
      data.rename(
      {
        "Open*": "Open",
        "Close**": "Close",
        "Market Cap": "Market_Cap"
      },
      axis='columns', inplace=True)

      data.set_index('Date', inplace = True)
      data.sort_index(inplace = True)

      consolidated_data = pd.concat([consolidated_data, data[self.attribute]], axis = 1)
      consolidated_data.rename({self.attribute : ticker+'_'+ self.attribute.lower()}, axis = 'columns', inplace = True)
     
    print("Completed Data extraction of: {}".format(self.tickers))

    return consolidated_data

if __name__ == '__main__':
  data = MultipleHistoricalData(tickers = ['BTC','ETH'], 
                                attribute = 'Open', 
                                start_date = '2018-01-01', 
                                end_date = '2019-01-01').retrieve_data()
