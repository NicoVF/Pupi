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

    def test03_dots_in_price_are_removed(self):
        csv = self.example_csv_with_price_with_dots()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_price_normalized()
        self.assertEqual(expected_csv, normalized_csv)

    def test04_commas_in_price_are_removed(self):
        csv = self.example_csv_with_price_with_commas()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_price_normalized()
        self.assertEqual(expected_csv, normalized_csv)

    def test05_price_contains_cents_in_english(self):
        csv = self.example_csv_with_price_with_cents_in_english()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_price_normalized()
        self.assertEqual(expected_csv, normalized_csv)

    def test06_price_contains_cents_in_arg(self):
        csv = self.example_csv_with_price_with_cents_in_arg()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_price_normalized()
        self.assertEqual(expected_csv, normalized_csv)

    def test07_when_price_is_ambiguous_normalization_fails(self):
        csv = self.example_csv_with_ambiguous_price()
        normalization_failed = False
        try:
            self.pupi.normalize_csv(csv)
        except ValueError:
            normalization_failed = True
        self.assertTrue(normalization_failed)

    def test08_when_price_is_not_a_number_normalization_fails(self):
        csv = self.example_csv_with_price_is_not_a_number()
        normalization_failed = False
        try:
            self.pupi.normalize_csv(csv)
        except ValueError:
            normalization_failed = True
        self.assertTrue(normalization_failed)

    def test09_when_price_is_contains_money_symbol(self):
        csv = self.example_csv_with_price_with_money_symbol()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_price_normalized()
        self.assertEqual(expected_csv, normalized_csv)

    def example_csv_with_price_normalized(self):
        return "Audi,A1,,,1500000,ARS,,,,,,,,,,,1500000"

    def example_csv_with_price_normalized_absent(self):
        return "Audi,A1,,,1500000,ARS,,,,,,,,,,,"

    def example_csv_with_price_with_dots(self):
        return "Audi,A1,,,1.500.000,ARS,,,,,,,,,,,"

    def example_csv_with_price_with_commas(self):
        return "Audi,A1,,,\"1,500,000\",ARS,,,,,,,,,,,"

    def example_csv_with_price_with_cents_in_english(self):
        return "Audi,A1,,,\"1,500,000.00\",ARS,,,,,,,,,,,"

    def example_csv_with_price_with_cents_in_arg(self):
        return "Audi,A1,,,\"1,500,000.00\",ARS,,,,,,,,,,,"

    def example_csv_with_ambiguous_price(self):
        return "Audi,A1,,,\"1,500\",ARS,,,,,,,,,,,"

    def example_csv_with_price_with_money_symbol(self):
        return "Audi,A1,,,$1500000,ARS,,,,,,,,,,,"

    def example_csv_with_price_with_symbols(self):
        return "Audi,A1,,,AR$1500000,ARS,,,,,,,,,,,"

    def example_csv_with_price_is_not_a_number(self):
        return "Audi,A1,,,todos los chistes de gallegos son anecdotas,ARS,,,,,,,,,,,"

    def example_normalized_csv_with_price_normalized(self):
        return """"Audi","A1","","","1500000","ARS","","","","","","","","","","","1500000\""""




