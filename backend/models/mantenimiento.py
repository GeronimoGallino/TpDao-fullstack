from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from backend.database import Base  # 👈 correcto
from sqlalchemy.orm import relationship

class Mantenimiento(Base):
    __tablename__ = "mantenimientos"

    id = Column(Integer, primary_key=True, index=True)

    # Relación con Vehículo y Empleado
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    id_empleado = Column(Integer, ForeignKey("empleados.id"), nullable=False)

    # Datos del mantenimiento realizado
    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    km_actual = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)  # preventivo, correctivo, etc.
    costo = Column(Integer, nullable=False)
    observaciones = Column(String)

    # Campos provenientes del plan (opcionales)
    km_prox_mant = Column(Integer, default=10000, nullable=False)
    meses_prox_mant = Column(Integer, default=12, nullable=False)


    vehiculo = relationship("Vehiculo", back_populates="mantenimientos")
    empleado = relationship("Empleado", back_populates="mantenimientos")

    def _sumar_meses(self, fecha: datetime, meses: int) -> datetime:
        """
        Suma meses correctamente sin errores de validación.
        """
        mes = fecha.month - 1 + meses
        año = fecha.year + mes // 12
        mes = mes % 12 + 1
        dia = min(
            fecha.day,
            [
                31,
                29 if año % 4 == 0 and (año % 100 != 0 or año % 400 == 0) else 28,
                31, 30, 31, 30, 31, 31, 30, 31, 30, 31,
            ][mes - 1],
        )
        return fecha.replace(year=año, month=mes, day=dia, tzinfo=fecha.tzinfo or timezone.utc)

    
    def _calcular_alertas(
        self,
        kilometraje_actual: int,
        fecha_actual: datetime,
        proximo_km: int,
        proxima_fecha: datetime
    ):
        """Calcula si corresponde emitir alertas de mantenimiento."""

        alerta_km = kilometraje_actual >= proximo_km - 1000

        # Normalizar ambas fechas a UTC
        if fecha_actual.tzinfo is None:
            fecha_actual = fecha_actual.replace(tzinfo=timezone.utc)
        else:
            fecha_actual = fecha_actual.astimezone(timezone.utc)

        if proxima_fecha.tzinfo is None:
            proxima_fecha = proxima_fecha.replace(tzinfo=timezone.utc)
        else:
            proxima_fecha = proxima_fecha.astimezone(timezone.utc)

        fecha_alerta = proxima_fecha - timedelta(days=15)
        alerta_fecha = fecha_actual >= fecha_alerta

        return alerta_km, alerta_fecha
    
    def calcular_proximo_mantenimiento(
        self,
        kilometraje_actual: int,
        fecha_actual: datetime
    ):
        """
        Calcula el próximo mantenimiento basado en los datos del mantenimiento actual.
        """

        # Cálculo del próximo mantenimiento
        proximo_km = self.km_actual + self.km_prox_mant
        fecha_base = self.fecha
        if fecha_base.tzinfo is None:
            fecha_base = fecha_base.replace(tzinfo=timezone.utc)

        proxima_fecha = self._sumar_meses(fecha_base, self.meses_prox_mant)

        # Cálculo de alertas
        alerta_km, alerta_fecha = self._calcular_alertas(
            kilometraje_actual=kilometraje_actual,
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

    
