import argparse
import math
import urllib.request
import json


def get_all_symbols(json_data):
    """

    :param all_currencies:
    :return:
    """

    for currency in json_data.values():
        return {currency_info['id']: currency_info.get('currencySymbol') for currency_info in
                currency.values() if currency_info.get('currencySymbol') is not None}


def validate_amount(amount):
    """

    :param amount:
    :return:
    """

    if not amount:
        raise argparse.ArgumentTypeError("Amount value represented by empty string.")

    try:
        amount = float(amount)

        if amount < 0:
            raise argparse.ArgumentTypeError("Amount value should be a non-negative value.")

        if math.isnan(amount) or math.isinf(amount):
            raise argparse.ArgumentTypeError("Amount value is not a number.")

    except ValueError:
        raise

    return amount


def validate_currency(currency):
    """
    Validate input and output currency symbol or 3 letters name
    :param currency:
    :return: char symbol or currency name in uppercase
    """
    # currencyID = currency.upper()

    if len(currency) > 3:
        raise argparse.ArgumentTypeError("Input or output currency has a wrong format. Type currency  symbol or "
                                         "3 letters name.")

    with urllib.request.urlopen("https://free.currencyconverterapi.com/api/v6/currencies") as allCurrencies:
        json_data = json.load(allCurrencies)

        # Check if currency id exists
        if len(currency) == 3:

            if currency.upper() not in json_data['results']:
                raise argparse.ArgumentTypeError("Wrong input or output currency name.")
            else:
                return currency.upper()

        # Check if currency symbol exists
        else:
            all_symbols = get_all_symbols(json_data)

            if currency not in all_symbols.values():
                raise argparse.ArgumentTypeError("Wrong input or output currency symbol.")
            else:
                # TODO: convert currency symbol to 3 letters currency name
                return currency

    return currency


def parse_args():

    """
    Configure argparse object for working with input arguments
    :return: dictionary which has a following format -> input_argument_name: argument_value
    """

    parser = argparse.ArgumentParser(description="Process input arguments for currency converter")

    parser.add_argument('--amount', help="Converting amount. Should be a number value. If this parameter is missing"
                                         ", program will set this value to 1", default=1, type=validate_amount)

    parser.add_argument('--input_currency', help="Input currency for converting. Should be represented by 3 letters "
                                                 "name or currency symbol", required=True, type=validate_currency)

    parser.add_argument('--output_currency', help="Output currency. 3 letters or currency symbol."
                                                  "If this parameter is missing, program will convert "
                                                  "to all known currencies.")

    return vars(parser.parse_args())


if __name__ == '__main__':
    parsed_arguments = parse_args()
    print(parse_args())