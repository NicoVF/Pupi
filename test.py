import unittest


class MyTestCase(unittest.TestCase):
    def test01_AnEmptySpreadsheetOutputsNoFile(self):
        spreadsheet = self.new_empty_spreadsheet()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_cars = reader.read_preowned()
        self.assertTrue(len(preowned_cars) == 0)

    def test02_ANoneEmptySpreadsheetOutputAFile(self):
        spreadsheet = self.example_spreadsheet()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_cars = reader.read_preowned()
        self.assertTrue(len(preowned_cars) > 0)

    def test03_xxx(self):
        spreadsheet = self.example_spreadsheet()
        reader = PreownedReaderFromSpreadsheet(spreadsheet)
        preowned_car = reader.read_preowned()[0]
        self.assertEqual("Ford", preowned_car.brand())

    def new_empty_spreadsheet(self):
        return None

    def example_spreadsheet(self):
        return "Hola"


if __name__ == '__main__':
    unittest.main()


class PreownedCar:

    def brand(self):
        return "Ford"


class PreownedReaderFromSpreadsheet:
    def __init__(self, spreadsheet):
        self._spreadsheet = spreadsheet

    def read_preowned(self):
        if self._spreadsheet is None:
            return []
        return [PreownedCar()]
