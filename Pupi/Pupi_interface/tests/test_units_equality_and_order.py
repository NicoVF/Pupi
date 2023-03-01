import unittest

from Pupi_interface.business.pupi import UnitForSale, Pupi


class UnitForSaleEqualityAndOrderTest(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def setUp(self):
        self.unit_audi = UnitForSale.create_unit_from(["Audi"])
        self.unit_audi_A1 = UnitForSale.create_unit_from(["Audi", "A1"])
        self.unit_audi_A3 = UnitForSale.create_unit_from(["Audi", "A3"])
        self.unit_fiat = UnitForSale.create_unit_from(["Fiat"])
        self.unit_fiat_palio_nafta = UnitForSale.create_unit_from(["Fiat", "Palio", "Nafta"])
        self.unit_fiat_palio_gnc = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC"])
        self.unit_fiat_palio_gnc_precio150 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "", "150"])
        self.unit_fiat_palio_gnc_precio1000 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "", "1000"])
        self.unit_fiat_palio_gnc_precio250 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "", "250"])
        self.unit_fiat_palio_gnc_anio2015 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2015"])
        self.unit_fiat_palio_gnc_anio2018 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2018"])
        super(UnitForSaleEqualityAndOrderTest, self).setUp()
        self.pupi = Pupi()

    def test01_same_units_with_brand(self):
        self.assertEqual(self.unit_audi, self.unit_audi)

    def test02_different_units_with_model(self):
        self.assertNotEqual(self.unit_audi_A1, self.unit_audi_A3)

    def test03_first_unit_less_than_second_unit_with_model(self):
        self.assertLess(self.unit_audi_A1, self.unit_audi_A3)

    def test04_first_unit_great_than_second_unit_with_model(self):
        self.assertGreater(self.unit_audi_A3, self.unit_audi_A1)

    def test05_same_units_with_version(self):
        self.assertEqual(self.unit_fiat_palio_gnc, self.unit_fiat_palio_gnc)

    def test06_different_units_with_brand(self):
        self.assertNotEqual(self.unit_fiat_palio_gnc, self.unit_fiat_palio_nafta)

    def test07_first_unit_less_than_second_unit_with_version(self):
        self.assertLess(self.unit_fiat_palio_gnc, self.unit_fiat_palio_nafta)

    def test08_first_unit_great_than_second_unit_with_version(self):
        self.assertGreater(self.unit_fiat_palio_nafta, self.unit_fiat_palio_gnc)

    def test09_same_units_with_price(self):
        self.assertEqual(self.unit_fiat_palio_gnc_precio150, self.unit_fiat_palio_gnc_precio150)

    def test10_different_units_with_price(self):
        self.assertNotEqual(self.unit_fiat_palio_gnc_precio150, self.unit_fiat_palio_gnc_precio250)

    def test11_first_unit_less_than_second_unit_with_price(self):
        self.assertLess(self.unit_fiat_palio_gnc_precio150, self.unit_fiat_palio_gnc_precio250)

    def test12_first_unit_great_than_second_unit_with_price(self):
        self.assertGreater(self.unit_fiat_palio_gnc_precio250, self.unit_fiat_palio_gnc_precio150)

    def test13_same_units_with_year(self):
        self.assertEqual(self.unit_fiat_palio_gnc_anio2015, self.unit_fiat_palio_gnc_anio2015)

    def test14_different_units_with_year(self):
        self.assertNotEqual(self.unit_fiat_palio_gnc_anio2015, self.unit_fiat_palio_gnc_anio2018)

    def test15_first_unit_less_than_second_unit_with_year(self):
        self.assertLess(self.unit_fiat_palio_gnc_anio2015, self.unit_fiat_palio_gnc_anio2018)

    def test16_first_unit_great_than_second_unit_with_year(self):
        self.assertGreater(self.unit_fiat_palio_gnc_anio2018, self.unit_fiat_palio_gnc_anio2015)
    def test17_lexicographic_order_of_price_doesnt_matter(self):
        self.assertLess(self.unit_fiat_palio_gnc_precio250, self.unit_fiat_palio_gnc_precio1000)
