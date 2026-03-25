import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import logging

class ReportGenerator:
    def __init__(self, db_manager, output_dir="/data/reports"):
        self.db = db_manager
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_trend_chart(self, currency_code: str, days_back: int = 7):
        """Generating linear chart for the given currency from the last X days."""
        logging.info(f"Generating trend chart for {currency_code} ({days_back} days)...")

        query = f"""SELECT effective_date, rate
                    FROM currency_rates
                    WHERE code = '{currency_code}'
                    AND effective_date > CURRENT_DATE - INTERVAL '{days_back}' day
                    ORDER BY effective_date ASC
        """
        pass
        