import unittest
import main as currency_converter

# TODO: Check negative value
# TODO: Such a big value, wow
# TODO: Arguments are passed to py script as strings -> test them for correct format for float func


class CurrencyConverterTest(unittest.TestCase):

    def test_negative_value(self):
        with self.assertRaises(ValueError):
            currency_converter.validate_amount(-34.14)

    # def test_value(self):
    #     self.assertEqual(currency_converter.validate_amount(10), 10.0)
    #     self.assertEqual(currency_converter.validate_amount(2.11), 2.11)
    #
    # def test_instance_of(self):
    #     self.assertTrue(isinstance(currency_converter.validate_amount(10)), float)
    #     self.assertTrue(isinstance(currency_converter.validate_amount(2.11)), float)
    #
    # def test_string_value(self):
    #     self.assertRaises(ValueError, currency_converter.validate_amount(" "))
    #     # self.assertRaises(ValueError, currency_converter.validate_amount("22.0q"))


if __name__ == '__main__':
    unittest.main()