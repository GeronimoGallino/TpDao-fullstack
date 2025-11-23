from datetime import datetime, timezone
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from backend.database import Base  # 👈 correcto
from sqlalchemy.orm import relationship

class Mantenimiento(Base):
    __tablename__ = "mantenimientos"

    id = Column(Integer, primary_key=True, index=True)
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    id_empleado = Column(Integer, ForeignKey("empleados.id"), nullable=False)
    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    km_actual = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)  # preventivo, correctivo, etc.
    costo = Column(Integer, nullable=False)
    observaciones = Column(String)

    vehiculo = relationship("Vehiculo", back_populates="mantenimientos")

