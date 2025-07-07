from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_async_session
from .. import crud, schemas

router = APIRouter()

@router.get("", response_model=List[schemas.Equipment])
async def get_all_equipment(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_all_equipment(session)

@router.get("{equipment_id}", response_model=schemas.Equipment)
async def get_equipment(equipment_id: int, session: AsyncSession = Depends(get_async_session)):
    equipment = await crud.get_equipment_by_id(equipment_id, session)
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment