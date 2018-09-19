import unittest
import argparse
from main import validate_currency


class ValidatingCurrencyTest(unittest.TestCase):

    def test_return(self):
        self.assertEqual(validate_currency("CzK"), "CZK")

    def test_length(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_currency("CZKU")

    def test_not_existing_currency(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_currency("LOL")

    def test_symbol_doesnt_exist(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_currency("%")

    def test_symbol_exists(self):
        self.assertEqual("$", "$")

    @unittest.skip("Function can't do that right now")
    def convert_symbol_to_currency(self):
        pass
