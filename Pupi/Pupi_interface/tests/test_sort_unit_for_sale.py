import unittest

from Pupi_interface.business.pupi import UnitForSale, Pupi


class PupiSortUnitForSaleTest(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def setUp(self):
        super(PupiSortUnitForSaleTest, self).setUp()
        self.unit_audi = UnitForSale.create_unit_from(["Audi"])
        self.unit_audi_A1 = UnitForSale.create_unit_from(["Audi", "A1"])
        self.unit_audi_A3 = UnitForSale.create_unit_from(["Audi", "A3"])
        self.unit_fiat = UnitForSale.create_unit_from(["Fiat"])
        self.unit_fiat_palio_nafta = UnitForSale.create_unit_from(["Fiat", "Palio", "Nafta"])
        self.unit_fiat_palio_gnc = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC"])
        self.unit_fiat_palio_gnc_precio150 = UnitForSale.create_unit_from(
            ["Fiat", "Palio", "GNC", "", "150", "ARS", "", "", "", "", "", "", "", "", "", "", "150"])
        self.unit_fiat_palio_gnc_precio250 = UnitForSale.create_unit_from(
        ["Fiat", "Palio", "GNC", "", "250", "ARS", "", "", "", "", "", "", "", "", "", "", "250"])
        self.unit_fiat_palio_gnc_precio350 = UnitForSale.create_unit_from(
            ["Fiat", "Palio", "GNC", "", "350", "ARS", "", "", "", "", "", "", "", "", "", "", "350"])
        self.unit_fiat_palio_gnc_anio2015 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2015"])
        self.unit_fiat_palio_gnc_anio2018 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2018"])
        self.unit_fiat_palio_gnc_anio2015_precio150 = UnitForSale.create_unit_from(
            ["Fiat", "Palio", "GNC", "2015", "150", "ARS", "", "", "", "", "", "", "", "", "", "", "150"])
        self.unit_fiat_palio_gnc_anio2015_precio350 = UnitForSale.create_unit_from(
            ["Fiat", "Palio", "GNC", "2015", "350", "ARS", "", "", "", "", "", "", "", "", "", "", "350"])
        self.unit_fiat_palio_gnc_anio2018_precio150 = UnitForSale.create_unit_from(
            ["Fiat", "Palio", "GNC", "2018", "150", "ARS", "", "", "", "", "", "", "", "", "", "", "150"])
        self.unit_fiat_palio_gnc_anio2018_precio250 = UnitForSale.create_unit_from(
            ["Fiat", "Palio", "GNC", "2018", "250", "ARS", "", "", "", "", "", "", "", "", "", "", "250"])
        self.unit_fiat_palio_gnc_anio2018_precio250_2 = UnitForSale.create_unit_from(
            ["Fiat", "Palio", "GNC", "2018", "250", "ARS", "", "", "", "", "", "", "", "", "", "", "250"])
        self.unit_fiat_palio_gnc_anio2017_precio750 = UnitForSale.create_unit_from(
            ["Fiat", "Palio", "GNC", "2017", "750", "ARS", "", "", "", "", "", "", "", "", "", "", "750"])
        self.pupi = Pupi()

    def test01_sorts_brands(self):
        units = self.example_units_with_brands_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_brands_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test02_sorts_model_with_same_brand(self):
        units = self.example_units_with_models_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_models_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test03_sorts_version_with_same_model(self):
        units = self.example_units_with_versions_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_versions_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test04_sorts_highest_price_first_within_same_version(self):
        units = self.example_units_with_price_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_price_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test05_sorts_highest_year_with_same_price(self):
        units = self.example_units_with_year_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_year_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test06_sorts_units_by_year_with_only_one_year(self):
        units = self.example_units_by_year_with_only_one_year()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_by_year_with_only_one_year_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test07_sorts_units_by_year_with_different_year_and_same_price(self):
        units = self.example_units_by_year_with_different_year_and_same_price()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_by_year_with_only_one_year_and_same_price_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test08_sorts_units_by_year_with_different_year_and_different_price(self):
        units = self.example_units_by_year_with_different_year_and_different_price()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_by_year_with_only_one_year_and_different_price_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test09_sorts_many_units_by_year_with_different_year_and_different_price(self):
        units = self.example_many_units_by_year_with_different_year_and_different_price()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_many_units_by_year_with_only_one_year_and_different_price_sorted()
        self.assertEqual(expected_units, sorted_units)

    def example_units_with_brands_not_sorted(self):
        return [self.unit_fiat,
                self.unit_audi]

    def example_units_with_brands_sorted(self):
        return [self.unit_audi,
                self.unit_fiat]

    def example_units_with_models_not_sorted(self):
        return [self.unit_audi_A3,
                self.unit_audi_A1]

    def example_units_with_models_sorted(self):
        return [self.unit_audi_A1,
                self.unit_audi_A3]

    def example_units_with_versions_not_sorted(self):
        return [self.unit_fiat_palio_nafta,
                self.unit_fiat_palio_gnc]

    def example_units_with_versions_sorted(self):
        return [self.unit_fiat_palio_gnc,
                self.unit_fiat_palio_nafta]

    def example_units_with_price_not_sorted(self):
        return [self.unit_fiat_palio_gnc_precio250,
                self.unit_fiat_palio_gnc_precio150]

    def example_units_with_price_sorted(self):
        return [self.unit_fiat_palio_gnc_precio150,
                self.unit_fiat_palio_gnc_precio250]

    def example_units_with_year_not_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2018,
                self.unit_fiat_palio_gnc_anio2015]

    def example_units_with_year_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2015,
                self.unit_fiat_palio_gnc_anio2018]

    def example_units_by_year_with_only_one_year(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio250,
                self.unit_fiat_palio_gnc_anio2018_precio150]

    def example_units_by_year_with_only_one_year_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2018_precio250]

    def example_units_by_year_with_different_year_and_same_price(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2015_precio150]

    def example_units_by_year_with_only_one_year_and_same_price_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2015_precio150,
                self.unit_fiat_palio_gnc_anio2018_precio150]

    def example_units_by_year_with_different_year_and_different_price(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2017_precio750]

    def example_units_by_year_with_only_one_year_and_different_price_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2017_precio750,
                self.unit_fiat_palio_gnc_anio2018_precio150]

    def example_many_units_by_year_with_different_year_and_different_price(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2018_precio250,
                self.unit_fiat_palio_gnc_anio2015_precio150,
                self.unit_fiat_palio_gnc_anio2017_precio750,
                self.unit_fiat_palio_gnc_anio2018_precio250_2,
                self.unit_fiat_palio_gnc_anio2015_precio350]

    def example_many_units_by_year_with_only_one_year_and_different_price_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2015_precio150,
                self.unit_fiat_palio_gnc_anio2015_precio350,
                self.unit_fiat_palio_gnc_anio2017_precio750,
                self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2018_precio250,
                self.unit_fiat_palio_gnc_anio2018_precio250_2]
