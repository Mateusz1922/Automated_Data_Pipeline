from src.ingestion.nbp_rates import DataIngestor
from src.processing.validation import DataProcessor
from src.processing.transformation import DataTransformer
from src.storage.duckdb import DatabaseManager
from src.processing.quality import DataQualityChecker
from src.analytics.cli import CliInterface
from src.analytics.reporting import ReportGenerator
import os
from pathlib import Path
from src.ingestion.market_data import GoldIngestor
from src.models.pydantic import GoldPrice
import pandas as pd
from datetime import datetime

# get the absolute path to the folder where main.py is
BASE_DIR = Path(__file__).resolve().parent

def main():
    # We can use a free NBP API: https://api.nbp.pl/api/exchangerates/tables/A?format=json

    URL = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"
    RAW_DIR = BASE_DIR / "data" / "raw"
    DB_PATH = BASE_DIR / "data" / "database" / "rates.duckdb"
    REPORT_DIR = BASE_DIR / "data" / "reports"

    cli = CliInterface()
    args = cli.parse_arguments()

    currency_list = [c.strip().upper() for c in args.currencies.split(',')]

    # 1. extract data and save raw
    ingestor = DataIngestor(api_url=URL, output_dir=RAW_DIR)
    raw_data = ingestor.fetch_data()
    ingestor.save_to_raw(raw_data)

    # 2. Processing: read the file, validate and clean the data
    processor = DataProcessor(input_dir=RAW_DIR)
    raw_json = processor.load_latest_file()

    if raw_json:
        validated = processor.validate_data(raw_json)
        cleaned = processor.clean_data(validated, currency_list)

        # PANDAS TRANSFORMATION
        df = DataTransformer.to_dataframe(cleaned)

        # DATABASE LOAD
        db = DatabaseManager(db_path=DB_PATH)
        # Use the arguments in the process
        quality_checker = DataQualityChecker(db)
        df = quality_checker.check_for_anomalies(df, threshold=args.threshold)

        db.save_dataframe(df, table_name="currency_rates")

        # Enrichment - gold
        if args.check_gold:
            print("Fetching gold prices as requested...")
            gold_ingestor = GoldIngestor()
            raw_gold = gold_ingestor.fetch_gold_data()

            if raw_gold:
                # 2. validate (Pydantic), NBP returns a list, we take the first (newest) element
                gold_validated = GoldPrice(**raw_gold[0])

                # transform to df
                gold_df = DataTransformer.gold_to_dataframe(gold_validated)

                db.save_dataframe(gold_df, table_name="gold_rates")

        # REPORTING
        report_gen = ReportGenerator(db, output_dir=REPORT_DIR)

        # separate charts for every currency
        for code in currency_list:
            report_gen.generate_trend_chart(currency_code=code, days_back=args.days)
        
        # Only if we have the gold flag and current currency in the list
        currency = "USD"
        if args.check_gold and currency in currency_list:
            report_gen.generate_gold_vs_currency_chart(currency_code=currency)

    
    print(f"Pipeline finished for currencies: {currency_list}")

if __name__ == "__main__":
    main()

        # print(f"Data fetch date: {cleaned.effectiveDate}")
        # for r in cleaned.rates:
        #     print(f"Rate {r.code}: {r.rate} PLN")
        
        # DEBUG CHECK:
        # print("\n--- Database data check ---")
        # try:
        #     check_conn = duckdb.connect(DB_PATH)
        #     print(check_conn.query("SELECT * FROM currency_rates LIMIT 100").df())
        #     check_conn.close()
        # except Exception as e:
        #     print(f"Database check error: {e}")
