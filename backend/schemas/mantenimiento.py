from pydantic import BaseModel
from datetime import datetime

class MantenimientoBase(BaseModel):
    id_vehiculo: int
    id_empleado: int
    fecha: datetime | None = None
    km_actual: int
    tipo: str  # preventivo, correctivo, etc.
    costo: int
    observaciones: str | None = None
    km_prox_mant: int = 10000
    meses_prox_mant: int = 12


class MantenimientoCreate(MantenimientoBase):
    """Esquema usado para crear un nuevo mantenimiento."""
    pass

class Mantenimiento(MantenimientoBase):
    """Esquema de respuesta (incluye campos autogenerados)."""
    id: int

    model_config = {
        "from_attributes": True  # ✅ reemplaza orm_mode en Pydantic v2
    }