from enum import Enum
from typing import Optional
from pydantic import BaseModel

class VehicleType(str, Enum):
    SEDAN = "sedan"
    SUV = "suv"
    HATCHBACK = "hatchback"
    WAGON = "wagon"
    STANDARD = "standard"

class DriverCreate(BaseModel):
    name: str
    license_number: str
    vehicle_type: Optional[VehicleType] = None
    is_available: bool = True

class DriverResponse(BaseModel):
    id: int
    name: str
    license_number: str
    vehicle_type: Optional[VehicleType]
    is_available: bool
