import argparse
from datetime import datetime as dt
import configparser
import logging
import os.path
import re

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
    if len(bars.data) > 0:
        bars.df.to_csv(csv_filename)
    else:
        logger.warning(f"No bars data downloaded!")


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
    if len(quotes.data) > 0:
        quotes.df.to_csv(csv_filename)
    else:
        logger.warning(f"No quotes data downloaded!")


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
    if len(trades.data) > 0:
        trades.df.to_csv(csv_filename)
    else:
        logger.warning(f"No trades data downloaded!")


#
# MAIN
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download financial market data using the Alpaca API')
    parser.add_argument('--secrets',
                        type=str,
                        required=False,
                        default='alpaca.secrets',
                        help='Name of the JSON file containing the Alpaca API key and secret')
    parser.add_argument('--symbols',
                        type=str,
                        required=True,
                        help='Name of the text file containing the list of symbols to download data for')
    parser.add_argument('--start_time',
                        type=dt.fromisoformat,
                        required=False,
                        default=day_start_time(dt.now()),
                        help='Start time for the data download')
    parser.add_argument('--end_time',
                        type=dt.fromisoformat,
                        required=False,
                        default=dt.now(),
                        help='End time for the data download')
    parser.add_argument('--output_dir',
                        type=str,
                        required=False,
                        default=os.getcwd(),
                        help='Name of the directory where the downloaded data will be saved')
    args = parser.parse_args()

    # params
    secrets_file_name = args.secrets
    symbols_list = re.split(r',\s*', args.symbols)
    start_time = args.start_time
    end_time = args.end_time
    output_dir = args.output_dir

    # get API credentials
    credentials = parse_secrets(secrets_file_name)

    # configure data API client
    client = StockHistoricalDataClient(credentials['key'], credentials['secret'])

    # fetch bars data
    download_bars(client,
                  symbols_list,
                  start_time,
                  end_time,
                  get_csv_outfile(output_dir, "bars", start_time))

    # fetch quotes data
    download_quotes(client,
                    symbols_list,
                    start_time,
                    end_time,
                    get_csv_outfile(output_dir, "quotes", start_time))

    # fetch trades data
    download_trades(client,
                    symbols_list,
                    start_time,
                    end_time,
                    get_csv_outfile(output_dir, "trades", start_time))
