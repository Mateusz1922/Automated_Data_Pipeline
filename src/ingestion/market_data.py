# Separate Ingestor for gold - Gold has different endpoint and other format than currencies
import requests
import logging

class GoldIngestor:
    def __init__(self, url="https://api.nbp.pl/api/cenyzlota?format=json"):
        self.url = url

    def fetch_gold_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Fetching gold error: {e}")
            return None
        