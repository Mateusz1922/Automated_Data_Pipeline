import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"Testuję bota...\nToken: {TOKEN[:10]}...\nID: {CHAT_ID}")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": "Test połączenia 123"}

r = requests.post(url, json=data)
print(f"Status: {r.status_code}")
print(f"Odpowiedź: {r.text}")