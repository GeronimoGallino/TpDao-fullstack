from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database
from ..schemas import mantenimiento as schemas
from backend.services import mantenimiento as service

router = APIRouter(prefix="/mantenimientos", tags=["Mantenimientos"])


@router.post("/", response_model=schemas.Mantenimiento)
def crear_mant(data: schemas.MantenimientoCreate, db: Session = Depends(database.get_db)):
    return service.crear_mantenimiento(db, data)


@router.get("/", response_model=list[schemas.Mantenimiento])
def listar(db: Session = Depends(database.get_db)):
    return service.listar_mantenimientos(db)


@router.get("/{mantenimiento_id}", response_model=schemas.Mantenimiento)
def obtener(mantenimiento_id: int, db: Session = Depends(database.get_db)):
    return service.obtener_mantenimiento(db, mantenimiento_id)


@router.put("/{mantenimiento_id}", response_model=schemas.Mantenimiento)
def actualizar(mantenimiento_id: int, data: schemas.MantenimientoCreate, db: Session = Depends(database.get_db)):
    return service.actualizar_mantenimiento(db, mantenimiento_id, data)


@router.delete("/{mantenimiento_id}")
def eliminar(mantenimiento_id: int, db: Session = Depends(database.get_db)):
    service.eliminar_mantenimiento(db, mantenimiento_id)
    return {"mensaje": "Mantenimiento eliminado correctamente"}