from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from backend.database import Base
from sqlalchemy.orm import relationship


class Multa(Base):
    __tablename__ = "multas"

    id_multa = Column(Integer, primary_key=True, index=True)
    id_alquiler = Column(Integer, ForeignKey("alquileres.id"), nullable=False)

    tipo = Column(String, nullable=False)
    descripcion = Column(String)
    costo = Column(Float, nullable=False)

    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación con Alquiler
    alquiler = relationship("Alquiler", back_populates="multas")
