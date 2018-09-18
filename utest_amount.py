import unittest
import argparse
from main import validate_amount


class ValidatingAmountTest(unittest.TestCase):

    def test_value(self):
        self.assertEqual(validate_amount(10), 10.0)
        self.assertEqual(validate_amount(2.11), 2.11)

    def test_negative_value(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_amount(-34.14)

    def test_NaN(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_amount(float('NaN'))

    def test_Inf(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_amount(float('Inf'))

    def test_string_value(self):
        with self.assertRaises(ValueError):
            validate_amount("22.0qw")

    @unittest.skip
    def test_empty_string(self):
        with self.assertRaises(ValueError):
            validate_amount(" ")

    def test_instance_of(self):
        self.assertTrue(isinstance(validate_amount(10), float))
        self.assertTrue(isinstance(validate_amount(2.11), float))


if __name__ == '__main__':
    unittest.main()