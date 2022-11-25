import unittest
from PreownedReaderFromSpreadsheet import PreownedReaderFromSpreadsheet
from Spreadsheet import Spreadsheet


class MyTestCase(unittest.TestCase):
    def test01_AnEmptySpreadsheetOutputsNoFile(self):
        spreadsheet = self.new_empty_spreadsheet()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_cars = reader.read_preowned()
        self.assertTrue(len(preowned_cars) == 0)

    def test02_xx(self):
        spreadsheet = self.example_spreadsheet_with_one_row()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_cars = reader.read_preowned()
        self.assertTrue(len(preowned_cars) == 1)

    def test03_xxx(self):
        spreadsheet = self.example_spreadsheet_with_one_row()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_car = reader.read_preowned()[0]
        self.assertEqual("Fiat", preowned_car.brand())

    def test04_xxxx(self):
        spreadsheet = self.example_spreadsheet()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_car = reader.read_preowned()[0]
        self.assertEqual("Ford", preowned_car.brand())

    def new_empty_spreadsheet(self):
        return Spreadsheet()

    def example_spreadsheet(self):
        spreadsheet = Spreadsheet()
        spreadsheet.add_row(["Ford"])
        return spreadsheet

    def example_spreadsheet_with_one_row(self):
        spreadsheet = Spreadsheet()
        spreadsheet.add_row(["Fiat"])
        return spreadsheet



if __name__ == '__main__':
    unittest.main()





