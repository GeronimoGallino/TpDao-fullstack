from pydantic import BaseModel
from datetime import datetime

class AlquilerBase(BaseModel):
    id_cliente: int
    id_vehiculo: int
    id_empleado: int
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    costo_total: int | None = None
    kilometraje_inicial: int | None = None
    kilometraje_final: int | None = None
    estado: str | None = "activo"

class AlquilerCreate(AlquilerBase):
    """Esquema usado para crear un nuevo alquiler."""
    pass

class Alquiler(AlquilerBase):
    """Esquema de respuesta (incluye campos autogenerados)."""
    id: int

    model_config = {
        "from_attributes": True  # ✅ reemplaza orm_mode en Pydantic v2
    }