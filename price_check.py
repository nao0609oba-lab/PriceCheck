import os
import json
import re
import requests
import gspread
from google.oauth2.service_account import Credentials

# -------------------------
# Google認証
# -------------------------
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

# -------------------------
# 価格取得関数
# -------------------------
headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_price(url):
    try:
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
            return match.group(1)

    except Exception as e:
        print(f"ERROR {url}: {e}")

    return ""

# -------------------------
# シート取得
# -------------------------
rows = sheet.get_all_values()

# D列用
d_values = []

# J列用
j_values = []

for row_num in range(2, len(rows) + 1):

    row = rows[row_num - 1]

    # -------------------------
    # C列(URL) → D列(価格)
    # -------------------------
    price_d = ""

    if len(row) >= 3:

        url = row[2].strip()

        if url.startswith("https://kakaku.com/item/"):

            print(f"Row {row_num} C列取得中")

            price_d = get_price(url)

            if price_d:
                print(
                    f"Row {row_num} C→D : {price_d}"
                )

    d_values.append([price_d])

    # -------------------------
    # I列(URL) → J列(価格)
    # -------------------------
    price_j = ""

    if len(row) >= 9:

        url2 = row[8].strip()

        if url2.startswith("https://kakaku.com/item/"):

            print(f"Row {row_num} I列取得中")

            price_j = get_price(url2)

            if price_j:
                print(
                    f"Row {row_num} I→J : {price_j}"
                )

    j_values.append([price_j])

# -------------------------
# 一括更新
# -------------------------
sheet.batch_update([
    {
        "range": f"D2:D{len(d_values)+1}",
        "values": d_values
    },
    {
        "range": f"J2:J{len(j_values)+1}",
        "values": j_values
    }
])

print("更新完了")
