import unittest

from Pupi_interface.business.pupi import Pupi


class PupiNormalizationWhenConvertingCsvToXmlTest(unittest.TestCase):

    def setUp(self):
        super(PupiNormalizationWhenConvertingCsvToXmlTest, self).setUp()
        self.pupi = Pupi()

    def test01_ignore_case_in_brand_name(self):
        csv = self.example_csv_with_two_brands_with_different_case()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_two_brands_with_different_case()
        self.assertEqual(expected_csv, normalized_csv)

    def test02_ignore_case_in_model_name(self):
        csv = self.example_csv_with_two_model_with_different_case()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_two_model_with_different_case()
        self.assertEqual(expected_csv, normalized_csv)

    def test03_replace_comma_with_dot_in_lat_and_long(self):
        csv = self.example_csv_with_model_with_lat_and_long()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_model_with_lat_and_long()
        self.assertEqual(expected_csv, normalized_csv)

    def test04_capitalize_each_word_in_version(self):
        csv = self.example_csv_with_long_version_name()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_long_version_name()
        self.assertEqual(expected_csv, normalized_csv)

    def test05_capitalize_each_word_in_zone(self):
        csv = self.example_csv_with_model_with_zone()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_model_with_zone()
        self.assertEqual(expected_csv, normalized_csv)

    def test06_capitalize_each_word_in_brand(self):
        csv = self.example_csv_with_model()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_model()
        self.assertEqual(expected_csv, normalized_csv)

    def test07_capitalize_each_word_in_brand_and_model(self):
        csv = self.example_csv_with_brand_and_model()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_brand_and_model()
        self.assertEqual(expected_csv, normalized_csv)

    def example_csv_with_two_brands_with_different_case(self):
        return "AUDI\naudi"

    def example_normalized_csv_with_two_brands_with_different_case(self):
        return """"Audi"\n"Audi\""""

    def example_csv_with_two_model_with_different_case(self):
        return "Toyota,COROLLA\ntoyota,coRolla"

    def example_normalized_csv_with_two_model_with_different_case(self):
        return """"Toyota","Corolla"\n"Toyota","Corolla\""""

    def example_csv_with_model_with_lat_and_long(self):
        return "Audi,A1,,,,,,,,,\"-34,3745734\",\"-58,3745734\""

    def example_normalized_csv_with_model_with_lat_and_long(self):
        return """"Audi","A1","","","","","","","","","-34.3745734","-58.3745734\""""

    def example_csv_with_long_version_name(self):
        return "Toyota,COROLLA,1.6 SENSE DRIVE AUTOMATIC\ntoyota,coRolla,1.6 sense drive automatic"

    def example_normalized_csv_with_long_version_name(self):
        return """"Toyota","Corolla","1.6 Sense Drive Automatic"\n"Toyota","Corolla","1.6 Sense Drive Automatic\""""

    def example_csv_with_model_with_zone(self):
        return "Audi,A1,,,,,,,,\"SAN LUIS, Av. del Fundador esq, Las voces del Chorrillero,\""

    def example_normalized_csv_with_model_with_zone(self):
        return """"Audi","A1","","","","","","","","San Luis, Av. Del Fundador Esq, Las Voces Del Chorrillero,\""""

    def example_csv_with_model(self):
        return "Audi,a1 sport"

    def example_normalized_csv_with_model(self):
        return """"Audi","A1 Sport\""""

    def example_csv_with_brand_and_model(self):
        return "Alfa romeo"

    def example_normalized_csv_with_brand_and_model(self):
        return """"Alfa Romeo\""""

    def example_csv_with_brands_not_sorted(self):
        return "Chevrolet\nAudi"

    def example_normalized_csv_with_brands_sorted(self):
        return """"Audi"\n"Chevrolet\""""

    def example_csv_with_models_not_sorted(self):
        return "Audi,B250\nAudi,A1"

    def example_normalized_csv_with_models_sorted(self):
        return """"Audi","A1"\n"Audi","B250\""""

    def example_csv_with_models_not_sorted_and_different_brand(self):
        return "Chevrolet,S10\nAudi,A1"

    def example_normalized_csv_with_models_sorted_and_different_brand(self):
        return """"Audi","A1"\n"Chevrolet","S10\""""

    def example_csv_with_versions_not_sorted(self):
        return "Audi,A1,Bt. Tetronic\nAudi,A1,1.4T Turbo"

    def example_normalized_csv_with_versions_sorted(self):
        return """"Audi","A1","1.4T Turbo"\n"Audi","A1","Bt. Tetronic\""""

    def example_csv_with_same_units_not_sorted(self):
        return "Audi,A1,,,1500000\nAudi,A1,,,2500000"

    def example_normalized_csv_with_same_unit_sorted(self):
        return """"Audi","A1","","","2500000"\n"Audi","A1","","","1500000\""""

    def example_csv_with_same_units_by_year(self):
        return "Audi,A1,,2019\nAudi,A1,,2022"

    def example_normalized_csv_with_same_unit_by_year_sorted(self):
        return """"Audi","A1","","2022"\n"Audi","A1","","2019\""""

    def example_csv_with_same_units_by_year_with_only_one_year(self):
        return "Audi,A1,,\nAudi,A1,,2022"

    def example_normalized_csv_with_same_unit_by_year_sorted_with_only_one_year(self):
        return """"Audi","A1","","2022"\n"Audi","A1","","\""""
