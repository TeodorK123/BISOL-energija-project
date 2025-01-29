# TODO fix autoincrement issue

from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from crud import create_customer, get_customers, update_customer, delete_customer, create_sipx_price, get_sipx_prices 
from schemas import CustomerCreate, CustomerUpdate, SIPXPriceCreate, EnergyDataCreate, CustomerResponse, SIPXPriceResponse, EnergyDataResponse


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to create a new customer

@app.post("/customers/", response_model=CustomerResponse)
def create_new_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db=db, customer=customer)

# Route to get a customer by ID

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: str, db: Session = Depends(get_db)):
    db_customer = get_customers(db=db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Route to get all customers

@app.get("/customers/", response_model=list[CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = get_customers(db=db, skip=skip, limit=limit)
    return customers

# Route to update a customer by ID

@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer_view(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = update_customer(db=db, customer_id=customer_id, customer_data=customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


# Route to delete a customer by ID
@app.delete("/customers/{customer_id}", response_model=CustomerResponse)
def delete_customer_view(customer_id: str, db: Session = Depends(get_db)):
    db_customer = delete_customer(db=db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Route to create a new SIPX price
@app.post("/sipx_prices/", response_model=SIPXPriceResponse)
def create_sipx_price_view(sipx_price: SIPXPriceCreate, db: Session = Depends(get_db)):
    return create_sipx_price(db=db, sipx_price=sipx_price)


# Route to get SIPX prices by timestamp range
@app.get("/sipx_prices/range", response_model=list[SIPXPriceResponse])
def get_sipx_prices_by_range(
    start_timestamp: datetime, 
    end_timestamp: datetime, 
    db: Session = Depends(get_db)
):
    sipx_prices = db.query(sipx_prices).filter(
        sipx_prices.timestamp_utc >= start_timestamp, 
        sipx_prices.timestamp_utc <= end_timestamp
    ).all()

    if not sipx_prices:
        raise HTTPException(status_code=404, detail="No SIPX prices found in the given range")
    
    return sipx_prices

# Route to get all SIPX prices
@app.get("/sipx_prices/", response_model=list[SIPXPriceResponse])
def get_all_sipx_prices(db: Session = Depends(get_db)):
    return get_sipx_prices(db=db)

