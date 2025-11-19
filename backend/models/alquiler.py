from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.database import Base  # 👈 importante este import
from sqlalchemy.orm import relationship


class Alquiler(Base):
    __tablename__ = "alquileres"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    id_empleado = Column(Integer, ForeignKey("empleados.id"), nullable=False)
    fecha_inicio = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_fin = Column(DateTime)
    costo_total = Column(Integer)
    kilometraje_inicial = Column(Integer)
    kilometraje_final = Column(Integer)
    estado = Column(String, default="activo")  # activo, finalizado, cancelado

    cliente = relationship("Cliente")
    vehiculo = relationship("Vehiculo")
    empleado = relationship("Empleado")     