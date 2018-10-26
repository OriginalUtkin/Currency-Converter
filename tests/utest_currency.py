import unittest
import argparse
from sample.core import validate_currency, get_currencies_by_symbol


class ValidatingCurrencyTest(unittest.TestCase):

    def test_return(self):
        self.assertEqual(validate_currency("CzK"), "CZK")
        self.assertEqual(validate_currency("czk"), "CZK")
        self.assertEqual(validate_currency("CZK"), "CZK")
        self.assertEqual(validate_currency("руб"), "руб")

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
        self.assertEqual(validate_currency("$"), "$")

    @unittest.skip("just for debugging")
    def test_convert_symb_to_curr(self):
        self.assertEqual(len(get_currencies_by_symbol("руб")), 1)
        self.assertEqual(len(get_currencies_by_symbol("$")), 22)
        self.assertEqual(len(get_currencies_by_symbol("£")), 7)

