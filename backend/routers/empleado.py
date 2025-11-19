from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from ..schemas import empleado as schemas

router = APIRouter(prefix="/empleados", tags=["Empleados"])


@router.post("/", response_model=schemas.Empleado)
def crear_empleado(empleado: schemas.EmpleadoCreate, db: Session = Depends(database.get_db)):
    nuevo_empleado = models.Empleado(**empleado.dict())
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
    return nuevo_empleado


@router.get("/", response_model=list[schemas.Empleado])
def listar_empleados(db: Session = Depends(database.get_db)):
    return db.query(models.Empleado).filter(models.Empleado.estado == True).all()


@router.get("/{empleado_id}", response_model=schemas.Empleado)
def obtener_empleado(empleado_id: int, db: Session = Depends(database.get_db)):
    empleado = db.query(models.Empleado).filter(
        models.Empleado.id == empleado_id,
        models.Empleado.estado == True
    ).first()

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado o eliminado")

    return empleado


@router.put("/{empleado_id}", response_model=schemas.Empleado)
def actualizar_empleado(empleado_id: int, datos: schemas.EmpleadoCreate, db: Session = Depends(database.get_db)):
    empleado = db.query(models.Empleado).filter(
        models.Empleado.id == empleado_id,
        models.Empleado.estado == True
    ).first()

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado o eliminado")

    for key, value in datos.dict().items():
        setattr(empleado, key, value)

    db.commit()
    db.refresh(empleado)
    return empleado


@router.delete("/{empleado_id}")
def eliminar_empleado(empleado_id: int, db: Session = Depends(database.get_db)):
    empleado = db.query(models.Empleado).filter(
        models.Empleado.id == empleado_id,
        models.Empleado.estado == True
    ).first()

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado o ya eliminado")

    empleado.estado = False  # 👈 borrado lógico
    db.commit()

    return {"mensaje": "Empleado eliminado (borrado lógico)"}
