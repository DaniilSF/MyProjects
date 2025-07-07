from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


# ---------- Equipment ---------- #
class Equipment(BaseModel):
    id: int
    name: str
    type: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- BodyWeight ---------- #
class BodyWeight(BaseModel):
    id: int
    equipment_id: int
    empty_weight_kg: int
    max_load_kg: int
    effective_date: Optional[date] = None
    equipment: Equipment

    model_config = ConfigDict(from_attributes=True)


# ---------- CargoType ---------- #
class CargoType(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    density_kg_m3: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Location ---------- #
class Location(BaseModel):
    id: int
    name: str
    type: str
    coordinates: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Distance ---------- #
class Distance(BaseModel):
    id: int
    from_location: Location        # ← вместо пары ID
    to_location: Location
    distance_km: Decimal
    estimated_time_min: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)



# ---------- Shipment ---------- #
class Shipment(BaseModel):
    id: int
    equipment: Equipment
    cargo_type: CargoType
    load_location: Location
    unload_location: Location
    planned_datetime: Optional[datetime] = None
    actual_datetime: Optional[datetime] = None
    weight_kg: Optional[int] = None
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
