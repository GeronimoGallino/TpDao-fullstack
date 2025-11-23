from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from datetime import datetime
import calendar

from .. import models
from ..schemas.alquiler import AlquilerClienteDetalle
from sqlalchemy import func


# =======================================================
# ALQUILERES POR CLIENTE
# =======================================================
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


# =======================================================
# VEHÍCULOS MÁS ALQUILADOS
# =======================================================
def get_vehiculos_mas_alquilados(db: Session, limite: int):
    resultados = (
        db.query(
            models.Vehiculo,
            func.count(models.Alquiler.id).label("cantidad_alquileres")
        )
        .join(models.Alquiler, models.Vehiculo.id == models.Alquiler.id_vehiculo)
        .group_by(models.Vehiculo.id)
        .order_by(func.count(models.Alquiler.id).desc())
        .limit(limite)
        .all()
    )
    return resultados


# =======================================================
# FUNCIÓN AUXILIAR - CALCULAR RANGO DEL PERIODO
# =======================================================
def _calcular_rango_periodo(tipo: str, anio: int, valor: int | None):
    tipo = tipo.lower()

    if tipo == "anual":
        fecha_inicio = datetime(anio, 1, 1)
        fecha_fin = datetime(anio, 12, 31, 23, 59, 59)

    elif tipo == "mensual":
        if valor is None:
            raise HTTPException(400, "Debe especificar el mes (valor).")

        if valor < 1 or valor > 12:
            raise HTTPException(400, "El mes debe estar entre 1 y 12.")

        ultimo_dia = calendar.monthrange(anio, valor)[1]

        fecha_inicio = datetime(anio, valor, 1)
        fecha_fin = datetime(anio, valor, ultimo_dia, 23, 59, 59)

    elif tipo == "trimestral":
        if valor is None:
            raise HTTPException(400, "Debe especificar el trimestre (valor).")

        if valor < 1 or valor > 4:
            raise HTTPException(400, "El trimestre debe ser 1, 2, 3 o 4.")

        mes_inicio = (valor - 1) * 3 + 1
        mes_fin = mes_inicio + 2

        ultimo_dia = calendar.monthrange(anio, mes_fin)[1]

        fecha_inicio = datetime(anio, mes_inicio, 1)
        fecha_fin = datetime(anio, mes_fin, ultimo_dia, 23, 59, 59)

    else:
        raise HTTPException(400, "Tipo inválido. Use: mensual, trimestral o anual.")

    return fecha_inicio, fecha_fin


# =======================================================
# ALQUILERES POR PERIODO
# =======================================================
def alquileres_por_periodo(db: Session, tipo: str, anio: int, valor: int | None):

    # 1️⃣ Calcular rango del período
    fecha_inicio, fecha_fin = _calcular_rango_periodo(tipo, anio, valor)

    # 2️⃣ Traer alquileres dentro del periodo
    alquileres = (
        db.query(models.Alquiler)
        .options(
            joinedload(models.Alquiler.vehiculo),
            joinedload(models.Alquiler.empleado),
            joinedload(models.Alquiler.cliente)
        )
        .filter(models.Alquiler.fecha_inicio >= fecha_inicio)
        .filter(models.Alquiler.fecha_fin != None)
        .filter(models.Alquiler.fecha_fin <= fecha_fin)
        .all()
    )

    # 3️⃣ Devolver formato final usando tu schema AlquilerClienteDetalle
    return {
        "cantidad_alquileres": len(alquileres),
        "alquileres": [AlquilerClienteDetalle.model_validate(a) for a in alquileres]
    }
