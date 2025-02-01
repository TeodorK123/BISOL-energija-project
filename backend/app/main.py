#MAIN / ROUTES

#Imports

from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from crud import create_customer, create_energy_data, create_sipx_price_crud, customer_exists, get_customers, get_customers_all, get_energy_data_all, get_energy_data_by_customer_and_timestamp_range, get_sipx_prices_all, update_customer, delete_customer, get_sipx_prices 
from schemas import CustomerCreate, SIPXPriceCreate, EnergyDataCreate, CustomerResponse, SIPXPriceResponse, EnergyDataResponse
from models import Customer, SIPXPrice, EnergyData

from fastapi.middleware.cors import CORSMiddleware



# --- INIT ---

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- ROUTES ---

#Route for the root page, which redirects to the docs

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

# Route to create a new customer

@app.post("/customers/", response_model=CustomerResponse)
def create_new_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db=db, customer=customer)

# Route to get a customer by ID

@app.get("/customers/{id}", response_model=CustomerResponse)
def read_customer_by_id(id: str, db: Session = Depends(get_db)):
    db_customer = get_customers(db,id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Route to get all customers

@app.get("/customers/", response_model=list[CustomerResponse])
def read_first_100_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = get_customers_all(db=db, skip=skip, limit=limit)
    return customers

# Route to update a customer by ID

@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer_view(customer_id: str, customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = update_customer(db=db, customer_id=customer_id, customer=customer)
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
def create_sipx_price(sipx_price: SIPXPriceCreate, db: Session = Depends(get_db)):
    return create_sipx_price_crud(db=db, sipx_price=sipx_price)


# Route to get SIPX prices by timestamp range
@app.get("/sipx_prices/range", response_model=list[SIPXPriceResponse])
def get_sipx_prices_by_timestamprange(
    start_timestamp: datetime, 
    end_timestamp: datetime, 
    db: Session = Depends(get_db)
):
    sipx_prices = db.query(SIPXPrice).filter(
        SIPXPrice.timestamp_utc >= start_timestamp, 
        SIPXPrice.timestamp_utc <= end_timestamp
    ).all()

    if not sipx_prices:
        raise HTTPException(status_code=404, detail="No SIPX prices found in the given range")
    return sipx_prices

# Route to get all SIPX prices
@app.get("/sipx_prices/", response_model=list[SIPXPriceResponse])
def get_all_sipx_prices(db: Session = Depends(get_db)):
    return get_sipx_prices_all(db=db)

# Route to get all energy data entries

@app.get("/energy_data/", response_model=list[EnergyDataResponse])
def get_all_energy_data(db: Session = Depends(get_db)):
    return get_energy_data_all(db=db)


# Route to get energy data by timestamp range and customer id

@app.get("/energy_data/customer/{customer_id}/range", response_model=list[EnergyDataResponse])
def get_energy_data_by_customer_and_range(
    customer_id: str,
    start_timestamp: datetime,
    end_timestamp: datetime,
    db: Session = Depends(get_db)
):
    energy_data = get_energy_data_by_customer_and_timestamp_range(db=db, customer_id=customer_id, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
    if not energy_data:
        raise HTTPException(status_code=404, detail="No energy data found for the given customer ID and timestamp range")
    return energy_data

# Route to create a new energy data entry

@app.post("/energy_data/", response_model=EnergyDataResponse)
def create_energy_data_view(energy_data: EnergyDataCreate, db: Session = Depends(get_db)):
    if not customer_exists(db, energy_data.customer_id): 
        raise HTTPException(status_code=404, detail="Customer not found")
    return create_energy_data(db=db, energy_data=energy_data)