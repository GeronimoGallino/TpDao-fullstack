from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from backend.database import Base  # 👈 correcto

class PlanMantenimiento(Base):
    __tablename__ = "planes_mantenimiento"

    id = Column(Integer, primary_key=True, index=True)
    tipo_vehiculo = Column(String, nullable=False)  # auto, camioneta, moto, etc.
    km_intervalo = Column(Integer, nullable=False)  # cada cuantos km se realiza el mantenimiento
    meses_intervalo = Column(Integer, nullable=False)  # cada cuantos meses se realiza el mantenimiento

    def _sumar_meses(self, fecha: datetime, meses: int) -> datetime:
        """Suma meses correctamente sin generar errores de fecha."""
        mes = fecha.month - 1 + meses
        año = fecha.year + mes // 12
        mes = mes % 12 + 1
        dia = min(fecha.day, [31,
            29 if año % 4 == 0 and (año % 100 != 0 or año % 400 == 0) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mes - 1])
        return fecha.replace(year=año, month=mes, day=dia, tzinfo=fecha.tzinfo)
    


    def calcular_proximo_mantenimiento(
            self,
            ultimo_km: int,
            ultimo_fecha: datetime,
            kilometraje_actual: int,
            fecha_actual: datetime
        ):
        """
        Calcula el próximo mantenimiento y además llama al método interno
        de alertas para determinar si corresponde emitir avisos.
        """

        # Cálculo del próximo mantenimiento
        proximo_km = ultimo_km + self.km_intervalo
        proxima_fecha = self._sumar_meses(ultimo_fecha, self.meses_intervalo)

        # Llamar al método interno de alertas
        alerta_km, alerta_fecha = self._calcular_alertas(
            kilometraje_actual=kilometraje_actual,
            fecha_actual=fecha_actual,
            proximo_km=proximo_km,
            proxima_fecha=proxima_fecha
        )

        print("[]Proximo mantenimiento calculado:", proximo_km, proxima_fecha, alerta_km, alerta_fecha)

        return {
            "proximo_km": proximo_km,
            "proxima_fecha": proxima_fecha,
            "alerta_km": alerta_km,
            "alerta_fecha": alerta_fecha
        }


    def _calcular_alertas(
            self,
            kilometraje_actual: int,
            fecha_actual: datetime,
            proximo_km: int,
            proxima_fecha: datetime
        ):
        """
        Método interno: calcula únicamente las alertas.
        """

        # alerta por km → dentro de 1000 km del mantenimiento
        alerta_km = kilometraje_actual >= proximo_km - 1000

        # alerta por fecha → dentro de los últimos 15 días antes del límite
        fecha_alerta = proxima_fecha - timedelta(days=15)
        alerta_fecha = fecha_actual.replace(tzinfo=None) >= fecha_alerta

        return alerta_km, alerta_fecha
    