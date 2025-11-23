from pydantic import BaseModel
from datetime import datetime

class PlanMantenimientoBase(BaseModel):
    tipo_vehiculo: str  # auto, camioneta, moto, etc.
    km_intervalo: int  # cada cuantos km se realiza el mantenimiento
    meses_intervalo: int  # cada cuantos meses se realiza el mantenimiento

class PlanMantenimientoCreate(PlanMantenimientoBase):
    """Esquema usado para crear un nuevo plan de mantenimiento."""
    pass

class PlanMantenimiento(PlanMantenimientoBase):
    """Esquema de respuesta (incluye campos autogenerados)."""
    id: int

    model_config = {
        "from_attributes": True  # ✅ reemplaza orm_mode en Pydantic v2
    }