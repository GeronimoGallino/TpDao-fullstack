from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.mantenimiento import Mantenimiento
from ..schemas.mantenimiento import MantenimientoCreate


def crear_mantenimiento(db: Session, data: MantenimientoCreate) -> Mantenimiento:
    nuevo = Mantenimiento(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_mantenimientos(db: Session) -> list[Mantenimiento]:
    return db.query(Mantenimiento).all()


def obtener_mantenimiento(db: Session, mantenimiento_id: int) -> Mantenimiento:
    mantenimiento = db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return mantenimiento


def actualizar_mantenimiento(db: Session, mantenimiento_id: int, data: MantenimientoCreate) -> Mantenimiento:
    mantenimiento = obtener_mantenimiento(db, mantenimiento_id)

    for key, value in data.model_dump().items():
        setattr(mantenimiento, key, value)

    db.commit()
    db.refresh(mantenimiento)
    return mantenimiento


def eliminar_mantenimiento(db: Session, mantenimiento_id: int) -> None:
    mantenimiento = obtener_mantenimiento(db, mantenimiento_id)

    db.delete(mantenimiento)
    db.commit()