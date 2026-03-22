# We create a new class, which receives our validated Pydantic model and transforms it to an ordered pandas table

import pandas as pd
import logging
from datetime import datetime
from src.models import RateTable

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


