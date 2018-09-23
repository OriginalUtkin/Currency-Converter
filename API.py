import core
import argparse
from flask import Flask, request, jsonify
# TODO : Вывод в json
# curl -X GET http://127.0.0.1:port/currency_converter?param_value&param_value HTTP/1.1
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

    return str(arguments)


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


if __name__ == '__main__':
    app.run(port=5000)