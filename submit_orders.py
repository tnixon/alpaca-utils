import argparse
import logging
import pandas as pd

from alpaca.trading import TradingClient
from alpaca.trading.requests import OrderRequest, MarketOrderRequest, LimitOrderRequest, StopOrderRequest, StopLimitOrderRequest, TrailingStopOrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce, OrderClass

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
    orders = pd.read_csv(orders_file, sep=',\s*', header=0)
    return orders


def build_order_request(order: pd.Series) -> OrderRequest:
    '''
    Builds an OrderRequest object from the given order
    :param order: the order
    :return: the OrderRequest object
    '''
    #print(f"Parsing order: {order}")
    # get order type
    order_type = OrderType[order['ORDER_TYPE'].upper()]

    # build order request based on order type
    if order_type == OrderType.MARKET:
        return MarketOrderRequest(
            symbol=order['SYMBOL'],
            qty=order['QTY'],
            side=OrderSide[order['ORDER_SIDE'].upper()],
            time_in_force=TimeInForce[order['TIME_IN_FORCE'].upper()])
    elif order_type == OrderType.LIMIT:
        return LimitOrderRequest(
            symbol=order['SYMBOL'],
            qty=order['QTY'],
            side=OrderSide[order['ORDER_SIDE'].upper()],
            time_in_force=TimeInForce[order['TIME_IN_FORCE'].upper()],
            limit_price=order['LIMIT_PRICE'])
    elif order_type == OrderType.STOP:
        return StopOrderRequest(
            symbol=order['SYMBOL'],
            qty=order['QTY'],
            side=OrderSide[order['ORDER_SIDE'].upper()],
            time_in_force=TimeInForce[order['TIME_IN_FORCE'].upper()],
            stop_price=order['STOP_PRICE'])
    elif order_type == OrderType.STOP_LIMIT:
        return StopLimitOrderRequest(
            symbol=order['SYMBOL'],
            qty=order['QTY'],
            side=OrderSide[order['ORDER_SIDE'].upper()],
            time_in_force=TimeInForce[order['TIME_IN_FORCE'].upper()],
            limit_price=order['LIMIT_PRICE'],
            stop_price=order['STOP_PRICE'])
    elif order_type == OrderType.TRAILING_STOP:
        return TrailingStopOrderRequest(
            symbol=order['SYMBOL'],
            qty=order['QTY'],
            side=OrderSide[order['ORDER_SIDE'].upper()],
            time_in_force=TimeInForce[order['TIME_IN_FORCE'].upper()],
            trail_price=order['TRAIL_PRICE'],
            trail_percent=order['TRAIL_PERCENT'])
    else:
        raise ValueError(f"Invalid order type: {order_type}")


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
    for index, order_row in orders.iterrows():
        order_request = build_order_request(order_row)
        print(f"Submitting order: {order_request}")
        order = client.submit_order(order_request)
        print(f"Received order: {order}")