from pydantic import BaseModel
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str
    dni: str
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None

class ClienteCreate(ClienteBase):
    """Esquema usado para crear un nuevo cliente."""
    pass

class Cliente(ClienteBase):
    """Esquema de respuesta (incluye campos autogenerados)."""
    id: int
    fecha_registro: datetime

    model_config = {
        "from_attributes": True  # ✅ reemplaza orm_mode en Pydantic v2
    }
