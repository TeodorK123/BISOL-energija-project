from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

#Customer

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

class CustomerUpdate(CustomerBase):
    name: Optional[str] = None
    is_consumer: Optional[bool] = None
    is_producer: Optional[bool] = None

#Price

class SIPXPriceBase(BaseModel):
    timestamp_utc: datetime
    price_eur_per_kwh: float

class SIPXPriceCreate(SIPXPriceBase):
    pass

class SIPXPriceResponse(SIPXPriceBase):
    class Config:
        orm_mode = True

class SIPXPriceUpdate(SIPXPriceBase):
    timestamp_utc: Optional[datetime] = None
    price_eur_per_kwh: Optional[float] = None

#EnergyData

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

class EnergyDataUpdate(EnergyDataBase):
    timestamp_utc: Optional[datetime] = None
    customer_id: Optional[str] = None
    cons_kwh: Optional[float] = None
    prod_kwh: Optional[float] = None
