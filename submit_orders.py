import argparse
import logging
import pandas as pd

from alpaca.trading import TradingClient

from shared import parse_secrets

# set up logger
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

# define helper functions


def parse_orders(orders_file: str) -> pd.DataFrame:
    '''
    Parses the given orders file and returns the list of orders
    :param orders_file: the orders file name
    :return: the list of orders
    '''
    orders = pd.read_csv(orders_file, sep='\t', header=0)
    return orders


#
# MAIN
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Submit orders to Alpaca')
    parser.add_argument('--secrets',
                        type=str,
                        required=False,
                        default='alpaca.secrets',
                        help='Name of the JSON file containing the Alpaca API key and secret')
    parser.add_argument('--orders',
                        type=str,
                        required=False,
                        default='orders.csv',
                        help='Name of the csv file containing the list of orders to submit')
    args = parser.parse_args()

    # params
    secrets_file_name = args.secrets
    orders_file_name = args.orders

    # get API credentials
    credentials = parse_secrets(secrets_file_name)
    is_paper_api = credentials['endpoint'] == 'https://paper-api.alpaca.markets'

    # set up API client
    client = TradingClient(credentials['key'], credentials['secret'], paper=is_paper_api)

    # get orders
    orders = parse_orders(orders_file_name)

    # submit orders
    for index, order in orders.iterrows():
        print(f"Submitting order: {order}")