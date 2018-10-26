import argparse
import urllib.error
from flask import Flask, request, jsonify
from sample import core

app = Flask(__name__)


@app.route("/currency_converter", methods=['GET'])
def currency_converter():

    arguments = {
        'amount': set_amount(request.args.get('amount')),
        'input_currency': set_currency(request.args.get('input_currency'), True),
        'output_currency': set_currency(request.args.get('output_currency'))
    }

    output = core.output(arguments['amount'], arguments['input_currency'], arguments['output_currency'])

    return jsonify(output)


def set_amount(input_amount):
    """
    Validate and set the arguments['amount'] value
    :param input_amount: input amount value from HTTP request
    :return: amount value which represented by the float number
    """
    # default amount value is 1
    if (input_amount is None) or (not input_amount):
        return 1.0

    else:
        return core.validate_amount(input_amount)


def set_currency(currency_value, none_flag=False):
    """
    Validate and set arguments['input_currency'] / arguments['output_currency'] value
    :param currency_value: input currency value from HTTP request
    :param none_flag: if is set, raises a exception if currency_value is None.
    :return: list with all currencies codes
    """

    if (currency_value is None) or (not currency_value):

        if none_flag:
            raise argparse.ArgumentTypeError("input_currency is required argument")

        else:
            return core.preparing_argument(None)

    else:
        return core.preparing_argument(core.validate_currency(currency_value))


@app.errorhandler(argparse.ArgumentTypeError)
def catch_ArgumentTypeError_exception(exc):
    return jsonify(error=400, text=(str(exc)))


@app.errorhandler(TypeError)
def catch_ValueError_exception(exc):
    return jsonify(error=400, text=(str(exc)))


@app.errorhandler(404)
def catch_404_exception(exc):
    return jsonify(error=404, text=(str(exc)))


@app.errorhandler(urllib.error.HTTPError)
def catch_forbidden(exc):
    return jsonify(error=403, text=(str(exc) + ". This problem has been occurred because you have sent "
                                               " more than 100 requests per 1 hour. See more on "
                                               " https://free.currencyconverterapi.com/. Premium version"
                                               " could solve this problem."))


if __name__ == '__main__':
    app.run(port=5000)