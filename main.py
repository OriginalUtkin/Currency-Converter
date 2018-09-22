import argparse
import math
import urllib.request
import json
import constants


# TODO: https://free.currencyconverterapi.com/api/v6/convert?q=EUR_RUB&compact=y
# TODO : обрезать значения до двух цифр после запятой


def get_name_symb(empty_value_flag):
    """

    :param empty_value_flag:
    :return: dictionary as [3 letters name]:[currency symbol]
    """

    with urllib.request.urlopen(constants.currencies_list_addr) as json_data:
        all_currencies = json.load(json_data)

    for currency in all_currencies.values():
        if empty_value_flag:
            return {currency_info['id']: currency_info.get('currencySymbol', "").lower() for currency_info in
                    currency.values()}
        else:
            return {currency_info['id']: currency_info.get('currencySymbol').lower() for currency_info in
                    currency.values() if currency_info.get('currencySymbol') is not None}


def get_currencies_by_symbol(symbol):
    """

    :param symbol:
    :return:
    """
    all_currencies = get_name_symb(False)

    for key, value in all_currencies.items():
        return [currency for currency, curr_symbol in all_currencies.items() if curr_symbol == symbol]


def validate_amount(amount):
    """
    Validate amount value
    :param amount: input value for validating which represented by string
    :return: amount value which represented by the float number
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
    :param currency: input value for validating which represented by string
    :return: char currency symbol or currency name in uppercase
    """
    if len(currency) > 3:
        raise argparse.ArgumentTypeError("Input or output currency has a wrong format. Type currency  symbol or "
                                         "3 letters name.")

    curr_name_symb = get_name_symb(True)

    # Check if currency id exists
    if currency.upper() not in curr_name_symb:

        # Check if currency symbol exists
        if currency.lower() not in curr_name_symb.values():
            raise argparse.ArgumentTypeError("Wrong input or output currency value.")

        else:
            return currency
    else:
        return currency.upper()


def parse_converted_value(json_response):
    """
    json response after API request has following format:
    {'<3 curr letters from>_<3 curr letters to>': {'val': <amount>}}
    :param json_response:
    :return:
    """
    for key, value in json_response.items():
        return key[4:7], float(value['val'])


def preparing_argument(argument_value):
    if argument_value is None:
        return constants.often_used_currencies

    if get_currencies_by_symbol(argument_value):
        return get_currencies_by_symbol(argument_value)

    else:
        return [argument_value]


def get_output_json(data):
    """

    :param data:
    :return:
    """


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
                                                  "to all known currencies.", type=validate_currency)

    return vars(parser.parse_args())


if __name__ == '__main__':
    parsed_arguments = parse_args()
    print(parsed_arguments)

    parsed_arguments['input_currency'] = preparing_argument(parsed_arguments['input_currency'])
    parsed_arguments['output_currency'] = preparing_argument(parsed_arguments['output_currency'])

    for input_curr in parsed_arguments['input_currency']:
        currency_output = dict()
        result = list()

        for output_curr in parsed_arguments['output_currency']:
            with urllib.request.urlopen("https://free.currencyconverterapi.com/api/v6/convert?q={0}_{1}&compact=y"
                                        .format(input_curr, output_curr)) as json_response:
                converted_result = parse_converted_value(json.load(json_response))
                currency_output[converted_result[0]] = converted_result[1] * parsed_arguments['amount']

        print({'input': {'amount': parsed_arguments['amount'], 'currency': input_curr},
               'output': {curr: val for curr, val in currency_output.items()}})
