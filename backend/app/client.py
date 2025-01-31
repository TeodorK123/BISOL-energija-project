import requests
from datetime import datetime, time, timezone

BASE_URL = "http://localhost:8000"

def create_customer(name, is_consumer, is_producer):
    url = f"{BASE_URL}/customers/"
    payload = {
        "name": name,
        "is_consumer": is_consumer,
        "is_producer": is_producer
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Customer '{name}' created successfully.")
    else:
        print(f"Failed to create customer '{name}': {response.json()}")

def create_energy_data(customer_id, timestamp_utc, cons_kwh, prod_kwh):
    url = f"{BASE_URL}/energy_data/"
    payload = {
        "customer_id": customer_id,
        "timestamp_utc": timestamp_utc,
        "cons_kwh": cons_kwh,
        "prod_kwh": prod_kwh
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Energy data for customer '{customer_id}' created successfully.")
    else:
        print(f"Failed to create energy data for customer '{customer_id}': {response.json()}")

def get_customers():
    url = f"{BASE_URL}/customers/"
    response = requests.get(url)
    if response.status_code == 200:
        customers = response.json()
        print("Customers:")
        for customer in customers:
            print(customer)
    else:
        print(f"Failed to get customers: {response.json()}")

def get_energy_data_by_customer_and_range(customer_id, start_timestamp, end_timestamp):
    url = f"{BASE_URL}/energy_data/customer/{customer_id}/range"
    params = {
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        energy_data = response.json()
        print(f"Energy data for customer '{customer_id}' from {start_timestamp} to {end_timestamp}:")
        for data in energy_data:
            print(data)
    else:
        print(f"Failed to get energy data for customer '{customer_id}': {response.json()}")

if __name__ == "__main__":
    create_customer("Customer 205", True, False) #Change as needed
    create_customer("Customer 305", False, True) #Change as needed

    create_energy_data("customer205", datetime.now(timezone.utc).isoformat(), 10.5, 0.0) #Change as needed, NOTE: customer ids are all lowercase, no spaces
    time.sleep(2)
    create_energy_data("customer205", datetime.now(timezone.utc).isoformat(), 2.5, 2.0) #Change as needed, NOTE: customer ids are all lowercase, no spaces
    create_energy_data("customer305", datetime.now(timezone.utc).isoformat(), 0.0, 15.3) #Change as needed, NOTE: customer ids are all lowercase, no spaces

    get_customers()

    start_timestamp = "2023-01-01T00:00:00" #3 year range
    end_timestamp = "2026-12-31T23:59:59"
    get_energy_data_by_customer_and_range("customer205", start_timestamp, end_timestamp) #Change as needed, NOTE: customer ids are all lowercase, no spaces