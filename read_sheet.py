from __future__ import print_function

import os.path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account


class SpreadsheetReader(object):

    SERVICE_ACCOUNT_FILE = './keys_secrets.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = None
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # If modifying these scopes, delete the file token.json.

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1ESmRbSaV0zURrEFNiPBut0mynSZ45GWSXjgTBbMfjAo'

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Hoja 1!A:Z", majorDimension='ROWS').execute()

    def GetValues(self):
        wanted_headers = ["marca","modelo","grupo","anio"]
        xxx = []
        values = self.result.get('values', [])
        for row in values:
            for field in row:
                if wanted_headers.__contains__(field):
                    xxx.append(row.index(field))
        return values
