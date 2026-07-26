price_check.py

import requests

url = "https://kakaku.com/item/K0001630332/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("ステータス:", response.status_code)
print(response.text[:1000])
