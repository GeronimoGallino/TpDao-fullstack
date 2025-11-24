from fastapi import HTTPException
from .anual import PeriodoAnualStrategy
from .mensual import PeriodoMensualStrategy
from .trimestral import PeriodoTrimestralStrategy

class PeriodoCalculator:

    def obtener_strategy(self, tipo: str):
        tipo = tipo.lower()

        if tipo == "anual":
            return PeriodoAnualStrategy()
        if tipo == "mensual":
            return PeriodoMensualStrategy()
        if tipo == "trimestral":
            return PeriodoTrimestralStrategy()

        raise HTTPException(400, "Tipo inválido. Use: mensual, trimestral o anual.")
