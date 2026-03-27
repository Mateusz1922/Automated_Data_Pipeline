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
            plt.switch_backend("Agg")
            plt.plot(df['date'], df['rate'], marker='o', linestyle='-', color='b')

            plt.title(f"{currency_code} rate for last {days_back} days")

            # save to file
            file_path = self.output_dir / f"{currency_code}_trend_{days_back}d.png"
            plt.savefig(file_path)
            plt.close()

            logging.info(f"Chart saved: {file_path}")
        except Exception as e:
            logging.error(f"Error while generating chart: {e}")
    
    def generate_gold_vs_currency_chart(self, currency_code: str):
        """Generates advanced correlation chart of gold and specified currency"""
        logging.info(f"Generating analysis of the correlation between gold and {currency_code}")

        query = f"""
                SELECT g.date, g.price_per_gram, c.rate as currency_rate
                FROM gold_rates g
                JOIN currency_rates c ON g.date = c.effective_date
                WHERE c.code = '{currency_code}'
                ORDER BY g.date ASC                
        """
        data = self.db.execute_query(query)
        if len(data) < 2:
            logging.warning("Not enough data to make the comparison")
            return
        
        df = pd.DataFrame(data, columns=["date", "gold", f"{currency_code}"])
        df["date"] = pd.to_datetime(df["date"])

        # Creating graph with 2 Y axes
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Ax Y: Gold
        color_gold = "tab:orange"
        ax1.set_xlabel("Data")
        ax1.set_ylabel("Gold price (PLN/g)", color=color_gold)
        ax1.plot(df["date"], df["gold"], color=color_gold, linewidth=2, label="Gold")
        ax1.tick_params(axis="y", labelcolor=color_gold)

        # Ax X: Our currency twin on the second ax
        ax2 = ax1.twinx()
        color_curr = 'tab:blue'
        ax2.set_ylabel(f"Kurs {currency_code} (PLN)", color=color_curr)
        ax2.plot(df['date'], df[f"{currency_code}"], color=color_curr, linestyle='--', linewidth=2, label=f"{currency_code}")
        ax2.tick_params(axis='y', labelcolor=color_curr)

        plt.title(f"Correlation analysis: Gold price vs {currency_code} rate")
        fig.tight_layout()
        
        # Save
        file_path = self.output_dir / f"gold_vs_{currency_code}_correlation.png"
        plt.savefig(file_path)
        plt.close()
        logging.info(f"Correlation analysis saved: {file_path}")
