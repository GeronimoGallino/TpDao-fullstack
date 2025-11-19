from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from ..schemas import alquiler as schemas

router = APIRouter(prefix="/alquileres", tags=["Alquileres"])

@router.post("/", response_model=schemas.Alquiler)
def crear_alquiler(alquiler: schemas.AlquilerCreate, db: Session = Depends(database.get_db)):
    nuevo_alquiler = models.Alquiler(**alquiler.dict())
    db.add(nuevo_alquiler)
    db.commit()
    db.refresh(nuevo_alquiler)
    return nuevo_alquiler

@router.get("/", response_model=list[schemas.Alquiler])
def listar_alquileres(db: Session = Depends(database.get_db)):
    return db.query(models.Alquiler).all()

@router.get("/{alquiler_id}", response_model=schemas.Alquiler)
def obtener_alquiler(alquiler_id: int, db: Session = Depends(database.get_db)):
    alquiler = db.query(models.Alquiler).filter(models.Alquiler.id == alquiler_id).first()
    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    return alquiler

@router.put("/{alquiler_id}", response_model=schemas.Alquiler)
def actualizar_alquiler(alquiler_id: int, datos: schemas.AlquilerCreate, db:
    Session = Depends(database.get_db)):
    alquiler = db.query(models.Alquiler).filter(models.Alquiler.id == alquiler_id).first()
    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    for key, value in datos.dict().items():
        setattr(alquiler, key, value)
    db.commit()
    db.refresh(alquiler)
    return alquiler

@router.delete("/{alquiler_id}")
def eliminar_alquiler(alquiler_id: int, db: Session = Depends(database.get_db)):
    alquiler = db.query(models.Alquiler).filter(models.Alquiler.id == alquiler_id).first()
    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    db.delete(alquiler)
    db.commit()
    return {"mensaje": "Alquiler eliminado correctamente"}
