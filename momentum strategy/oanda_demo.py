# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 23:36:44 2023

@author: Jinjin
"""

import configparser

# v20 OANDA API - 3rd party
import json
from oandapyV20 import API    # the client
import oandapyV20.endpoints.trades as trades

config = configparser.ConfigParser()
config.read('oanda.cfg')

client = API(access_token=config['oanda']['access_token'])

import pandas as pd
import datetime
from dateutil import parser
import oandapyV20.endpoints.instruments as instruments

# The v20 api handles from times a little differently - be careful of the timezone
params={"from": parser.parse("2016-12-07 18:00:00 EDT").strftime('%Y-%m-%d'),
        "to": parser.parse("2016-12-10 00:000:00 EDT").strftime('%Y-%m-%d'),
        "granularity":'M1',
        "price":'A'}


r = instruments.InstrumentsCandles(instrument="EUR_USD",params=params)
data = client.request(r)
results= [{"time":x['time'],"closeAsk":float(x['ask']['c'])} for x in data['candles']]
df = pd.DataFrame(results).set_index('time')

df.index = pd.DatetimeIndex(df.index)

df.info()


import numpy as np

df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1))

cols = []

for momentum in [15, 30, 60, 120]:
    col = 'position_%s' % momentum
    df[col] = np.sign(df['returns'].rolling(momentum).mean())
    cols.append(col)