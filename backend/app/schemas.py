# Imports

from pydantic import BaseModel
from typing import List
from datetime import datetime

# --- SCHEMAS ---

#Customer Schema

class CustomerBase(BaseModel):
    name: str
    is_consumer: bool
    is_producer: bool

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: str

    class Config:
        orm_mode = True


#Price schema

class SIPXPriceBase(BaseModel):
    timestamp_utc: datetime
    price_eur_per_kwh: float

class SIPXPriceCreate(SIPXPriceBase):
    pass

class SIPXPriceResponse(SIPXPriceBase):
    class Config:
        orm_mode = True

#EnergyData schema

class EnergyDataBase(BaseModel):
    timestamp_utc: datetime
    customer_id: str
    cons_kwh: float = 0.0
    prod_kwh: float = 0.0

class EnergyDataCreate(EnergyDataBase):
    pass

class EnergyDataResponse(EnergyDataBase):
    id: str

    class Config:
        orm_mode = True


