from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime, timezone

TIPOS_VALIDOS = {"auto", "camioneta", "moto", "suv", "van"}


class VehiculoBase(BaseModel):
    marca: str
    modelo: str
    anio: int
    patente: str
    tipo: str
    kilometraje: int | None = 0
    disponible: bool | None = True
    costo_diario: int
    estado: str | None = "activo"

    # --- VALIDACIONES ---
    """"
    @field_validator("fecha_registro")
    def validar_fecha_registro(cls, v):
        if v and v > datetime.now(timezone.utc):
            raise ValueError("La fecha de registro no puede ser futura")
        return v
    """
    @field_validator("marca")
    def validar_marca(cls, v):
        if not (2 <= len(v) <= 30):
            raise ValueError("La marca debe tener entre 2 y 30 caracteres")
        return v

    @field_validator("modelo")
    def validar_modelo(cls, v):
        if not (1 <= len(v) <= 40):
            raise ValueError("El modelo debe tener entre 1 y 40 caracteres")
        return v

    @field_validator("anio")
    def validar_anio(cls, v):
        actual = datetime.now().year
        if v < 1900 or v > actual:
            raise ValueError(f"El año debe estar entre 1900 y {actual}")
        return v

    @field_validator("patente")
    def validar_patente(cls, v):
        import re
        # Patente argentina vieja (ABC123) o nueva (AB123CD)
        patron = r"^[A-Z]{2,3}[0-9]{3}[A-Z]{0,2}$"
        if not re.match(patron, v.upper()):
            raise ValueError("La patente debe ser válida (formato ABC123 o AB123CD)")
        return v.upper()

    @field_validator("tipo")
    def validar_tipo(cls, v):
        if v.lower() not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Debe ser uno de: {', '.join(TIPOS_VALIDOS)}")
        return v.lower()

    @field_validator("kilometraje")
    def validar_kilometraje(cls, v):
        if v is not None and v < 0:
            raise ValueError("El kilometraje no puede ser negativo")
        return v

    @field_validator("costo_diario")
    def validar_costo(cls, v):
        if v < 0:
            raise ValueError("El costo diario no puede ser negativo")
        return v


class VehiculoCreate(VehiculoBase):
    """Esquema usado para crear un nuevo vehículo."""
    pass


class Vehiculo(VehiculoBase):
    """Esquema de respuesta (incluye campos autogenerados)."""
    id: int
    fecha_registro: datetime

    @model_validator(mode="after")
    def validar_fecha_registro(self):
        # 1. Obtener la hora actual AWARE (UTC)
        now_utc = datetime.now(timezone.utc)
        
        # 2. Asegurar que self.fecha_registro es AWARE.
        #    Si no tiene tzinfo (es naive) le asignamos UTC, que es lo que SQLAlchemy usó por defecto.
        fecha_db_aware = self.fecha_registro
        if fecha_db_aware.tzinfo is None:
            fecha_db_aware = self.fecha_registro.replace(tzinfo=timezone.utc)
        
        # 3. Realizar la comparación AWARE vs AWARE
        if fecha_db_aware > now_utc:
            raise ValueError("La fecha de registro no puede ser futura")
        return self

    model_config = {
        "from_attributes": True
    }


class VehiculoSimple(BaseModel):
    marca: str
    modelo: str
    patente: str

    model_config = {
        "from_attributes": True
    }
