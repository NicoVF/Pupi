import unittest

from GoogleSpreadsheet import GoogleSpreadsheet
from PreownedReaderFromSpreadsheet import PreownedReaderFromSpreadsheet
from Spreadsheet import Spreadsheet


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self._spreadsheet_factory = RemoteSpreadsheets()

    def test01_AnEmptySpreadsheetOutputsNoFile(self):
        spreadsheet = self.empty_spreadsheet()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_cars = reader.read_preowned()
        self.assertTrue(len(preowned_cars) == 0)

    def test02_ASpreadsheetWithOnlyOneRowOfDataHas1PreOwnedCar(self):
        spreadsheet = self.example_spreadsheet_with_one_row()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_cars = reader.read_preowned()
        self.assertTrue(len(preowned_cars) == 1)

    def test03_ASpreadsheetRowContainsABrandOfAPreOwnedCar(self):
        spreadsheet = self.example_spreadsheet_with_one_row()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_car = reader.read_preowned()[0]
        self.assertEqual("Fiat", preowned_car.brand())

    def test04_ASpreadsheetRowCanContainADifferentBrandOfAPreOwnedCar(self):
        spreadsheet = self.example_spreadsheet()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_car = reader.read_preowned()[0]
        self.assertEqual("Ford", preowned_car.brand())

    def empty_spreadsheet(self):
        return self._spreadsheet_factory.empty_spreadsheet()

    def example_spreadsheet(self):
        return self._spreadsheet_factory.example_spreadsheet()

    def example_spreadsheet_with_one_row(self):
        return self._spreadsheet_factory.example_spreadsheet_with_one_row()


class LocalSpreadsheets:
    def empty_spreadsheet(self):
        return Spreadsheet()

    def example_spreadsheet(self):
        spreadsheet = Spreadsheet()
        spreadsheet.add_row(["Ford"])
        return spreadsheet

    def example_spreadsheet_with_one_row(self):
        spreadsheet = Spreadsheet()
        spreadsheet.add_row(["Fiat"])
        return spreadsheet


class RemoteSpreadsheets:

    def empty_spreadsheet(self):
        return GoogleSpreadsheet('1ESmRbSaV0zURrEFNiPBut0mynSZ45GWSXjgTBbMfjAo')

    def example_spreadsheet_with_one_row(self):
        spreadsheet = Spreadsheet()
        spreadsheet.add_row(["Fiat"])
        return spreadsheet

    def example_spreadsheet(self):
        spreadsheet = Spreadsheet()
        spreadsheet.add_row(["Ford"])
        return spreadsheet


if __name__ == '__main__':
    unittest.main()





