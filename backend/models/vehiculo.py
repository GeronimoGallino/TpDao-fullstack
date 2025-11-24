from datetime import date, datetime, timezone, timedelta
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base  # 👈 correcto
from .mantenimiento import Mantenimiento

# CONFIGURACIÓN GLOBAL DEL SISTEMA
INTERVALO_KM_DEFAULT = 10000
INTERVALO_MESES_DEFAULT = 12

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


    def __repr__(self):
        return f"<Vehiculo(id={self.id}, marca={self.marca}, modelo={self.modelo}, patente={self.patente})>"
    

    def validar_disponibilidad(self): #Buscar en alquileres activos (o activos a esa fecha) si el vehiculo está alquilado o no
        pass

    def registrar_mantenimiento(self, mantenimiento: Mantenimiento):
        self.mantenimientos.append(mantenimiento)

    def obtener_historial_mantenimientos(self):
        return self.mantenimientos
    
    def consultar_proximo_mantenimiento(self):

        """
        Delegar el cálculo al último mantenimiento registrado.
        Si no hay mantenimientos, usa los valores por defecto del vehículo.
        """

        fecha_actual = datetime.now(timezone.utc)

        # ────────────────────────────────────────────────
        # Caso 1: hay mantenimientos → usar el último
        # ────────────────────────────────────────────────
        if self.mantenimientos:
            ultimo = self.mantenimientos[-1]

            # Delegar cálculo al mantenimiento
            return ultimo.calcular_proximo_mantenimiento(
                kilometraje_actual=self.kilometraje,
                fecha_actual=fecha_actual
            )

        # ────────────────────────────────────────────────
        # Caso 2: no hay mantenimientos → calcular manualmente con defaults
        # ────────────────────────────────────────────────
        else:
            # Daten por defecto
            ultimo_km = 0
            ultima_fecha = self.fecha_registro

            # Asegurar tzinfo
            if ultima_fecha.tzinfo is None:
                ultima_fecha = ultima_fecha.replace(tzinfo=timezone.utc)

            proximo_km = ultimo_km + INTERVALO_KM_DEFAULT

            # Sumar meses correctamente usando la misma lógica que Mantenimiento usa
            proxima_fecha = Mantenimiento._sumar_meses(
                self,
                fecha=ultima_fecha,
                meses=INTERVALO_MESES_DEFAULT
            )

            # Calcular alertas con el mismo criterio
            alerta_km, alerta_fecha = Mantenimiento._calcular_alertas(
                self,
                kilometraje_actual=self.kilometraje,
                fecha_actual=fecha_actual,
                proximo_km=proximo_km,
                proxima_fecha=proxima_fecha
            )

            return {
                "proximo_km": proximo_km,
                "proxima_fecha": proxima_fecha,
                "alerta_km": alerta_km,
                "alerta_fecha": alerta_fecha
            }



    #def actualizar_kilometraje(self, km_realizados: int):
    #    self.kilometraje = self.kilometraje + km_realizados

    #def registrar_mantenimiento(self, mantenimiento):
    #    self.mantenimientos.append(mantenimiento)

    #def obtener_historial_mantenimientos(self):
    #    return self.mantenimientos
    


    