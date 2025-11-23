from datetime import datetime, timezone
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base  # 👈 correcto
from .mantenimiento import Mantenimiento

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
    mantenimientos = relationship(
        "Mantenimiento",
        back_populates="vehiculo",
        cascade="all, delete-orphan"
    )
    plan_mantenimiento_id = Column(Integer, ForeignKey("planes_mantenimiento.id"))

    plan_mantenimiento = relationship("PlanMantenimiento")


    def actualizar_kilometraje(self, km_realizados: int):
        self.kilometraje = self.kilometraje + km_realizados

    def registrar_mantenimiento(self, mantenimiento):
        self.mantenimientos.append(mantenimiento)

    def obtener_historial_mantenimientos(self):
        return self.mantenimientos
    


    