from abc import ABC, abstractmethod
from datetime import datetime

class PeriodoStrategy(ABC):

    @abstractmethod
    def calcular_rango(self, anio: int, valor: int | None):
        pass
