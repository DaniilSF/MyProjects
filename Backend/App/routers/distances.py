from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_async_session
from .. import crud, schemas

router = APIRouter()

@router.get("", response_model=List[schemas.Distance])
async def get_all_distances(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_all_distances(session)

@router.get("{distance_id}", response_model=schemas.Distance)
async def get_distance(distance_id: int, session: AsyncSession = Depends(get_async_session)):
    distance = await crud.get_distance_by_id(distance_id, session)
    if distance is None:
        raise HTTPException(status_code=404, detail="Distance not found")
    return distance
