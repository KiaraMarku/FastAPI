import os
from typing import Optional
from fastapi import FastAPI, HTTPException
import pandas as pd
from models import DriverCreate, DriverResponse, VehicleType

app = FastAPI(
    title="Taxi Driver Management System",
    description="CRUD API for managing taxi drivers",
)
CSV_FILE = "drivers.csv"

def load_drivers():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)

        df['id'] = df['id'].astype(int)
        df['license_number'] = df['license_number'].astype(str) 
        df['name'] = df['name'].astype(str)
        df['vehicle_type'] = df['vehicle_type'].replace([pd.NA], None)
        df['is_available'] = df['is_available'].astype(bool)
        
        return df
    else:
        return pd.DataFrame(columns=['id', 'name', 'license_number', 'vehicle_type', 'is_available'])
    
def save_drivers(df):
    df.to_csv(CSV_FILE, index=False)

def get_next_id(df):
    if df.empty:
        return 1
    return int(df['id'].max()) + 1

@app.get("/")
async def root():
    return {
        "message": "CRUD API for Taxi Driver Management", 
        "description": "Visit the link below to access and test the endpoints",
        "docs_url": "http://localhost:8000/docs"
    }


@app.post("/drivers", response_model=DriverResponse)
def create_driver(driver: DriverCreate):
    df = load_drivers()

    new_id = get_next_id(df)

    new_driver = {
        'id': new_id,
        'name': driver.name,
        'license_number': driver.license_number,
        'vehicle_type': driver.vehicle_type.value if driver.vehicle_type else None,
        'is_available': driver.is_available
    }

    df = pd.concat([df, pd.DataFrame([new_driver])], ignore_index=True)
    save_drivers(df)
    return DriverResponse(**new_driver)

@app.put("/drivers/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: int, driver: DriverCreate):
    df = load_drivers()
    if df.loc[df['id'] == driver_id].empty:
        raise HTTPException(status_code=404, detail="Driver not found")

    df.loc[df['id'] == driver_id, ['name', 'license_number', 'vehicle_type', 'is_available']] = [
        driver.name,
        driver.license_number,
        driver.vehicle_type.value if driver.vehicle_type else None,
        driver.is_available
    ]
    save_drivers(df)
    updated_driver = df.loc[df['id'] == driver_id].iloc[0].to_dict()
    return DriverResponse(**updated_driver)

@app.get("/drivers/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int):
    df = load_drivers()
    driver_row = df.loc[df['id'] == driver_id]
    if driver_row.empty:
        raise HTTPException(status_code=404, detail="Driver not found")
    driver = driver_row.iloc[0].to_dict()
    return DriverResponse(**driver)


@app.get("/drivers", response_model=list[DriverResponse])
def get_drivers( is_available: Optional[bool] = None,
                 vehicle_type: Optional[VehicleType] = None,
                 name: Optional[str] = None):
    df = load_drivers()
    if df.empty:
        return []

    if is_available is not None:
        df = df[df['is_available'] == is_available]
    if vehicle_type is not None:
        df = df[df['vehicle_type'] == vehicle_type.value]
    if name is not None:
        df = df[df['name'].str.contains(name, case=False, na=False)]
    drivers = []
    for _, row in df.iterrows():
        drivers.append(DriverResponse(**row.to_dict()))

    return drivers