import requests
import re

url = "https://kakaku.com/item/K0001630332/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

html = response.content.decode("shift_jis", errors="ignore")

match = re.search(
    r'([\d,]+)<span class="p-prdInfoLowprice_currency">円</span>',
    html
)

if match:
    print("最安価格:", match.group(1))
else:
    print("価格が見つかりません")
