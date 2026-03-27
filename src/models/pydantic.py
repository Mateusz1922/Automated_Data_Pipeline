# file for creating standardized format of the data, if data not in our chosen shape, we'll get an error
from pydantic import BaseModel, Field
from typing import List

class CurrencyRate(BaseModel):
    # We are mapping fields from JSON NBP for our names, e.g. "currency", "code", "mid"
    currency_name: str = Field(alias="currency")
    code: str
    rate: float = Field(alias="mid")

class RateTable(BaseModel):
    table: str
    no: str
    effectiveDate: str
    rates: List[CurrencyRate] # CurrencyRate objects list

class GoldPrice(BaseModel):
    date: str = Field(alias="data")
    price: float = Field(alias="cena")