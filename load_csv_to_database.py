#!/usr/bin/python3

"""
This program is temporary and will only used
during the transition from CSV files to a database.
This can later be discarded.
"""

# Connect to MongoDB database
from pymongo import MongoClient

client = MongoClient()
db = client.remus
collection = db['stock']

import os
import re
from tqdm import tqdm
from datetime import datetime

from csv import reader

remus_path = os.path.expanduser('~/.remus/stock-data/raw')
symbols = os.listdir(remus_path)

for symbol in symbols:
    symbol_path = f'{remus_path}/{symbol}'
    files = [f for f in os.listdir(symbol_path) if f.endswith('.csv')]
    
    print(symbol_path)
    for fname in tqdm(files):
        path_file = f'{symbol_path}/{fname}'
        
        with open(path_file) as f:
            
            for line in f.read().split('\n'):
                if line:
                    _timestamp, _open, _high, _low, _close, _volume = line.split(',')
                    
                    m = re.match(r'.*(\+\d+\:\d+)$', _timestamp)
                    if m:
                        _timestamp = _timestamp[:-len(m.group(1))]
                    _timestamp = datetime.strptime(_timestamp, '%Y-%m-%d %H:%M:%S')
                    
                    _open, _high, _low, _close = map(float, [_open, _high, _low, _close])
                    _volume = int(_volume)
                    
                    collection.update_one({'_id': _timestamp}, {'$set': {
                        'open'  : _open,
                        'high'  : _high,
                        'low'   : _low,
                        'close' : _close,
                        'volume': _volume,
                        'authentic': True
                        
                    }}, upsert=True)