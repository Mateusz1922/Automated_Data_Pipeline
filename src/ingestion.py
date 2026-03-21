# Simple file for fetching data and saving them to a file, everything packed in a class
import requests
import logging
import json
from datetime import datetime
from pathlib import Path

# Logging config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class for obtaining and processing the data
class DataIngestor:
    def __init__(self, api_url: str, output_dir: str):
        self.api_url = api_url
        self.output_dir = Path(output_dir)
        # creates folder for data, if not exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_data(self) -> dict:
        """Fetches raw data from API"""
        logging.info(f"Fetching from: {self.api_url}")
        try:
            response = requests.get(self.api_url, timeout=10)
            # check if server responded positively
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP Error: {http_err}")
        
        except Exception as e:
            logging.error(f"Error during data fetching: {e}")
        
        return {}

    def save_to_raw(self, data: dict):
        """Saves raw data as json file"""
        if not data:
            logging.warning("No data to save.")
            return

        # File generation with date and hour
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self.output_dir / f"raw_data_{timestamp}.json"
        
        # MIEJSCE NA IMPLEMENTACJĘ:
        # 1. Otwórz plik w trybie zapisu ('w')
        # 2. Użyj json.dump(data, f, indent=4), aby zapisać dane
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # dump: data -> to file f -> with 4 spaces indent
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Data saved in: {file_path}")
        except Exception as e:
            logging.error(f"Error during data saving to file: {e}")