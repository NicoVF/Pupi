import unittest

from Pupi_interface.business.pupi import Pupi


class NormalizationToCommonCurrencyTest(unittest.TestCase):

    def setUp(self):
        super(NormalizationToCommonCurrencyTest, self).setUp()
        self.pupi = Pupi()
        self.pupi.set_usd_in_ars(400)

    def test01_price_is_already_in_common_currency(self):
        csv = self.example_csv_with_price_in_common_currency()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_price_in_common_currency()
        self.assertEqual(expected_csv, normalized_csv)

    def test02_a_price_in_usd_is_normalized_to_common_currency(self):
        csv = self.example_csv_with_price_in_usd()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_price_normalized_in_common_currency()
        self.assertEqual(expected_csv, normalized_csv)

    def test03_another_price_in_usd_is_normalized_to_common_currency(self):
        csv = self.example_csv_with_another_price_in_usd()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_another_price_normalized_in_common_currency()
        self.assertEqual(expected_csv, normalized_csv)

    def example_csv_with_price_in_common_currency(self):
        return "Audi,A1,,,1500000,ARS,,,,,,,,,,,"

    def example_normalized_csv_with_price_in_common_currency(self):
        return """"Audi","A1","","","1500000","ARS","","","","","","","","","","","1500000\""""

    def example_csv_with_price_in_usd(self):
        return "Audi,A1,,,10000,USD,,,,,,,,,,,"

    def example_normalized_csv_with_price_normalized_in_common_currency(self):
        return """"Audi","A1","","","10000","USD","","","","","","","","","","","4000000\""""

    def example_csv_with_another_price_in_usd(self):
        return "Audi,A1,,,20000,USD,,,,,,,,,,,"

    def example_normalized_csv_with_another_price_normalized_in_common_currency(self):
        return """"Audi","A1","","","20000","USD","","","","","","","","","","","8000000\""""


