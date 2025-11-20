from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from backend.database import Base  # 👈 importante este import


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    dni = Column(String, unique=True, nullable=False)
    telefono = Column(String)
    email = Column(String)
    direccion = Column(String)
    fecha_registro = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)