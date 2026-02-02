from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_async_session
from .. import crud, schemas

router = APIRouter()

@router.get("", response_model=List[schemas.Shipment])
async def get_all_shipments(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_all_shipments(session)

@router.get("{shipment_id}", response_model=schemas.Shipment)
async def get_shipment(shipment_id: int, session: AsyncSession = Depends(get_async_session)):
    shipment = await crud.get_shipment_by_id(shipment_id, session)
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment