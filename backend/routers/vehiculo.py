from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database
from ..schemas import vehiculo as schemas
from backend.services import vehiculo as vehiculo_service

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])

@router.post("/", response_model=schemas.Vehiculo)
def crear_vehiculo(vehiculo: schemas.VehiculoCreate, db: Session = Depends(database.get_db)):
    return vehiculo_service.crear_vehiculo(db, vehiculo)


#Lista los vehiculos disponibles para ser alquilados 
@router.get("/activos", response_model=list[schemas.Vehiculo])
def listar_vehiculos(db: Session = Depends(database.get_db)):
    return vehiculo_service.listar_vehiculos(db)


#Lista todos los vehiculos que no esten eliminados (pueden estar no disponibles para ser alquilados)
@router.get("/", response_model=list[schemas.Vehiculo])
def listar_vehiculos(db: Session = Depends(database.get_db)):
    return vehiculo_service.listar_todos_vehiculos(db)

@router.get("/filtrar", response_model=list[schemas.Vehiculo])
def filtrar_vehiculos(
    patente: str | None = None,
    marca: str | None = None,
    modelo: str | None = None,
    db: Session = Depends(database.get_db)
):
    return vehiculo_service.filtrar_vehiculos(db, patente, marca, modelo)

@router.get("/{vehiculo_id}", response_model=schemas.Vehiculo)
def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(database.get_db)):
    return vehiculo_service.obtener_vehiculo(db, vehiculo_id)

@router.put("/{vehiculo_id}", response_model=schemas.Vehiculo)
def actualizar_vehiculo(vehiculo_id: int, datos: schemas.VehiculoCreate, db: Session = Depends(database.get_db)):
    return vehiculo_service.actualizar_vehiculo(db, vehiculo_id, datos)

@router.delete("/{vehiculo_id}")
def eliminar_vehiculo(vehiculo_id: int, db: Session = Depends(database.get_db)):
    return vehiculo_service.eliminar_vehiculo(db, vehiculo_id)


