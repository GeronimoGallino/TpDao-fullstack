from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from backend.database import Base  # 👈 correcto

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    anio = Column(Integer, nullable=False)
    patente = Column(String, unique=True, nullable=False)
    tipo = Column(String, nullable=False)  # auto, camioneta, moto, etc.
    kilometraje = Column(Integer, default=0)
    disponible = Column(Boolean, default=True)
    costo_diario = Column(Integer, nullable=False)
    estado = Column(String, default="activo")  # activo, mantenimiento, inactivo
    fecha_registro = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    