from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dispatcher API", version="0.1.0")

origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://frontend",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routers import (
    equipment,
    locations,
    distances,
    body_weights,
    cargo_types,
    shipments,
)

app.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
app.include_router(locations.router,  prefix="/locations", tags=["locations"])
app.include_router(distances.router,  prefix="/distances", tags=["distances"])
app.include_router(body_weights.router, prefix="/body_weights", tags=["body_weights"])
app.include_router(cargo_types.router,  prefix="/cargo_types", tags=["cargo_types"])
app.include_router(shipments.router,    prefix="/shipments", tags=["shipments"])

@app.get("/")
async def root():
    return {"message": "API is working"}