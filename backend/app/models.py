from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base


#Customer Table

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    is_consumer = Column(Boolean, nullable=False, default=False)
    is_producer = Column(Boolean, nullable=False, default=False)
    energy_data = relationship("EnergyData", back_populates="customer", cascade="all, delete-orphan")

#Price Table

class SIPXPrice(Base):
    __tablename__ = "sipx_prices"

    timestamp_utc = Column(DateTime, primary_key=True)
    price_eur_per_kwh = Column(Float, nullable=False)
    energy_data = relationship("EnergyData", back_populates="sipx_price")

class EnergyData(Base):
    __tablename__ = "energy_data"

    id = Column(String, primary_key=True, index=True)
    timestamp_utc = Column(DateTime, ForeignKey("sipx_prices.timestamp_utc"), nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    cons_kwh = Column(Float, nullable=False, default=0.0)
    prod_kwh = Column(Float, nullable=False, default=0.0)
    customer = relationship("Customer", back_populates="energy_data")
    sipx_price = relationship("SIPXPrice", back_populates="energy_data")