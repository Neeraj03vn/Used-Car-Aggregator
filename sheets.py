# sheets.py
 
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet(sheet_name=None):
    sheet_name = sheet_name or os.environ.get("GOOGLE_SHEET_NAME", "Usedcar_Data")
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_path = "service_account.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1