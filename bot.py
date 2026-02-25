import requests
from bs4 import BeautifulSoup
import time
import os
from telegram import Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

SEARCH_URL = "https://www.firstcry.com/search?searchstring=hot%20wheels"

bot = Bot(token=BOT_TOKEN)

seen_products = set()

def check_products():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")

    for link in links:
        href = link.get("href")
        name = link.text.strip()

        if href and "/product-detail" in href:
            product_url = "https://www.firstcry.com" + href

            if product_url not in seen_products:
                seen_products.add(product_url)

                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"🔥 Hot Wheels Alert!\n{name}\n{product_url}"
                )

while True:
    try:
        check_products()
        time.sleep(180)
    except Exception as e:
        print("Error:", e)
        time.sleep(60)
