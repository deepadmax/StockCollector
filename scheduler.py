#!/usr/bin/python3

# PARSE ARGUMENTS

import os
import argparse

from argparse import ArgumentTypeError

parser = argparse.ArgumentParser(
    description="Schedule to download stock data from Yahoo! Finance")

parser.add_argument(
    '--period',
    dest='period',
    type=int,
    default=28
)

parser.add_argument(
    '--sym',
    nargs='*',
    dest='symbols',
    default=['BTC-USD']
)

parser.add_argument(
    '-v', '--verbose',
    dest='verbose',
    action='store_true'
)

ns = parser.parse_args()


# Check that values are within limits.

if ns.period > 28:
    raise ArgumentTypeError('Period must be less than or equal to 28.')

if type(ns.symbols) == list:
    for symbol in ns.symbols:
        if type(symbol) != str:
            raise ArgumentTypeError(f'{symbol} is not a string.')
else:
    raise ArgumentTypeError('Symbols is not a list.')

# ---------------



# Connect to MongoDB database
from pymongo import MongoClient
client = MongoClient()
db = client.remus

import schedule
import time

from downloader import download

def download_symbols():
    for symbol, data in download(ns.symbols):
        collection = db[f'stock:{symbol}']
        
        for timestamp, open, high, low, close, volume in data:
            collection.update_one({'_id': timestamp}, {'$set': {
                'open'  : open,
                'high'  : high,
                'low'   : low,
                'close' : close,
                'volume': volume,
                'authentic': True
                
            }}, upsert=True)
        

download_symbols()
schedule.every(ns.period).days.do(download_symbols)
print(f'Program is scheduled to run every {ns.period} days.')

while True:
    schedule.run_pending()
    time.sleep(1)