from PreownedCar import PreownedCar


class PreownedReaderFromSpreadsheet:
    def __init__(self, spreadsheet):
        self._spreadsheet = spreadsheet

    def read_preowned(self):
        preowned_cars = []
        rows = self._spreadsheet.rows()
        for row in rows:
            preowned_cars.append(PreownedCar(row[0]))
        return preowned_cars


