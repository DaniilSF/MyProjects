from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_async_session
from .. import crud, schemas

router = APIRouter()

@router.get("", response_model=List[schemas.Location])
async def get_all_locations(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_all_locations(session)

@router.get("{location_id}", response_model=schemas.Location)
async def get_location(location_id: int, session: AsyncSession = Depends(get_async_session)):
    location = await crud.get_location_by_id(location_id, session)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location
