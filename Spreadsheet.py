class Spreadsheet:
    def __init__(self):
        self._rows = []

    def rows(self):
        return self._rows

    def add_row(self, row):
        self._rows.append(row)
