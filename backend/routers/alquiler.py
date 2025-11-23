
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database
from ..schemas import alquiler as schemas
from ..services import alquiler as alquiler_service
from typing import List

router = APIRouter(prefix="/alquileres", tags=["Alquileres"])

@router.post("/", response_model=schemas.Alquiler)
def crear_alquiler(alquiler: schemas.AlquilerCreate, db: Session = Depends(database.get_db)):
    return alquiler_service.crear_alquiler(alquiler, db)

@router.get("/", response_model=list[schemas.Alquiler])
def listar(db: Session = Depends(database.get_db)):
    return alquiler_service.listar_activos(db)

@router.get("/{alquiler_id}", response_model=schemas.Alquiler)
def obtener(alquiler_id: int, db: Session = Depends(database.get_db)):
    return alquiler_service.obtener_alquiler(alquiler_id, db)

@router.put("/finalizar/{alquiler_id}", response_model=schemas.Alquiler)
def finalizar(alquiler_id: int, datos: schemas.AlquilerFinalizar, db: Session = Depends(database.get_db)):
    return alquiler_service.finalizar_alquiler(alquiler_id, datos, db)

@router.delete("/{alquiler_id}")
def cancelar(alquiler_id: int, db: Session = Depends(database.get_db)):
    return alquiler_service.cancelar_alquiler(alquiler_id, db)

