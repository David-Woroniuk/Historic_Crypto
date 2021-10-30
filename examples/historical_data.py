from ..HistoricalData import HistoricalData

new = HistoricalData('BTC-USD', 3600, '2021-06-01-00-00', '2021-07-01-00-00').retrieve_data()
print(new.head())
print(new.tail())
