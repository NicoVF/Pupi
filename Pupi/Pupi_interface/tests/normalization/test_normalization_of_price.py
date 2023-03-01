import unittest

from Pupi_interface.business.pupi import Pupi

class PriceNormalizationTest(unittest.TestCase):

    def setUp(self):
        super(PriceNormalizationTest, self).setUp()
        self.pupi = Pupi()

    def test01_price_is_already_normalized(self):
        csv = self.example_csv_with_price_normalized()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_price_normalized()
        self.assertEqual(expected_csv, normalized_csv)

    def test02_supply_normalized_price_if_absent(self):
        csv = self.example_csv_with_price_normalized_absent()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_price_normalized()
        self.assertEqual(expected_csv, normalized_csv)


    def example_csv_with_price_normalized(self):
        return "Audi,A1,,,1500000,ARS,,,,,,,,,,,1500000"

    def example_csv_with_price_normalized_absent(self):
        return "Audi,A1,,,1500000,ARS,,,,,,,,,,,"

    def example_normalized_csv_with_price_normalized(self):
        return """"Audi","A1","","","1500000","ARS","","","","","","","","","","","1500000\""""
