from .observer import Observer
from datetime import datetime, timezone

class AlertasMantenimientoObserver(Observer):
    def update(self, event_name: str, data: dict):
        vehiculo = data["vehiculo"]
        
        # Invocar la property para recalcular
        alerta = vehiculo.necesita_mantenimiento

        # Podés decidir qué hacer con ese valor:
        if alerta:
            print(f"⚠️ Vehículo {vehiculo.id} requiere mantenimiento")
        else:
            print(f"✅ Vehículo {vehiculo.id} al día")
