from datetime import datetime, timezone
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from backend.database import Base  # 👈 correcto

class PlanMantenimiento(Base):
    __tablename__ = "planes_mantenimiento"

    id = Column(Integer, primary_key=True, index=True)
    tipo_vehiculo = Column(String, nullable=False)  # auto, camioneta, moto, etc.
    km_intervalo = Column(Integer, nullable=False)  # cada cuantos km se realiza el mantenimiento
    meses_intervalo = Column(Integer, nullable=False)  # cada cuantos meses se realiza el mantenimiento

    def calcular_proximo_mantenimiento(self, ultimo_km: int, ultimo_fecha: datetime):
        proximo_km = ultimo_km + self.km_intervalo
        proxima_fecha = ultimo_fecha.replace(
            year=ultimo_fecha.year + (ultimo_fecha.month + self.meses_intervalo - 1) // 12,
            month=(ultimo_fecha.month + self.meses_intervalo - 1) % 12 + 1
        )
        return proximo_km, proxima_fecha
    
    def calcular_alertas(self, kilometraje_actual: int, fecha_actual: datetime, ultimo_km: int, ultimo_fecha: datetime):
        proximo_km, proxima_fecha = self.calcular_proximo_mantenimiento(ultimo_km, ultimo_fecha)
        alerta_km = kilometraje_actual >= proximo_km - 1000  # alerta 1000 km antes
        alerta_fecha = fecha_actual >= proxima_fecha.replace(day=proxima_fecha.day - 15)  # alerta 15 días antes
        return alerta_km, alerta_fecha
    
    