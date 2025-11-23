from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.mantenimiento import Mantenimiento
from .. import database
from ..schemas import mantenimiento as schemas

router = APIRouter(prefix="/mantenimientos", tags=["Mantenimientos"])

@router.post("/", response_model=schemas.Mantenimiento)
def crear_mantenimiento(mantenimiento: schemas.MantenimientoCreate, db: Session = Depends(database.get_db)):
    nuevo_mantenimiento = Mantenimiento(**mantenimiento.model_dump())
    db.add(nuevo_mantenimiento)
    db.commit()
    db.refresh(nuevo_mantenimiento)
    return nuevo_mantenimiento

@router.get("/", response_model=list[schemas.Mantenimiento])
def listar_mantenimientos(db: Session = Depends(database.get_db)):
    return db.query(Mantenimiento).all()

@router.get("/{mantenimiento_id}", response_model=schemas.Mantenimiento)
def obtener_mantenimiento(mantenimiento_id: int, db: Session = Depends(database.get_db)):
    mantenimiento = db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return mantenimiento

@router.put("/{mantenimiento_id}", response_model=schemas.Mantenimiento)
def actualizar_mantenimiento(mantenimiento_id: int, datos: schemas.MantenimientoCreate, db: Session = Depends(database.get_db)):
    mantenimiento = db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    for key, value in datos.model_dump().items():
        setattr(mantenimiento, key, value)
    db.commit()
    db.refresh(mantenimiento)
    return mantenimiento  

@router.delete("/{mantenimiento_id}")
def eliminar_mantenimiento(mantenimiento_id: int, db: Session = Depends(database.get_db)):
    mantenimiento = db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    db.delete(mantenimiento)
    db.commit()
    return {"mensaje": "Mantenimiento eliminado correctamente"}

