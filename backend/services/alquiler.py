from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone
import math

from sqlalchemy.orm import joinedload
from .. import models
from ..schemas import alquiler as schemas


# -------------------------------------------------------------------
# ✔ Funciones internas (privadas) para validaciones
# -------------------------------------------------------------------

def _validar_cliente_activo(db: Session, id_cliente: int):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id_cliente == id_cliente,
        models.Cliente.estado == True
    ).first()

    if not cliente:
        raise HTTPException(status_code=400, detail="Cliente no existe o está eliminado")

    return cliente


def _validar_vehiculo_disponible(db: Session, id_vehiculo: int):
    vehiculo = db.query(models.Vehiculo).filter(
        models.Vehiculo.id == id_vehiculo,
        models.Vehiculo.disponible == True
    ).first()

    if not vehiculo:
        raise HTTPException(status_code=400, detail="Vehículo no existe o no está disponible")

    return vehiculo


def _validar_empleado_activo(db: Session, id_empleado: int):
    empleado = db.query(models.Empleado).filter(
        models.Empleado.id == id_empleado,
        models.Empleado.estado == True
    ).first()

    if not empleado:
        raise HTTPException(status_code=400, detail="Empleado no existe o está inactivo")

    return empleado


def _obtener_alquiler_activo(db: Session, alquiler_id: int):
    alquiler = db.query(models.Alquiler).filter(
        models.Alquiler.id == alquiler_id,
        models.Alquiler.estado == "activo"
    ).first()

    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado o ya finalizado/cancelado")

    return alquiler


# -------------------------------------------------------------------
# ✔ Función genérica para disponibilidad del vehículo
# -------------------------------------------------------------------

def _set_disponibilidad_vehiculo(db: Session, vehiculo: models.Vehiculo, disponible: bool):
    vehiculo.disponible = disponible
    db.add(vehiculo)


# -------------------------------------------------------------------
# ✔ Crear alquiler
# -------------------------------------------------------------------

def crear_alquiler(datos: schemas.AlquilerCreate, db: Session):
    # Validaciones
    _validar_cliente_activo(db, datos.id_cliente)
    vehiculo = _validar_vehiculo_disponible(db, datos.id_vehiculo)
    _validar_empleado_activo(db, datos.id_empleado)

    # Cambiar disponibilidad del vehículo → NOTA IMPORTANTE
    _set_disponibilidad_vehiculo(db, vehiculo, False)

    # Crear alquiler
    nuevo_alquiler = models.Alquiler(**datos.model_dump())
    db.add(nuevo_alquiler)

    # Guardar cambios
    db.commit()
    db.refresh(nuevo_alquiler)

    return nuevo_alquiler


# -------------------------------------------------------------------
# ✔ Listar alquileres activos
# -------------------------------------------------------------------

def listar_activos(db: Session):
    return db.query(models.Alquiler).filter(
        models.Alquiler.estado == "activo"
    ).all()


# -------------------------------------------------------------------
# ✔ Obtener alquiler por ID
# -------------------------------------------------------------------

def obtener_alquiler(alquiler_id: int, db: Session):
    alquiler = db.query(models.Alquiler).filter(models.Alquiler.id == alquiler_id).first()

    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    return alquiler


# -------------------------------------------------------------------
# ✔ Finalizar alquiler
# -------------------------------------------------------------------

def finalizar_alquiler(alquiler_id: int, datos: schemas.AlquilerFinalizar, db: Session):
    # 1) Obtener alquiler activo
    alquiler = _obtener_alquiler_activo(db, alquiler_id)

    # 2) Fecha fin UTC
    fecha_fin = datetime.now(timezone.utc)

    # 3) Normalizar fecha_inicio
    fecha_inicio = alquiler.fecha_inicio
    if fecha_inicio.tzinfo is None:
        fecha_inicio = fecha_inicio.replace(tzinfo=timezone.utc)
    else:
        fecha_inicio = fecha_inicio.astimezone(timezone.utc)

    # 4) Obtener vehículo asociado
    vehiculo = db.query(models.Vehiculo).filter(
        models.Vehiculo.id == alquiler.id_vehiculo
    ).first()

    if not vehiculo:
        raise HTTPException(status_code=400, detail="Vehículo asociado no existe")

    # 5) Calcular días de alquiler
    diferencia = fecha_fin - fecha_inicio
    dias = math.ceil(diferencia.total_seconds() / 86400)
    dias = max(dias, 1)  # mínimo 1 día

    # 6) Calcular costo total
    if vehiculo.costo_diario is None:
        raise HTTPException(status_code=500, detail="El vehículo no tiene costo_diario definido")

    costo_total = dias * vehiculo.costo_diario

    # 7) Actualizar alquiler
    alquiler.fecha_fin = fecha_fin
    alquiler.kilometraje_final = datos.kilometraje_final
    alquiler.costo_total = costo_total
    alquiler.estado = "finalizado"

    # 8) Liberar vehículo (disponible = True)
    _set_disponibilidad_vehiculo(db, vehiculo, True)
    vehiculo.kilometraje = datos.kilometraje_final

    db.commit()
    db.refresh(alquiler)

    return alquiler


# -------------------------------------------------------------------
# ✔ Cancelar alquiler (borrado lógico)
# -------------------------------------------------------------------

def cancelar_alquiler(alquiler_id: int, db: Session):
    alquiler = _obtener_alquiler_activo(db, alquiler_id)

    alquiler.estado = "cancelado"

    # Hacemos el vehículo disponible nuevamente
    vehiculo = db.query(models.Vehiculo).filter(
        models.Vehiculo.id == alquiler.id_vehiculo
    ).first()

    if vehiculo:
        _set_disponibilidad_vehiculo(db, vehiculo, True)

    db.commit()

    return {"mensaje": "Alquiler cancelado"}


# -------------------------------------------------------------------
# ✔ Traer alquileres por cliente
# -------------------------------------------------------------------

def get_alquileres_por_cliente(db: Session, cliente_id: int):
    alquileres = (
        db.query(models.Alquiler)
        .options(
            joinedload(models.Alquiler.vehiculo),
            joinedload(models.Alquiler.empleado)
        )
        .filter(models.Alquiler.id_cliente == cliente_id)
        .all()
    )
    return alquileres