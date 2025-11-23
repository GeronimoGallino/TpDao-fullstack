from datetime import date, datetime, timezone
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

    def __repr__(self):
        return f"<Vehiculo(id={self.id}, marca={self.marca}, modelo={self.modelo}, patente={self.patente})>"
    
    def asignar_plan_mantenimiento(self, plan_mantenimiento):
        self.plan_mantenimiento = plan_mantenimiento

    def validar_disponibilidad(self): #Buscar en alquileres activos (o activos a esa fecha) si el vehiculo está alquilado o no
        pass

    def registrar_mantenimiento(self, mantenimiento: Mantenimiento):
        self.mantenimientos.append(mantenimiento)

    def obtener_historial_mantenimientos(self):
        return self.mantenimientos
    
    def consultar_proximo_mantenimiento(self):
        if not self.plan_mantenimiento:
            raise ValueError("El vehículo no tiene un plan de mantenimiento asignado.")
        
        ultimo_mant = self.mantenimientos[-1] if self.mantenimientos else None

        resultado = self.plan_mantenimiento.calcular_proximo_mantenimiento(
            ultimo_km=ultimo_mant.km_actual if ultimo_mant else 0,
            ultimo_fecha=ultimo_mant.fecha if ultimo_mant else self.fecha_registro,
            fecha_actual=datetime.now(timezone.utc),
            kilometraje_actual=self.kilometraje
        )

        print("Proximo mantenimiento calculado:", resultado["proximo_km"], resultado["proxima_fecha"], resultado["alerta_km"], resultado["alerta_fecha"])

        return {
            "proximo_km": resultado["proximo_km"],
            "proxima_fecha": resultado["proxima_fecha"],
            "alerta_km": bool(resultado["alerta_km"]),
            "alerta_fecha": bool(resultado["alerta_fecha"])
        }



    #def actualizar_kilometraje(self, km_realizados: int):
    #    self.kilometraje = self.kilometraje + km_realizados

    #def registrar_mantenimiento(self, mantenimiento):
    #    self.mantenimientos.append(mantenimiento)

    #def obtener_historial_mantenimientos(self):
    #    return self.mantenimientos
    


    