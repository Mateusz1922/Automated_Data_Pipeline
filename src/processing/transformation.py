# We create a new class, which receives our validated Pydantic model and transforms it to an ordered pandas table

import pandas as pd
import logging
from datetime import datetime
from src.models.pydantic import RateTable

class DataTransformer:
    @staticmethod
    def to_dataframe(validated_data: RateTable) -> pd.DataFrame:
        """Transforms Pydantic model into a DataFrame and adds metadata"""
        logging.info("Starting data transformation to Pandas format...")

        # 1. Get rates list (each element is a CurrencyRate)
        # Pydantic v2 lets us transform model to a dict
        rates_dicts = [rate.model_dump() for rate in validated_data.rates] # model dump transforms validated Pydantic model into raw Python dict

        # 2. Create a Dataframe
        df = pd.DataFrame(rates_dicts)

        # forcd type conversion for best possible e.g. object -> string
        df = df.convert_dtypes()

        # 3. Add metadata
        # Add date from NBP table
        df["effective_date"] = pd.to_datetime(validated_data.effectiveDate)
        # Add current timestamp (when the data were processed)
        df["processed_at"] = datetime.now()

        # 4. Simple transformation example
        df["Inverted rate"] = 1 / df["rate"] # e.g. PLNEUR

        logging.info(f"Transformation completed. Rows number: {len(df)}")
        return df
    
    @staticmethod
    def gold_to_dataframe(gold_data) -> pd.DataFrame:
        """
        Dedicated transformation for gold data. 
        Receives Pydantic GoldPrice object
        """
        logging.info("Gold transformation to pandas format...")
        
        # list with 1 dict as NBP makes it
        data = [{
            "date": gold_data.date,
            "price_per_gram": gold_data.price,
            "processed_at": datetime.now(),
            "source": "NBP API"
        }]
        
        df = pd.DataFrame(data)
        df = df.convert_dtypes()
        df['date'] = pd.to_datetime(df['date'])
        df['source'] = df['source']
        df['price_per_gram'] = df['price_per_gram']
        
        return df


