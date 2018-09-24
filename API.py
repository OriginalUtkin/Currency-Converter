import core
import argparse
import urllib.error
from flask import Flask, request, jsonify
# TODO : Вывод в json
app = Flask(__name__)


@app.route("/currency_converter", methods=['GET'])
def currency_converter():

    arguments = {
        'amount': set_amount(request.args.get('amount')),
        'input_currency': set_input_currency(request.args.get('input_currency')),
        'output_currency': set_output_currency(request.args.get('output_currency'))
    }

    output = core.output(arguments['amount'], arguments['input_currency'], arguments['output_currency'])
    print(output)

    return jsonify(reults = core.output(arguments['amount'],
                               arguments['input_currency'],
                               arguments['output_currency']))


def set_amount(input_amount):
    """

    :param input_amount:
    :return:
    """
    # default amount value is 1
    if (input_amount is None) or (not input_amount):
        return 1.0

    else:
        return core.validate_amount(input_amount)


def set_input_currency(input_currency):
    """

    :param input_currency:
    :return:
    """
    if (input_currency is None) or (not input_currency):
        raise argparse.ArgumentTypeError("input_currency is required argument")

    else:
        return core.preparing_argument(core.validate_currency(input_currency))


def set_output_currency(output_currency):
    """

    :param output_currency:
    :return:
    """
    if not output_currency:
        output_currency = None

    if output_currency is None:
        return core.preparing_argument(output_currency)

    else:
        return core.preparing_argument(core.validate_currency(output_currency))


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
    return jsonify(error=403, text=(str(exc) + ". This problem has been occurred because you send "
                                               " more than 100 requests per 1 hour. See more on "
                                               " https://free.currencyconverterapi.com/. Premium version"
                                               " could solve this problem."))


if __name__ == '__main__':
    app.run(port=5001)