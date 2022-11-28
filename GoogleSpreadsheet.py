from read_sheet import SpreadsheetReader


class GoogleSpreadsheet:

    def __init__(self, uid):
        self._reader = SpreadsheetReader(uid)

    def rows(self):
        return self._reader.GetValues()