from datetime import datetime
from fastapi import HTTPException
import calendar
from .base import PeriodoStrategy

class PeriodoTrimestralStrategy(PeriodoStrategy):
    def calcular_rango(self, anio: int, valor: int | None):
        if valor is None:
            raise HTTPException(400, "Debe especificar el trimestre (valor).")

        if valor < 1 or valor > 4:
            raise HTTPException(400, "El trimestre debe ser 1, 2, 3 o 4.")

        mes_inicio = (valor - 1) * 3 + 1
        mes_fin = mes_inicio + 2

        ultimo_dia = calendar.monthrange(anio, mes_fin)[1]

        fecha_inicio = datetime(anio, mes_inicio, 1)
        fecha_fin = datetime(anio, mes_fin, ultimo_dia, 23, 59, 59)

        return fecha_inicio, fecha_fin
