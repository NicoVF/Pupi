from __future__ import print_function

import os.path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account


class SpreadsheetReader(object):

    def __init__(self, uid):

        service_account_file = './keys_secrets.json'
        scopes = ['https://www.googleapis.com/auth/spreadsheets']

        credentials = None
        credentials = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=scopes)

        # If modifying these scopes, delete the file token.json.

        # The ID and range of a sample spreadsheet.
        self.spreadsheet_id = uid

        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        self.result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                range="Hoja 1!A:Z", majorDimension='ROWS').execute()

    def GetValues(self):
        wanted_headers = ["marca", "modelo", "grupo", "anio"]
        xxx = []
        values = self.result.get('values', [])[1:]
        for row in values:
            for field in row:
                if wanted_headers.__contains__(field):
                    xxx.append(row.index(field))
        return values
