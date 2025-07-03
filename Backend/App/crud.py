from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models

# === Equipment ===
async def get_all_equipment(db: AsyncSession):
    result = await db.execute(select(models.Equipment))
    return result.scalars().all()

async def get_equipment_by_id(equipment_id: int, db: AsyncSession):
    result = await db.execute(select(models.Equipment).where(models.Equipment.id == equipment_id))
    return result.scalar_one_or_none()

# === Locations ===
async def get_all_locations(db: AsyncSession):
    result = await db.execute(select(models.Location))
    return result.scalars().all()

async def get_location_by_id(location_id: int, db: AsyncSession):
    result = await db.execute(select(models.Location).where(models.Location.id == location_id))
    return result.scalar_one_or_none()

# === Distances ===
async def get_all_distances(db: AsyncSession):
    result = await db.execute(select(models.Distance))
    return result.scalars().all()

async def get_distance_by_id(distance_id: int, db: AsyncSession):
    result = await db.execute(select(models.Distance).where(models.Distance.id == distance_id))
    return result.scalar_one_or_none()

# === BodyWeights ===
async def get_all_body_weights(db: AsyncSession):
    result = await db.execute(
        select(models.BodyWeight).options(selectinload(models.BodyWeight.equipment))
    )
    return result.scalars().all()

async def get_body_weight_by_id(body_weight_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.BodyWeight)
        .options(selectinload(models.BodyWeight.equipment))
        .where(models.BodyWeight.id == body_weight_id)
    )
    return result.scalar_one_or_none()

# === CargoTypes ===
async def get_all_cargo_types(db: AsyncSession):
    result = await db.execute(select(models.CargoType))
    return result.scalars().all()

async def get_cargo_type_by_id(cargo_type_id: int, db: AsyncSession):
    result = await db.execute(select(models.CargoType).where(models.CargoType.id == cargo_type_id))
    return result.scalar_one_or_none()

# === Shipments ===
async def get_all_shipments(db: AsyncSession):
    result = await db.execute(
        select(models.Shipment)
        .options(
            selectinload(models.Shipment.equipment),
            selectinload(models.Shipment.cargo_type),
            selectinload(models.Shipment.load_location),
            selectinload(models.Shipment.unload_location),
        )
    )
    return result.scalars().all()

async def get_shipment_by_id(shipment_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.Shipment)
        .options(
            selectinload(models.Shipment.equipment),
            selectinload(models.Shipment.cargo_type),
            selectinload(models.Shipment.load_location),
            selectinload(models.Shipment.unload_location),
        )
        .where(models.Shipment.id == shipment_id)
    )
    return result.scalar_one_or_none()
