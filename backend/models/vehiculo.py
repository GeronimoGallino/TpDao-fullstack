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
        fecha_actual = datetime.now(timezone.utc)

        if self.mantenimientos:
            ultimo = self.mantenimientos[-1]

            # Normalizar fecha del último mantenimiento
            fecha_mant = ultimo.fecha
            if fecha_mant.tzinfo is None:
                fecha_mant = fecha_mant.replace(tzinfo=timezone.utc)

            return ultimo.calcular_proximo_mantenimiento(
                kilometraje_actual=self.kilometraje,
                fecha_actual=fecha_actual
            )
        else:
        # fallback seguro
            return {
                "proximo_km": self.kilometraje + INTERVALO_KM_DEFAULT,
                "proxima_fecha": fecha_actual + timedelta(days=30*INTERVALO_MESES_DEFAULT),
                "alerta_km": False,
                "alerta_fecha": False
        }
        
        """
        # ────────────────────────────────────────────────
        # Caso 2: no hay mantenimientos → calcular manualmente con defaults
        # ────────────────────────────────────────────────

        else:
            ultima_fecha = self.fecha_registro
            if ultima_fecha.tzinfo is None:
                ultima_fecha = ultima_fecha.replace(tzinfo=timezone.utc)

            proximo_km = 0 + INTERVALO_KM_DEFAULT
            proxima_fecha = Mantenimiento._sumar_meses(
                self,
                fecha=ultima_fecha,
                meses=INTERVALO_MESES_DEFAULT
            )

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
    """

    @property
    def necesita_mantenimiento(self) -> bool:
        datos = self.consultar_proximo_mantenimiento() or {}
        print("Vehiculo: ", self.marca, ". Datos mantenimiento:", datos)
        return bool(datos.get("alerta_km")) or bool(datos.get("alerta_fecha"))


    #def actualizar_kilometraje(self, km_realizados: int):
    #    self.kilometraje = self.kilometraje + km_realizados

    #def registrar_mantenimiento(self, mantenimiento):
    #    self.mantenimientos.append(mantenimiento)

    #def obtener_historial_mantenimientos(self):
    #    return self.mantenimientos
    


    