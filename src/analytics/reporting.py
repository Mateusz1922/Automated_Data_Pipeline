import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import logging

class ReportGenerator:
    def __init__(self, db_manager, output_dir="/data/reports"):
        self.db = db_manager
        self.output_dir = Path(output_dir)
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
        try:
            data = self.db.execute_query(query)
            if not data:
                logging.warning(f"No data for {currency_code}. Skipping the chart")
                return
            
            df = pd.DataFrame(data, columns=['date', 'rate'])
            df['date'] = pd.to_datetime(df['date'])

            plt.figure(figsize=(10, 6))
            plt.plot(df['date'], df['rate'], marker='o', linestyle='-', color='b')

            plt.title(f"{currency_code} rate for last {days_back} days")

            # save to file
            file_path = self.output_dir / f"{currency_code}_trend_{days_back}d.png"
            plt.savefig(file_path)
            plt.close()

            logging.info(f"Chart saved: {file_path}")
        except Exception as e:
            logging.error(f"Error while generating chart: {e}")
        