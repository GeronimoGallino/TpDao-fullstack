from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from backend.database import Base


class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    dni = Column(Integer, unique=True, nullable=False)
    cargo = Column(String, nullable=False)
    telefono = Column(String)
    email = Column(String)
    fecha_inicio = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    id_negocio = Column(Integer, nullable=False)
    estado = Column(Boolean, default=True)  # 👈 borrado lógico
