from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import database
from backend.schemas import empleado as schemas
from backend.services import empleado as empleado_service

router = APIRouter(prefix="/empleados", tags=["Empleados"])


@router.post("/", response_model=schemas.Empleado)
def crear_empleado(empleado: schemas.EmpleadoCreate, db: Session = Depends(database.get_db)):
    return empleado_service.crear_empleado(db, empleado)


@router.get("/", response_model=list[schemas.Empleado])
def listar_empleados(db: Session = Depends(database.get_db)):
    return empleado_service.listar_empleados(db)

@router.get("/filtrar", response_model=list[schemas.Empleado])
def filtrar_empleados(
    nombre: str | None = None,
    dni: int | None = None,
    cargo: str | None = None,
    db: Session = Depends(database.get_db)
):
    return empleado_service.filtrar_empleados(db, nombre, dni, cargo)


@router.get("/{empleado_id}", response_model=schemas.Empleado)
def obtener_empleado(empleado_id: int, db: Session = Depends(database.get_db)):
    return empleado_service.obtener_empleado(db, empleado_id)


@router.put("/{empleado_id}", response_model=schemas.Empleado)
def actualizar_empleado(
    empleado_id: int,
    datos: schemas.EmpleadoCreate,
    db: Session = Depends(database.get_db),
):
    return empleado_service.actualizar_empleado(db, empleado_id, datos)


@router.delete("/{empleado_id}")
def eliminar_empleado(empleado_id: int, db: Session = Depends(database.get_db)):
    return empleado_service.eliminar_empleado(db, empleado_id)
