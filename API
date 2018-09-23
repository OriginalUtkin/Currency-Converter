import core
import argparse
from flask import Flask, request, jsonify

# curl -X GET http://127.0.0.1:port/currency_converter?param_value&param_value HTTP/1.1
app = Flask(__name__)


@app.route("/currency_converter", methods=['GET'])
def currency_converter():

    amount = core.validate_amount(request.args.get('amount'))
    input_currency = core.validate_currency(request.args.get('input_currency'))
    # output_currency = core.validate_currency(request.args.get('output_currency'))

    return "OK"


@app.errorhandler(argparse.ArgumentTypeError)
def catch_ArgumentTypeError_exception(exc):
    return jsonify(error=400, text=(str(exc)))


@app.errorhandler(ValueError)
def catch_ValueError_exception(exc):
    return jsonify(error=400, text=(str(exc)))


@app.errorhandler(404)
def catch_404_exception(exc):
    return jsonify(error=404, text=(str(exc)))


if __name__ == '__main__':
    app.run(port=5000)