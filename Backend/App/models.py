from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50))
    status = Column(String(20))
    description = Column(Text)

    body_weights = relationship("BodyWeight", back_populates="equipment")
    shipments = relationship("Shipment", back_populates="equipment")


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)
    coordinates = Column(String(50))

    shipments_load = relationship("Shipment", back_populates="load_location", foreign_keys='Shipment.load_location_id')
    shipments_unload = relationship("Shipment", back_populates="unload_location", foreign_keys='Shipment.unload_location_id')


class Distance(Base):
    __tablename__ = "distances"
    id = Column(Integer, primary_key=True, index=True)
    location_from_id = Column(Integer, ForeignKey("locations.id"))
    location_to_id = Column(Integer, ForeignKey("locations.id"))
    distance_km = Column(Numeric(10, 2), nullable=False)
    estimated_time_min = Column(Integer)

    from_location = relationship("Location", foreign_keys=[location_from_id], lazy="joined",)
    to_location = relationship("Location", foreign_keys=[location_to_id], lazy="joined",)


class BodyWeight(Base):
    __tablename__ = "body_weights"
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    empty_weight_kg = Column(Integer, nullable=False)
    max_load_kg = Column(Integer, nullable=False)
    effective_date = Column(Date)

    equipment = relationship("Equipment", back_populates="body_weights")


class CargoType(Base):
    __tablename__ = "cargo_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20))
    density_kg_m3 = Column(Numeric(10, 2))

    shipments = relationship("Shipment", back_populates="cargo_type")


class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    cargo_type_id = Column(Integer, ForeignKey("cargo_types.id"))
    load_location_id = Column(Integer, ForeignKey("locations.id"))
    unload_location_id = Column(Integer, ForeignKey("locations.id"))
    planned_datetime = Column(TIMESTAMP)
    actual_datetime = Column(TIMESTAMP)
    weight_kg = Column(Integer)
    status = Column(String(20))

    equipment = relationship("Equipment", back_populates="shipments")
    cargo_type = relationship("CargoType", back_populates="shipments")
    load_location = relationship("Location", foreign_keys=[load_location_id], back_populates="shipments_load")
    unload_location = relationship("Location", foreign_keys=[unload_location_id], back_populates="shipments_unload")