import core
import argparse
import math
import urllib.request
import json
import constants


def parse_args():
    """
    Configure argparse object for working with input arguments
    :return: dictionary which has a following format -> input_argument_name: argument_value
    """

    parser = argparse.ArgumentParser(description="Process input arguments for currency converter")

    parser.add_argument('--amount', help="Converting amount. Should be a number value. If this parameter is missing"
                                         ", program will set this value to 1", default=1, type=core.validate_amount)

    parser.add_argument('--input_currency', help="Input currency for converting. Should be represented by 3 letters "
                                                 "name or currency symbol", required=True, type=core.validate_currency)

    parser.add_argument('--output_currency', help="Output currency. 3 letters or currency symbol."
                                                  "If this parameter is missing, program will convert "
                                                  "to all known currencies.", type=core.validate_currency)

    return vars(parser.parse_args())


if __name__ == '__main__':
    parsed_arguments = parse_args()
    print(parsed_arguments)

    parsed_arguments['input_currency'] = core.preparing_argument(parsed_arguments['input_currency'])
    parsed_arguments['output_currency'] = core.preparing_argument(parsed_arguments['output_currency'])

    for input_curr in parsed_arguments['input_currency']:

        currency_output = dict()
        result = list()

        for output_curr in [value for value in parsed_arguments['output_currency'] if value != input_curr]:

            with urllib.request.urlopen("https://free.currencyconverterapi.com/api/v6/convert?q={0}_{1}&compact=y"
                                        .format(input_curr, output_curr)) as json_response:
                converted_result = core.parse_converted_value(json.load(json_response))
                currency_output[converted_result[0]] = float('{:.2f}'.format(converted_result[1]
                                                                             * parsed_arguments['amount']))
        json_output = json.dumps(
                        {
                            "input": {
                                    "amount": parsed_arguments['amount'],
                                    "currency": input_curr
                            },
                            "output": {
                                    curr: val for curr, val in currency_output.items()
                                }
                        })

        print(json_output)
