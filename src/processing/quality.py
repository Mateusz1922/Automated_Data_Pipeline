import pandas as pd
import logging
import duckdb

class DataQualityChecker:
    def __init__(self, db_manager):
        self.db = db_manager

    def check_for_anomalies(self, df: pd.DataFrame, threshold: float = 0.20):
        df['is_anomaly'] = False

        for index, row in df.iterrows():
            current_code = row['code']
            current_rate = row['rate']
            query = f"""
                SELECT rate 
                FROM currency_rates 
                WHERE code = '{current_code}' 
                ORDER BY effective_date DESC 
                LIMIT 1
            """
            result = self.db.execute_query(query)
            # db can be empty
            if result:
                previous_rate = result[0][0]
                change = abs(current_rate - previous_rate) / previous_rate
                if change > threshold:
                    logging.warning(
                        f"Warning! The rate has changed for over {change*100:.2f}%. Please check if it's not the API error")
                    df.at[index, 'is_anomaly'] = True
            else:
                logging.info(f"No previous data for {current_code}. Quality test skip.")
        return df