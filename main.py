from src.ingestion import DataIngestor
from src.processing import DataProcessor
from src.transformation import DataTransformer
from src.database import DatabaseManager
import duckdb

def main():
    # We can use a free NBP API: https://api.nbp.pl/api/exchangerates/tables/A?format=json

    URL = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"
    RAW_DIR = "data/raw"
    MY_CURRENCIES = ["USD", "EUR", "GBP", "CHF"] # we want only these currencies
    DB_PATH = "data/database/rates.duckdb"

    # 1. download data and save to file
    ingestor = DataIngestor(api_url=URL, output_dir=RAW_DIR)
    raw_data = ingestor.fetch_data()
    ingestor.save_to_raw(raw_data)

    # 2. Processing: read the file, validate and clean the data
    processor = DataProcessor(input_dir=RAW_DIR)
    raw_json = processor.load_latest_file()

    if raw_json:
        validated = processor.validate_data(raw_json)
        cleaned = processor.clean_data(validated, MY_CURRENCIES)

        # PANDAS TRANSFORMATION
        df = DataTransformer.to_dataframe(cleaned)
        # print("\n--- Final Dataframe ---")
        # print(df.head())

        # DATABASE LOAD
        db = DatabaseManager(db_path=DB_PATH)
        db.save_dataframe(df, table_name="currency_rates")

        # print(f"Data fetch date: {cleaned.effectiveDate}")
        # for r in cleaned.rates:
        #     print(f"Rate {r.code}: {r.rate} PLN")
        
        # DEBUG CHECK:
        print("\n--- Database data check ---")
        try:
            check_conn = duckdb.connect(DB_PATH)
            print(check_conn.query("SELECT * FROM currency_rates LIMIT 100").df())
            check_conn.close()
        except Exception as e:
            print(f"Database check error: {e}")

if __name__ == "__main__":
    main()


