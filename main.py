from src.ingestion import DataIngestor
from src.processing import DataProcessor

def main():
    # We can use a free NBP API: https://api.nbp.pl/api/exchangerates/tables/A?format=json

    URL = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"
    RAW_DIR = "data/raw"
    MY_CURRENCIES = ["USD", "EUR", "GBP", "CHF"] # we want only these currencies

    # 1. download data and save to file
    ingestor = DataIngestor(api_url=URL, output_dir="data/raw")
    raw_data = ingestor.fetch_data()
    ingestor.save_to_raw(raw_data)

    # 2. Processing: read the file, validate and clean the data
    processor = DataProcessor(input_dir=RAW_DIR)
    raw_json = processor.load_latest_file()

    if raw_json:
        validated = processor.validate_data(raw_json)
        cleaned = processor.clean_data(validated, MY_CURRENCIES)

        print(f"Data fetch date: {cleaned.effectiveDate}")
        for r in cleaned.rates:
            print(f"Rate {r.code}: {r.rate} PLN")

if __name__ == "__main__":
    main()


