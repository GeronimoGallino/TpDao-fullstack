from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

from backend.schemas.empleado import EmpleadoSimple
from backend.schemas.vehiculo import VehiculoSimple

# ------------------------------
#  Base: Campos compartidos
# ------------------------------
class AlquilerBase(BaseModel):
    id_cliente: int
    id_vehiculo: int
    id_empleado: int
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    costo_total: Optional[int] = None
    kilometraje_inicial: Optional[int] = None
    kilometraje_final: Optional[int] = None
    estado: Optional[str] = "activo"

    @validator("fecha_fin")
    def validar_fechas(cls, v, values):
        if v and "fecha_inicio" in values and values["fecha_inicio"]:
            if v < values["fecha_inicio"]:
                raise ValueError("fecha_fin debe ser posterior a fecha_inicio")
        return v


# ------------------------------
#  Crear alquiler
# ------------------------------
class AlquilerCreate(BaseModel):
    id_cliente: int
    id_vehiculo: int
    id_empleado: int
    


# ------------------------------
#  Finalizar alquiler (solo lo necesario)
# ------------------------------
class AlquilerFinalizar(BaseModel):
    kilometraje_final: int


# ------------------------------
#  Respuesta
# ------------------------------
class Alquiler(AlquilerBase):
    id: int

    class Config:
        from_attributes = True

class AlquilerClienteDetalle(BaseModel):
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    costo_total: Optional[float] = None
    estado: str
    kilometraje_inicial: int
    kilometraje_final: Optional[int]

    vehiculo: VehiculoSimple
    empleado: EmpleadoSimple

    model_config = {
        "from_attributes": True
    }



