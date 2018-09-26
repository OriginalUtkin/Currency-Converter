# Currency-Converter
The Junior Python Developer practical task. [Read more](https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c)

## Prerequisites

Python 3.6

## Built with
* [Flask 1.0.2](http://flask.pocoo.org/) - The web framework used

## Currency conversion API
Program use the last verion of [this](https://free.currencyconverterapi.com/) API. All supported currencies could be found on [this page](https://free.currencyconverterapi.com/api/v6/currencies)


## Usage 
* CLI
```
./currency_converter.py [--amount <number>] --input_currency <string> [--output_currency <string>]
```
* Web API
```
GET /currency_converter?amount=<number>&input_currency=<string>&output_currency=<string> HTTP/1.1
```

## Input parameters
- `amount` - amount which we want to convert - float value. If isn't set, will be set to 1.
- `input_currency` - input currency - 3 letters name or currency symbol. Required
- `output_currency` - requested/output currency - 3 letters name or currency symbol. If isn't set, program will convert input amount value to often usable currencies as: EUR, USD, RUB, CZK, GBP, AUD, JPY, CHF.

## Program output
- json with following structure.
```
{
    "input": { 
        "amount": <float>,
        "currency": <3 letter currency code>
    }
    "output": {
        <3 letter currency code>: <float>
    }
}
```
- If problem was occured, you will get:
 *  json with following structure using Web API:
```
code: <error code>
text: <error text description>
```

 *  string output using CLI verion:
```
error:<error text description>
```

## Examples

### CLI 
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{   
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2707.36, 
    }
}
```
```
./currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
{   
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.20, 
    }
}
```
```
./currency_converter.py --amount 10.92 --input_currency £ 
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}

{
    "input": {
        "amount": 10.92,
        "currency": "SYP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}
```
### API
```
GET /currency_converter?amount=0.9&input_currency=¥&output_currency=AUD HTTP/1.1
{   
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.20, 
    }
}
```

```
GET /currency_converter?amount=10.92&input_currency=£ HTTP/1.1
0:{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}

1:{
    "input": {
        "amount": 10.92,
        "currency": "SYP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}
```

## Known issues
The free version of [FreeCurencyAPI](https://free.currencyconverterapi.com/) allows you to send just 100 requests per hour. After that you are getting a HTTP response from server with 403 : Forbidden error code.  You have to wait for some time for sending another requests to server. This problem could be solved with buying a premium version of this service.

 ## TODO
 - offline conversion
 - save output data to local machine using CLI version of program
 - cache requests
 - logging  (?)
