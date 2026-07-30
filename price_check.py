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

sheet = gc.open_by_key(
    os.environ["SHEET_ID"]
).worksheet("PriceCheck")

rows = sheet.get_all_values()

headers = {
    "User-Agent": "Mozilla/5.0"
}

for row_num in range(2, len(rows) + 1):

    try:
        row = rows[row_num - 1]

        # ==========================
        # C列(URL) → D列(最安価格)
        # ==========================
        if len(row) >= 3:

            url = row[2].strip()

            if url.startswith("https://kakaku.com/item/"):

                response = requests.get(
                    url,
                    headers=headers,
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
                    sheet.update_cell(row_num, 4, price)

                    print(
                        f"Row {row_num} C→D : {price}"
                    )

        # ==========================
        # I列(URL) → J列(最安価格)
        # ==========================
        if len(row) >= 9:

            url2 = row[8].strip()

            if url2.startswith("https://kakaku.com/item/"):

                response = requests.get(
                    url2,
                    headers=headers,
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
                    price2 = match.group(1)
                    sheet.update_cell(row_num, 10, price2)

                    print(
                        f"Row {row_num} I→J : {price2}"
                    )

    except Exception as e:
        print(
            f"Row {row_num}: ERROR {e}"
        )

print("完了")
