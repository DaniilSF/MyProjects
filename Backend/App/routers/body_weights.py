from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_async_session
from .. import crud, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.BodyWeight])
async def get_all_body_weights(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_all_body_weights(session)

@router.get("/{body_weight_id}", response_model=schemas.BodyWeight)
async def get_body_weight(body_weight_id: int, session: AsyncSession = Depends(get_async_session)):
    body_weight = await crud.get_body_weight_by_id(body_weight_id, session)
    if body_weight is None:
        raise HTTPException(status_code=404, detail="Body weight record not found")
    return body_weight
