import argparse
import math


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

    :param currency:
    :return:
    """
    return " "


def parse_args():

    """
    Configure argparse object for working with input arguments
    :return: dictionary which has a following format -> input_argument_name: argument_value
    """

    parser = argparse.ArgumentParser(description="Process input arguments for currency converter")

    parser.add_argument('--amount', help="Converting amount. Should be a number value. If this parameter is missing"
                                         ", program will set this value to 1", default=1, type=validate_amount)

    parser.add_argument('--input_currency', help="Input currency for converting. Should be represented by 3 letters "
                                                 "name or currency symbol", required=True)

    parser.add_argument('--output_currency', help="Output currency. 3 letters or currency symbol."
                                                  "If this parameter is missing, program will convert "
                                                  "to all known currencies.")

    return vars(parser.parse_args())


if __name__ == '__main__':
    parsed_arguments = parse_args()