import duckdb
import pandas as pd
import logging
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        # ensure that folder for the database exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def execute_query(self, query: str):
        """Universal method to ingest data from the database"""
        conn = duckdb.connect(str(self.db_path))
        try:
            return conn.execute(query).fetchall()
        except duckdb.CatalogException:
            # it happens when there is no table yet
            logging.info('The table does not exist yet. Probably first run')
            return []
        except Exception as e:
            logging.error(f"Other database error: {e}")
            return []
        finally:
            conn.close()
    
    def save_dataframe(self, df: pd.DataFrame, table_name: str):
        """Saves DataFrame to DuckDB database"""
        if df.empty:
            logging.warning("DataFrame is empty")
            return
        
        # connect with the duckDB
        conn = duckdb.connect(str(self.db_path))

        try:
            # explicitly registered dataframe
            conn.register('temp_df', df)
            logging.info(f"Starting connection with database: {self.db_path}")
            # duck db sees the variable df from Python local range
            conn.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} AS 
                             SELECT * FROM temp_df WHERE 1=0
                          """) # now we copy only column headers, initiating empty table
            conn.execute(f"""INSERT INTO {table_name} 
                           SELECT * FROM temp_df
                           WHERE NOT EXISTS (
                               SELECT 1 FROM {table_name} t
                               WHERE t.code = temp_df.code
                               AND t.effective_date = temp_df.effective_date
                            )
                        """)

            # Check number of rows after saving
            count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            logging.info(f"Success! Table '{table_name}' has now {count} rows.")
            conn.unregister('temp_df')
        
        except Exception as e:
            logging.error(f"Saving to database error: {e}")
            raise e
        finally:
            if conn:
                conn.close()
                logging.info("Database connection closed")

