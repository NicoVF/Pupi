import unittest


class Spreadsheet:
    def __init__(self):
        self._rows = []

    def rows(self):
        return self._rows

    def add_row(self, row):
        self._rows.append(row)


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
        spreadsheet.add_row("Ford")
        return spreadsheet

    def example_spreadsheet_with_one_row(self):
        spreadsheet = Spreadsheet()
        spreadsheet.add_row("Fiat")
        return spreadsheet



if __name__ == '__main__':
    unittest.main()


class PreownedCar:
    def __init__(self, marca):
        self._marca = marca

    def brand(self):
        return self._marca


class PreownedReaderFromSpreadsheet:
    def __init__(self, spreadsheet):
        self._spreadsheet = spreadsheet

    def read_preowned(self):
        preowned_cars = []
        for row in self._spreadsheet.rows():
            preowned_cars.append(PreownedCar(row))
        return preowned_cars

