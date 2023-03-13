from datetime import datetime as dt
import configparser

import pandas as pd

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

# define functions

def parse_secrets(secrets_file, config_section='DEFAULT'):
    config = configparser.ConfigParser()
    config.read(secrets_file_name)
    if config_section in config:
        return config[config_section]
    else:
        raise configparser.NoSectionError(f"Config section {config_section} not found in secrets file {secrets_file}!")

def bars_to_pdf(bars):
    sym_pdfs = map(lambda sym: pd.DataFrame(map(lambda r: r.dict(), bars.data[sym])), bars.data)
    return pd.concat(sym_pdfs)


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
start_date = dt(2010,1,1)
end_date = dt.today()
output_file = "bars.csv"

# get API credentials
credentials = parse_secrets(secrets_file_name)

# configure data API client
client = StockHistoricalDataClient(credentials['key'], credentials['secret'])

# fetch bars data
bars_request = StockBarsRequest(symbol_or_symbols=symbols_list,
                                start=start_date,
                                end=end_date,
                                timeframe=TimeFrame(1,TimeFrameUnit.Day))
bars = client.get_stock_bars(bars_request)

print(f"Loaded records for {len(bars.data)} symbols:")
bars_pdf = bars_to_pdf(bars)
print(f"Loaded {bars_pdf.shape[0]} records")

print(f"Writing to {output_file}")
bars_pdf.to_csv(output_file)
