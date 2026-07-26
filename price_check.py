import os
import json
import re
import requests
import gspread
from google.oauth2.service_account import Credentials

# Google認証
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=scopes
)

gc = gspread.authorize(creds)

sheet = gc.open_by_key(os.environ["SHEET_ID"]).worksheet("PriceCheck")

rows = sheet.get_all_values()

for row_num in range(2, len(rows) + 1):

    if len(rows[row_num - 1]) < 2:
        continue

    url = rows[row_num - 1][1]

    if not url:
        continue

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )

        html = response.content.decode(
            "shift_jis",
            errors="ignore"
        )

        match = re.search(
            r'([\d,]+)<span class="p-prdInfoLowprice_currency">円</span>',
            html
        )

        if match:
            price = match.group(1)
            sheet.update_cell(row_num, 3, price)
            print(f"Row {row_num}: {price}")

    except Exception as e:
        print(f"Row {row_num}: ERROR {e}")
