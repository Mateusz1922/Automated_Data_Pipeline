# File for reading json file saved in ingestion.py and we push it through the models
import json
import logging
from pathlib import Path
from src.models.pydantic import RateTable
import glob

class DataProcessor:
    def __init__(self, input_dir: str):
        self.input_dir = Path(input_dir)

    def load_latest_file(self) -> dict:
        """Finds the newest JSON file in raw folder"""
        files_list = list(self.input_dir.glob("*.json"))
        if not files_list:
            logging.error("No JSON files in the folder!")
            return {}
        # alphabetical sorting (works with the format YYYYMMDD_HHMMSS)
        # newest file at the end of the list
        latest_file_path = sorted(files_list)[-1]
        logging.info(f"Read the newest file: {latest_file_path.name}")

        with open(latest_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate_data(self, raw_data: list) -> RateTable:
        """Substitutes raw dict into validated Pydantic object"""
        if not raw_data:
            raise ValueError("Input data is empty!")
        return RateTable(**raw_data[0])

    def clean_data(self, validated_data: RateTable, currency_codes_list: list[str]) -> RateTable:
        """Optional: filter only the currencies you are interested in."""
        # we create a new list only with the currencies we want
        filtered_rates = [rate for rate in validated_data.rates if rate.code in currency_codes_list]
        # We create a copy of the object with the new list of rates
        cleaned_data = validated_data.model_copy(update={"rates": filtered_rates})
        return cleaned_data
