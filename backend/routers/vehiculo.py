from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.vehiculo import Vehiculo
from .. import database
from ..schemas import vehiculo as schemas

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])

@router.post("/", response_model=schemas.Vehiculo)
def crear_vehiculo(vehiculo: schemas.VehiculoCreate, db: Session = Depends(database.get_db)):
    nuevo_vehiculo = Vehiculo(**vehiculo.dict())
    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)
    return nuevo_vehiculo

@router.get("/", response_model=list[schemas.Vehiculo])
def listar_vehiculos(db: Session = Depends(database.get_db)):
    return db.query(Vehiculo).all()

@router.get("/{vehiculo_id}", response_model=schemas.Vehiculo)
def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(database.get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

@router.put("/{vehiculo_id}", response_model=schemas.Vehiculo)
def actualizar_vehiculo(vehiculo_id: int, datos: schemas.VehiculoCreate, db: Session = Depends(database.get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    for key, value in datos.dict().items():
        setattr(vehiculo, key, value)
    db.commit()
    db.refresh(vehiculo)
    return vehiculo

@router.delete("/{vehiculo_id}")
def eliminar_vehiculo(vehiculo_id: int, db: Session = Depends(database.get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    db.delete(vehiculo)
    db.commit()
    return {"mensaje": "Vehículo eliminado correctamente"}
