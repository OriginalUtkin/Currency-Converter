import core
import argparse
import urllib.request
import json
import constants

# TODO : Значение amount равняется нулю

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

    parsed_arguments['input_currency'] = core.preparing_argument(parsed_arguments['input_currency'])
    parsed_arguments['output_currency'] = core.preparing_argument(parsed_arguments['output_currency'])

    output = core.output(parsed_arguments['amount'], parsed_arguments['input_currency'],
                         parsed_arguments['output_currency'])

    for elem in output:
        print(elem)
