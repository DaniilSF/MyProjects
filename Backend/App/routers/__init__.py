# боковой импорт нужен, чтобы main.py смог сделать
# “from .routers import equipment, …”
from . import (
    equipment,
    locations,
    distances,
    body_weights,
    cargo_types,
    shipments,
)

__all__ = [
    "equipment",
    "locations",
    "distances",
    "body_weights",
    "cargo_types",
    "shipments",
]
