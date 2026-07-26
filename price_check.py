import requests
import re

url = "https://kakaku.com/item/K0001630332/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

html = response.content.decode("shift_jis", errors="ignore")

print("価格文字列を検索中")

for word in ["最安", "価格", "円", "¥"]:
    pos = html.find(word)

    if pos >= 0:
        print(f"\n=== {word} ===")
        print(html[pos-200:pos+500])
