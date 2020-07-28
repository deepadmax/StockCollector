#!/usr/bin/python3

import os
import re

import yfinance as yf
import pandas as pd

import time, datetime
from datetime import date, timedelta, timezone



def download(symbols, period=29, verbose=False):
    # Download the last month of stock data
    # from Yahoo! Finance for a list of stock symbols.

    ## Deltas for different time spans.
    dPeriod = timedelta(days=period)
    dWeek = timedelta(days=7)
    dDay = timedelta(days=1)

    today = date.today()

    for symbol in symbols:
        ticker = yf.Ticker(symbol)

        # Start and end of entire time span
        start = today - dPeriod
        end = today + dDay

        # Beginning and end of the moving timeframe
        a = start
        b = a + dWeek

        dataframes = []

        while a < end:
            a_string = str(a)
            b_string = str(b)
            
            data = ticker.history(
                start=a_string,
                end=b_string,
                interval='1m',
                actions=False
            )

            if not data.empty:
                i = a_string
                j = str(b-dDay if b<end else end)

                if verbose:
                    print(f'\033[0mAcquired timeframe \033[33m{i} \033[0m-> ' +\
                          f'\033[33m{j} \033[0mfor \033[32m{symbol}\033[0m')

                dataframes.append(data.loc[i:j])

            a = b - dDay
            b = a + dWeek
        
        
        data = []
        for timestamp, series in pd.concat(dataframes).iterrows():
            t = timestamp.to_pydatetime()
            # Convert to UTC and remove DST
            t = t.replace(tzinfo=timezone.utc) - t.dst()
            
            floats, volume = series[:-1], int(series[-1])
            
            data.append([t, *floats, volume])
            
        yield symbol, data[:-1]

    if verbose:
        print(f'Minute data for the past {period} days has been downloaded.')