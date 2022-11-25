from read_sheet import SpreadsheetReader


class GoogleSpreadsheet:

    def __init__(self):
        self._reader = SpreadsheetReader()

    def rows(self):
        return self._reader.GetValues()