#!/usr/bin/python3

# PARSE ARGUMENTS

import os
import argparse

parser = argparse.ArgumentParser(
    description="Sanitize downloaded stock data into generalised deltas")

parser.add_argument(
    '--sym',
    nargs='*',
    dest='symbols',
    default=['*']
)

parser.add_argument(
    '--start',
    dest='start',
    default=None
)

parser.add_argument(
    '--end',
    dest='end',
    default=None
)

parser.add_argument(
    '--interval',
    dest='interval',
    default=1
)

parser.add_argument(
    '--path',
    dest='path',
    default=os.path.expanduser('~/.remus/training-data')
)

parser.add_argument(
    '-v', '--verbose',
    dest='verbose',
    action='store_true'
)

ns = parser.parse_args()

# ---------------



# Connect to MongoDB database
from pymongo import MongoClient
client = MongoClient()
db = client.remus


# If no symbols are entered, pick all.
if ns.symbols == ['*']:
    symbols = [c[6:] for c in db.list_collection_names() if c.startswith('stock:')]
else:
    symbols = ns.symbols
    

# Create query from start and end datetimes
import datetime

query = {}

if ns.start:
    query['$gte'] = datetime.strptime(ns.start, '%d-%m-%y %H:%M:%S')
if ns.end:
    query['$lte'] = datetime.strptime(ns.end,   '%d-%m-%y %H:%M:%S')

if query:
    query = {'_id': query}
    

# Create directory if it does not exist
if not os.path.exists(ns.path):
    os.makedirs(ns.path)


for symbol in symbols:
    collection = db[f'stock:{symbol}']
    
    docs = [doc for doc in collection.find(query)]
    
    # TODO: Offset docs by interval        
    
    for a, b in zip(docs[0:-1], docs[1:]):
        d_t = int((b['_id'] - a['_id']).total_seconds())
        d_floats = (
            b['open']   - a['open'],
            b['high']   - a['high'],
            b['low']    - a['low'],
            b['close']  - a['close']
        )
        d_volume = b['volume'] - a['volume']
        
        delta = (d_t, *d_floats, d_volume)
        print(delta)
        
    if ns.verbose:
        print(f'SUCCESS MESSAGE!!!')