from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_async_session
from .. import crud, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.CargoType])
async def get_all_cargo_types(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_all_cargo_types(session)

@router.get("/{cargo_type_id}", response_model=schemas.CargoType)
async def get_cargo_type(cargo_type_id: int, session: AsyncSession = Depends(get_async_session)):
    cargo_type = await crud.get_cargo_type_by_id(cargo_type_id, session)
    if cargo_type is None:
        raise HTTPException(status_code=404, detail="Cargo type not found")
    return cargo_type
