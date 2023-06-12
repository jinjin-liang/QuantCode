# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 22:48:24 2023

@author: Jinjin Liang
"""

# Importing the yfinance package
import yfinance as yf
 
# Set the start and end date
start_date = '2023-01-01'
end_date = '2023-05-01'
 
# Set the ticker
ticker = 'aapl'
 
# Get the data
data = yf.download(ticker, start_date, end_date)
 
# Print the last 5 rows
print(data.tail())