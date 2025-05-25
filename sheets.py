import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# возвращает таблицу с заданным range
def get_sheet(gcp_key, sheet_id, range):

    credentials = Credentials.from_service_account_file(gcp_key, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    sheet_read = sheet.values().get(spreadsheetId=sheet_id, range=range).execute()

    return sheet_read

# считает среднее списка
def count_mean(data):
    total = 0
    count = 0
    for item in data:
        try:
            num = float(item)
            total += num
            count += 1
        except (ValueError, TypeError):
            continue
    return "{:.2f}".format(total / count) if count != 0 else "0.00"


def mean_score(column):
    values = column.get('values', [])

    values1 = [val[0] for val in values if len(val) == 1]

    return count_mean(values1)

def mean_score_by_group(data, group):
    values = data.get('values', [])

    values1 = [val[2] for val in values if len(val) == 3 and val[0] == group]

    return count_mean(values1)
