import unittest
import argparse
from main import validate_currency


class ValidatingCurrencyTest(unittest.TestCase):

    def test_length(self):
        with self.assertRaises(argparse.ArgumentError):
            validate_currency("CZKU")

    def test_not_existing_currency(self):
        with self.assertRaises(argparse.ArgumentError):
            validate_currency("LOL")
