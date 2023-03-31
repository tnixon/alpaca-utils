from datetime import datetime as dt
import configparser
import logging
import os.path

import pandas as pd

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, StockTradesRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

# set up logger
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

# define functions


def day_start_time(day: dt) -> dt:
    return day.replace(hour=0, minute=0, second=0, microsecond=0)


def get_csv_outfile(basdir: str, prefix: str, filedate: dt) -> str:
    return os.path.join(basdir, f"{prefix}_{filedate.date()}.csv")


def parse_secrets(secrets_file, config_section='DEFAULT'):
    config = configparser.ConfigParser()
    config.read(secrets_file_name)
    if config_section in config:
        return config[config_section]
    else:
        raise configparser.NoSectionError(f"Config section {config_section} not found in secrets file {secrets_file}!")


def download_bars(client: StockHistoricalDataClient,
                  symbols: list[str],
                  start_time: dt,
                  end_time: dt,
                  csv_filename: str,
                  frequency: TimeFrameUnit = TimeFrameUnit.Minute) -> None:
    # fetch bars data
    logger.info(f"Fetching bars data...")
    bars_request = StockBarsRequest(symbol_or_symbols=symbols,
                                    start=start_time,
                                    end=end_time,
                                    timeframe=TimeFrame(1, frequency))
    bars = client.get_stock_bars(bars_request)
    logger.info(f"Downloaded bars for {len(bars.data.keys())} symbols")
    # save to CSV
    logger.info(f"Writing bars data to file: {csv_filename}")
    bars.df.to_csv(csv_filename)


def download_todays_bars(client: StockHistoricalDataClient,
                         symbols: list[str]) -> None:
    now = dt.now()
    bars_outfile = get_csv_outfile(output_dir, "bars", now)
    download_bars(client, symbols, day_start_time(now), now, bars_outfile)


def download_quotes(client: StockHistoricalDataClient,
                    symbols: list[str],
                    start_time: dt,
                    end_time: dt,
                    csv_filename: str) -> None:
    # fetch quotes data
    logger.info(f"Fetching quotes data...")
    quotes_request = StockQuotesRequest(symbol_or_symbols=symbols,
                                        start=start_time,
                                        end=end_time)
    quotes = client.get_stock_quotes(quotes_request)
    logger.info(f"Downloaded quotes for {len(quotes.data.keys())} symbols")
    # save to CSV
    logger.info(f"Writing quotes data to file: {csv_filename}")
    quotes.df.to_csv(csv_filename)


def download_todays_quotes(client: StockHistoricalDataClient,
                           symbols: list[str]) -> None:
    now = dt.now()
    quotes_outfile = get_csv_outfile(output_dir, "quotes", now)
    download_quotes(client, symbols, day_start_time(now), now, quotes_outfile)


def download_trades(client: StockHistoricalDataClient,
                    symbols: list[str],
                    start_time: dt,
                    end_time: dt,
                    csv_filename: str) -> None:
    # fetch trades data
    logger.info(f"Fetching trades data...")
    trades_request = StockTradesRequest(symbol_or_symbols=symbols,
                                        start=start_time,
                                        end=end_time)
    trades = client.get_stock_trades(trades_request)
    logger.info(f"Downloaded trades for {len(trades.data.keys())} symbols")
    # save to CSV
    logger.info(f"Writing trades data to file: {csv_filename}")
    trades.df.to_csv(csv_filename)


def download_todays_trades(client: StockHistoricalDataClient,
                           symbols: list[str]) -> None:
    now = dt.now()
    trades_outfile = get_csv_outfile(output_dir, "trades", now)
    download_trades(client, symbols, day_start_time(now), now, trades_outfile)


#
# MAIN
#

# params
secrets_file_name = "alpaca.secrets"
symbols_list = ['T',
                'APA',
                'BBBY',
                'PTEN',
                'X',
                'BB',
                'EQT']
output_dir = os.getcwd()  # replace with path to folder for output

# get API credentials
credentials = parse_secrets(secrets_file_name)

# configure data API client
client = StockHistoricalDataClient(credentials['key'], credentials['secret'])

# fetch bars data
download_todays_bars(client, symbols_list)

# fetch quotes data
download_todays_quotes(client, symbols_list)

# fetch trades data
download_todays_trades(client, symbols_list)
