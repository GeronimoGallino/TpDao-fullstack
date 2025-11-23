from pydantic import BaseModel
from datetime import datetime


class EmpleadoBase(BaseModel):
    nombre: str
    dni: int
    cargo: str
    telefono: str | None = None
    email: str | None = None
    id_negocio: int


class EmpleadoCreate(EmpleadoBase):
    """Esquema para crear empleado."""
    pass


class Empleado(EmpleadoBase):
    """Respuesta completa."""
    id: int
    fecha_inicio: datetime
    estado: bool

    model_config = {
        "from_attributes": True
    }

class EmpleadoSimple(BaseModel):
    nombre: str

    model_config = {
        "from_attributes": True
    }
