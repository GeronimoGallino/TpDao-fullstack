from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.multa import Multa
from backend.models.alquiler import Alquiler
from backend.schemas.multa import MultaCreate, MultaUpdate


# ---------------------------------------------------------
# Crear multa
# ---------------------------------------------------------
def crear_multa(db: Session, datos: MultaCreate):
    # Verificar que el alquiler exista y esté activo
    alquiler = db.query(Alquiler).filter(Alquiler.id == datos.id_alquiler).first()
    print(alquiler.id, alquiler.estado, 'el alquiler')
    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    if alquiler.estado != "Activo":
        raise HTTPException(
            status_code=400,
            detail="No se puede crear una multa porque el alquiler no está activo"
        )

    nueva_multa = Multa(**datos.model_dump())
    db.add(nueva_multa)
    db.commit()
    db.refresh(nueva_multa)
    return nueva_multa


# ---------------------------------------------------------
# Obtener todas las multas
# ---------------------------------------------------------
def obtener_todas_las_multas(db: Session):
    multas = db.query(Multa).all()
    return multas


# ---------------------------------------------------------
# Obtener Multa por ID
# ---------------------------------------------------------
def obtener_multa(db: Session, multa_id: int):
    multa = db.query(Multa).filter(Multa.id_multa == multa_id).first()

    if not multa:
        raise HTTPException(status_code=404, detail="Multa no encontrada")

    return multa


# ---------------------------------------------------------
# Actualizar Multa
# ---------------------------------------------------------
def actualizar_multa(db: Session, multa_id: int, datos: MultaUpdate):
    multa = obtener_multa(db, multa_id)

    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(multa, key, value)

    db.commit()
    db.refresh(multa)
    return multa


# ---------------------------------------------------------
# Eliminar Multa (borrado físico)
# ---------------------------------------------------------
def eliminar_multa(db: Session, multa_id: int):
    multa = obtener_multa(db, multa_id)

    db.delete(multa)
    db.commit()

    return {"mensaje": "Multa eliminada exitosamente"}
