from datetime import datetime
from pydantic import BaseModel


# ------------------------------
# Base
# ------------------------------
class MultaBase(BaseModel):
    id_alquiler: int
    tipo: str
    descripcion: str | None = None
    costo: float


# ------------------------------
# Create
# ------------------------------
class MultaCreate(MultaBase):
    pass


# ------------------------------
# Update (opcional)
# ------------------------------
class MultaUpdate(BaseModel):
    tipo: str | None = None
    descripcion: str | None = None
    costo: float | None = None


# ------------------------------
# Response / Full schema
# ------------------------------
class Multa(MultaBase):
    id_multa: int
    fecha: datetime

    model_config = {
        "from_attributes": True
    }