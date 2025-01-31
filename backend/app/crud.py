from sqlalchemy.orm import Session
from models import Customer, SIPXPrice, EnergyData
from schemas import CustomerCreate, CustomerUpdate, SIPXPriceCreate, EnergyDataCreate
from datetime import datetime


# CUSTOMERS
# Validate that customer exists
def customer_exists(db: Session, customer_id: str) -> bool:
    return db.query(Customer).filter(Customer.id == customer_id).first() is not None

# Create a new customer

def create_customer(db: Session, customer: CustomerCreate):
    customer_id = customer.name.lower().replace(" ", "_")
    db_customer = Customer(id=customer_id,name = customer.name, is_consumer = customer.is_consumer, is_producer = customer.is_producer)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Get customer by ID
def get_customers(db: Session, customer_id: str):
    # Ensure customer_id is being treated as a string
    if not isinstance(customer_id, str):
        raise ValueError("customer_id must be a string")
    return db.query(Customer).filter(Customer.id == customer_id).first()


# Get all customers
def get_customers_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()

# Update customer by ID
def update_customer(db: Session, customer_id: str, customer: CustomerCreate):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer:
        db_customer.name = customer.name
        db_customer.is_consumer = customer.is_consumer
        db_customer.is_producer = customer.is_producer
        db.commit()
        db.refresh(db_customer)
        return db_customer
    return None

# Delete customer by ID

def delete_customer(db: Session, customer_id: str):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return db_customer
    return None

# SIPX PRICES

# Create a new SIPX price   

def create_sipx_price_crud(db: Session, sipx_price: SIPXPriceCreate):
    db_sipx_price = SIPXPrice(timestamp_utc = sipx_price.timestamp_utc, price_eur_per_kwh = sipx_price.price_eur_per_kwh)
    db.add(db_sipx_price)
    db.commit()
    db.refresh(db_sipx_price)
    return db_sipx_price

# Get SIPX price by timestamp range

def get_sipx_prices(db: Session, start_timestamp: datetime, end_timestamp: datetime):
    return db.query(SIPXPrice).filter(SIPXPrice.timestamp_utc >= start_timestamp, SIPXPrice.timestamp_utc <= end_timestamp).all()

# Get all SIPX prices

def get_sipx_prices_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SIPXPrice).offset(skip).limit(limit).all()

# Energy Data

# Create a new energy data entry

def create_energy_data(db: Session, energy_data: EnergyDataCreate):
    # Generate id based on customer_id and timestamp
    energy_data_id = f"{energy_data.customer_id}_{energy_data.timestamp_utc.strftime('%Y%m%d%H%M%S')}"
    db_energy_data = EnergyData(id=energy_data_id, timestamp_utc=energy_data.timestamp_utc, customer_id=energy_data.customer_id, cons_kwh=energy_data.cons_kwh, prod_kwh=energy_data.prod_kwh)
    db.add(db_energy_data)
    db.commit()
    db.refresh(db_energy_data)
    return db_energy_data

# Get energy data by customer ID

def get_energy_data(db: Session, customer_id: str):
    return db.query(EnergyData).filter(EnergyData.customer_id == customer_id).all()

# Get all energy data

def get_energy_data_all(db: Session):
    return db.query(EnergyData).all()

# Get energy data by timestamp range and customer ID

def get_energy_data_by_customer_and_timestamp_range(db: Session, customer_id: str, start_timestamp: datetime, end_timestamp: datetime):
    return db.query(EnergyData).filter(
        EnergyData.customer_id == customer_id,
        EnergyData.timestamp_utc >= start_timestamp,
        EnergyData.timestamp_utc <= end_timestamp
    ).all()