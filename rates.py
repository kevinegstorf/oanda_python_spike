import pandas as pd
import oandapy
import configparser

# INITIAL SETUP
config = configparser.ConfigParser()
config.read('../config/config.ini')

account_id = config['oanda']['account_id']
api_key = config['oanda']['api_key']


# RATES
oanda = oandapy.API(environment='practice',
                    access_token=api_key)
response = oanda.get_prices(instruments = "EUR_USD,NZD_USD,EUR_GBP")

prices = response['prices'][0]['ask']

data = response['prices']
time_stamp = data[0]['time']
instrument = data[0]['instrument']
bid_price = data[0]['bid']
ask_price = data[0]['ask']

print("[{}][{}] bid = {} ask = {}".format(time_stamp,
                                        instrument,
                                        bid_price,
                                        ask_price))

table_print = pd.DataFrame(response['prices'])

print(table_print)

# INSTRUMENTS
response = oanda.get_instruments(account_id)
instruments_table = pd.DataFrame(response['instruments'])
print(instruments_table)

# HISTORY
response = oanda.get_history(instrument="EUR_USD")
# print(response)
history_print = pd.DataFrame(response['candles'])
history_print.columns = ['Close_Ask', 'Close_Bid', 'Complete', 'High_Ask', 'High_Bid', 'Low_Ask', 'Low_Bid',
                            'Open_Ask', 'Open_Bid', 'Time', 'Volume']
# print(history_print.columns)

res = history_print.reindex_axis(['Time', 'Open_Bid', 'Open_Ask',
                        'High_Bid', 'High_Ask', 'Low_Bid',
                        'Low_Ask', 'Close_Bid', 'Close_Ask',
                        'Complete', 'Volume'],
                       axis=1)

# print(res)
print(res.tail())
