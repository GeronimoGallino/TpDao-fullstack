from pydantic import BaseModel
from datetime import datetime

class VehiculoBase(BaseModel):
    marca: str
    modelo: str
    anio: int
    patente: str
    tipo: str  # auto, camioneta, moto, etc.
    kilometraje: int | None = 0
    disponible: bool | None = True
    costo_diario: int
    estado: str | None = "activo"  # activo, mantenimiento, inactivo

class VehiculoCreate(VehiculoBase):
    """Esquema usado para crear un nuevo vehículo."""
    pass

class Vehiculo(VehiculoBase):
    """Esquema de respuesta (incluye campos autogenerados)."""
    id: int
    fecha_registro: datetime

    model_config = {
        "from_attributes": True  # ✅ reemplaza orm_mode en Pydantic v2
    }

class VehiculoSimple(BaseModel):
    marca: str
    modelo: str
    patente: str

    model_config = {
        "from_attributes": True
    }
