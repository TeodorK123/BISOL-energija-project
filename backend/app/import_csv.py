# This script reads the CSV file and populates the database with the data (Slovenian: "Uvoz podatkov iz CSV datoteke v bazo podatkov").

#Imports
import csv
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Customer, SIPXPrice, EnergyData
from dateutil import parser

# Function to read the CSV and populate the database
def import_csv(file_path: str):
    db: Session = SessionLocal()
    processed_customers = set()
    processed_energydata = set()
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse the timestamp
                try:
                    timestamp = parser.parse(row["timestamp_utc"])  # Handles timezones automatically
                except Exception as e:
                    print(f"Error parsing timestamp: {row['timestamp_utc']} - {e}")
                    continue

                # Check or create SIPX Price entry
                sipx_price = db.query(SIPXPrice).filter(SIPXPrice.timestamp_utc == timestamp).first()
                if not sipx_price:
                    sipx_price = SIPXPrice(
                        timestamp_utc=timestamp,
                        price_eur_per_kwh=float(row["SIPX_EUR_kWh"]),
                    )
                    db.add(sipx_price)

                # Process customer and energy data for all relevant columns
                for col in row.keys():
                    if col.endswith("_cons_kWh") or col.endswith("_prod_kWh"):
                        # Extract customer ID and data type (cons/prod)
                        customer_id = col.split("_")[0]
                        data_type = "cons_kWh" if col.endswith("_cons_kWh") else "prod_kWh"

                        # Check or create Customer entry
                        if customer_id not in processed_customers:
                            customer = db.query(Customer).filter(Customer.id == customer_id).first()
                            if not customer:
                                # Create a new customer if not found
                                customer = Customer(
                                    id=customer_id,
                                    name=customer_id.capitalize(),
                                    is_consumer=False,
                                    is_producer=False,
                                )
                                db.add(customer)
                                processed_customers.add(customer_id)

                        # Update customer's role (whether consumer or producer)
                        if data_type == "cons_kWh":
                            customer.is_consumer = True
                        elif data_type == "prod_kWh":
                            customer.is_producer = True

                        # Add or update energy data
                        energy_data_id = f"{customer_id}_{timestamp}"
                        if energy_data_id not in processed_energydata:
                            energy_data = db.query(EnergyData).filter(EnergyData.id == energy_data_id).first()

                            if not energy_data:
                                # Create a new entry if it doesn't exist
                                energy_data = EnergyData(
                                    id=energy_data_id,
                                    timestamp_utc=timestamp,
                                    customer_id=customer_id,
                                    cons_kwh=float(row[col]) if data_type == "cons_kWh" else 0.0,
                                    prod_kwh=float(row[col]) if data_type == "prod_kWh" else 0.0
                                )
                                db.add(energy_data)
                                processed_energydata.add(energy_data_id)
                        
                            # Update the existing entry
                        if data_type == "cons_kWh":
                            energy_data.cons_kwh = float(row[col])
                        elif data_type == "prod_kWh":
                            energy_data.prod_kwh = float(row[col])

            # Commit changes after processing all rows
        db.commit()
        print("Data imported successfully!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

# Run the script
if __name__ == "__main__":
    csv_file_path = "/home/vboxuser/Desktop/BISOL energija project/backend/app/data.csv"
    import_csv(csv_file_path)
