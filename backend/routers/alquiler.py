from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from ..schemas import alquiler as schemas
from datetime import datetime, timezone
import math
router = APIRouter(prefix="/alquileres", tags=["Alquileres"])


# ------------------------------
#  Crear alquiler
# ------------------------------
@router.post("/", response_model=schemas.Alquiler)
def crear_alquiler(alquiler: schemas.AlquilerCreate, db: Session = Depends(database.get_db)):

    # A) Verificar cliente activo
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id_cliente == alquiler.id_cliente,
        models.Cliente.estado == True
    ).first()

    if not cliente:
        raise HTTPException(status_code=400, detail="Cliente no existe o está eliminado")

    # B) Verificar vehículo disponible → no debe tener un alquiler activo
    alquiler_activo = db.query(models.Vehiculo).filter(
        models.Vehiculo.id == alquiler.id_vehiculo,
        models.Vehiculo.disponible == True
    ).first()

    if not alquiler_activo:
        raise HTTPException(status_code=400, detail="Vehículo no existe o está eliminado")


    # C) Verificar empleado activo
    empleado = db.query(models.Empleado).filter(
        models.Empleado.id == alquiler.id_empleado,
        models.Empleado.estado == True
    ).first()

    if not empleado:
        raise HTTPException(status_code=400, detail="Empleado no existe o está inactivo")

    # Crear alquiler
    nuevo_alquiler = models.Alquiler(**alquiler.model_dump())
    db.add(nuevo_alquiler)
    db.commit()
    db.refresh(nuevo_alquiler)

    return nuevo_alquiler


# ------------------------------
#  Listar alquileres activos
# ------------------------------
@router.get("/", response_model=list[schemas.Alquiler])
def listar_alquileres(db: Session = Depends(database.get_db)):
    return db.query(models.Alquiler).filter(models.Alquiler.estado == "activo").all()


# ------------------------------
# Obtener alquiler por ID
# ------------------------------
@router.get("/{alquiler_id}", response_model=schemas.Alquiler)
def obtener_alquiler(alquiler_id: int, db: Session = Depends(database.get_db)):

    alquiler = db.query(models.Alquiler).filter(models.Alquiler.id == alquiler_id).first()

    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    return alquiler


# ------------------------------
# Finalizar alquiler
# ------------------------------
@router.put("/{alquiler_id}/finalizar", response_model=schemas.Alquiler)
def finalizar_alquiler(
    alquiler_id: int,
    datos: schemas.AlquilerFinalizar,   # el front envía solo kilometraje_final
    db: Session = Depends(database.get_db)
):

    alquiler = db.query(models.Alquiler).filter(
        models.Alquiler.id == alquiler_id,
        models.Alquiler.estado == "activo"
    ).first()

    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado o ya finalizado")

    # 1. Fecha de finalización = ahora (ignora lo que mande el front)
    fecha_fin = datetime.now(timezone.utc)
    # 2. Obtener vehículo asociado
    vehiculo = db.query(models.Vehiculo).filter(
        models.Vehiculo.id == alquiler.id_vehiculo
    ).first()

    if not vehiculo:
        raise HTTPException(status_code=400, detail="Vehículo asociado no existe")
    
    if alquiler.fecha_inicio.tzinfo is None:
        ### FIX 2A: Si viene naïve desde la BD, lo convertimos a UTC
        fecha_inicio = alquiler.fecha_inicio.replace(tzinfo=timezone.utc)
    else:
        ### FIX 2B: Si ya tiene TZ, forzamos a UTC para que coincida
        fecha_inicio = alquiler.fecha_inicio.astimezone(timezone.utc)

    # 3. Calcular días de alquiler
    diferencia = fecha_fin - alquiler.fecha_inicio
    dias = math.ceil(diferencia.total_seconds() / 86400)  # redondear hacia arriba

    # 4. Costo total
    if not hasattr(vehiculo, "costo_diario"):
        raise HTTPException(status_code=500, detail="El vehículo no tiene costo_diario definido")

    costo_total = dias * vehiculo.costo_diario

    # 5. Aplicar actualizaciones al alquiler
    alquiler.fecha_fin = fecha_fin
    alquiler.kilometraje_final = datos.kilometraje_final
    alquiler.costo_total = costo_total
    alquiler.estado = "finalizado"

    # 6. Actualizar vehículo (marcar disponible + km final)
    vehiculo.disponible = True
    if datos.kilometraje_final:
        vehiculo.kilometraje = datos.kilometraje_final

    db.commit()
    db.refresh(alquiler)

    return alquiler

# ------------------------------
# Cancelar alquiler (borrado lógico)
# ------------------------------
@router.delete("/{alquiler_id}")
def cancelar_alquiler(alquiler_id: int, db: Session = Depends(database.get_db)):

    alquiler = db.query(models.Alquiler).filter(
        models.Alquiler.id == alquiler_id,
        models.Alquiler.estado == "activo"
    ).first()

    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado o ya cancelado")

    alquiler.estado = "cancelado"
    db.commit()

    return {"mensaje": "Alquiler cancelado"}
