from datetime import datetime
from fastapi import HTTPException
import calendar
from .base import PeriodoStrategy

class PeriodoMensualStrategy(PeriodoStrategy):
    def calcular_rango(self, anio: int, valor: int | None):
        if valor is None:
            raise HTTPException(400, "Debe especificar el mes (valor).")

        if valor < 1 or valor > 12:
            raise HTTPException(400, "El mes debe estar entre 1 y 12.")

        ultimo_dia = calendar.monthrange(anio, valor)[1]

        fecha_inicio = datetime(anio, valor, 1)
        fecha_fin = datetime(anio, valor, ultimo_dia, 23, 59, 59)

        return fecha_inicio, fecha_fin
