import argparse
import math
import urllib.request
import json
import constants


def get_name_symb(empty_value_flag):
    """
    Create a dictionary with currencies names and currencies symbols
    :param empty_value_flag: if a flag is set to true, currencies without currencies symbol will be added to result list
    :return: dictionary with following structure [3 letters name]:[currency symbol]
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
    Get all currencies that is associated with symbol param
    :param symbol: symbol which represents currency
    :return: list with all currencies that is associated with this symbol
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
    Parse received json response. Response has a following format:
    {'<3 curr letters from>_<3 curr letters to>': {'val': <amount>}}
    :param json_response: received json response from server
    :return:currency name and currency rate
    """
    for key, value in json_response.items():
        return key[4:7], float(value['val'])


def preparing_argument(argument_value):
    """
    Prepare input/output currency argument for API request
    :param argument_value: currency name or symbol
    :return: list with currencies
    """

    if argument_value is None:
        return constants.often_used_currencies

    # argument_value is a currency symbol
    if get_currencies_by_symbol(argument_value):
        return get_currencies_by_symbol(argument_value)

    # argument_value is 3 letters name
    else:
        return [argument_value]


def float_output(value):
    """
    Format argument_value to float value with 2 digits after decimal point
    :param value: float value for formatting
    :return: float value with 2 digits after decimal point
    """
    return float(format(value, '.2f'))


def output(amount, input_currency, output_currency):
    """
    Prepare an input and converted data for serializing to json format
    :param amount: input amount value
    :param input_currency: list with all currencies reductions (3 letters name) from --input_currency argument
    :param output_currency: list with all currencies reductions (3 letters name) from --output_currency argument
    :return: prepared serializable string
    """
    result = list()

    for input_curr in input_currency:

        currency_output = dict()

        for output_curr in [value for value in output_currency if value != input_curr]:

            # Okay guys, I can convert this one without API request
            if amount == 0:
                currency_output[output_curr] = float_output(0.00)

            # get currency rate and calculate output result
            else:
                with urllib.request.urlopen(constants.converting_request.format(input_curr, output_curr)) as json_response:
                    converted_result = parse_converted_value(json.load(json_response))
                    currency_output[converted_result[0]] = float_output(converted_result[1] * amount)

        # output currency list contains just a input  currency
        if not currency_output:
            currency_output = {input_currency[0]: amount}

        result.append(
                        {
                            "input": {
                                    "amount": float_output(amount),
                                    "currency": input_curr
                            },
                            "output": {
                                    curr: val for curr, val in currency_output.items()
                                }
                        }
                    )

    return result
