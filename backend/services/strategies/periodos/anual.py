from datetime import datetime
from .base import PeriodoStrategy

class PeriodoAnualStrategy(PeriodoStrategy):
    def calcular_rango(self, anio: int, valor: int | None):
        fecha_inicio = datetime(anio, 1, 1)
        fecha_fin = datetime(anio, 12, 31, 23, 59, 59)
        return fecha_inicio, fecha_fin
