import argparse
import math
import urllib.request
import json
import constants


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

    return [currency for currency, curr_symbol in all_currencies.items() if curr_symbol == symbol]


def validate_amount(amount):
    """
    Validate input amount value
    :param amount: input value for validating which represented by string
    :return: amount value which represented by the float number
    """

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
    """

    :param argument_value:
    :return:
    """

    if argument_value is None:
        return constants.often_used_currencies

    # argument_value is a currency symbol
    if get_currencies_by_symbol(argument_value):
        return get_currencies_by_symbol(argument_value)

    # argument_value is 3 letters name
    else:
        return [argument_value]


def output(amount, input_currency, output_currency):
    """

    :param amount:
    :param input_currency:
    :param output_currency:
    :return:
    """
    result = list()

    for input_curr in input_currency:

        currency_output = dict()

        for output_curr in [value for value in output_currency if value != input_curr]:

            with urllib.request.urlopen(constants.converting_request.format(input_curr, output_curr)) as json_response:
                converted_result = parse_converted_value(json.load(json_response))
                currency_output[converted_result[0]] = float("%.2f" % (converted_result[1] * amount))

        # input and output was equals
        if not currency_output:
            currency_output = {input_currency[0]: amount}

        result.append(
                        {
                            "input": {
                                    "amount": amount,
                                    "currency": input_curr
                            },
                            "output": {
                                    curr: val for curr, val in currency_output.items()
                                }
                        }
                    )

    return result
