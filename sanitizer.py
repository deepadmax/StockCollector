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

path = os.path.expanduser('~/.remus/stock-data')

parser.add_argument(
    '-s', '--src',
    dest='source',
    default=f'{path}/raw'
)

parser.add_argument(
    '-d', '--dest',
    dest='destination',
    default=f'{path}/clean'
)

parser.add_argument(
    '-v', '--verbose',
    dest='verbose',
    action='store_true'
)

ns = parser.parse_args()

# ---------------



import re

import time
from time import strptime
from datetime import date


def readlines_multiple(paths):
    # Read lines from multiple files as one continuous stream

    for path in paths:
        with open(path, 'r') as f:
            for line in f.read().split('\n'):
                yield line

def get_values(line):
    # Format line into proper objects

    items = line.split(',')

    # Remove the ending, ex. "+01:00", and convert to timestamp
    head, _, _ = items[0].partition('+')
    t = int(time.mktime(strptime(head, '%Y-%m-%d %H:%M:%S')))

    floats = tuple(float(x) for x in items[1:-1])
    volume = int(items[-1])

    return t, floats, volume

def bigrams(lines_iter):
    # Get the values of every two consecutive lines

    a = get_values(next(lines_iter))

    for b in lines_iter:
        if not b:
            break

        b = get_values(b)
        yield a, b
        a = b


# If no symbols are entered, use all in folder.
if ns.symbols == ['*']:
    if os.path.exists(ns.source):
        symbols = os.listdir(ns.source)
    else:
        symbols = []
else:
    symbols = ns.symbols


for symbol in symbols:
    source      = f'{ns.source}/{symbol}'
    destination = f'{ns.destination}/{symbol}'

    if not os.path.exists(source):
        print(f'Warning: {source} could not be found.')
        continue

    if not os.path.exists(destination):
        os.makedirs(destination)

    #  All the CSV files in the symbol folder, in alphabetical order
    csv_names = [fname for fname in sorted(os.listdir(source)) if fname.endswith('.csv')]
    csv_paths = [f'{source}/{fname}' for fname in csv_names]

    # New file name, using the first and the last date
    start = csv_names[ 0].partition('_')[ 0]
    end   = csv_names[-1].partition('_')[-1]
    fname = f'{destination}/{start}_{end}' # .csv is already in end

    # Clear file if it already exists
    open(fname, 'w').close()

    with open(fname, 'a') as f:
        lines_iter = readlines_multiple(csv_paths)

        for a, b in bigrams(lines_iter):
            # Calculate the delta between two frames
            a_t, a_floats, a_volume = a
            b_t, b_floats, b_volume = b

            d_t = b_t - a_t
            d_floats = ','.join([
                str(round(b - a, 10)) for a, b in zip(a_floats, b_floats)])
            d_volume = b_volume - a_volume

            f.write(f'{d_t},{d_floats},{d_volume}\n')
            
    if ns.verbose:
        print(f'Data from {source} has been sanitized and saved in {destination}')