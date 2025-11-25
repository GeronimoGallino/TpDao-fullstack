from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database
from backend.schemas import multa as schemas
from backend.services import multa as multa_service

router = APIRouter(prefix="/multas", tags=["Multas"])


# ============================
# Crear Multa
# ============================
@router.post("/", response_model=schemas.Multa)
def crear_multa(multa: schemas.MultaCreate, db: Session = Depends(database.get_db)):
    return multa_service.crear_multa(db, multa)

# ============================
# Obtener todas las multas
# ============================
@router.get("/", response_model=list[schemas.Multa])
def obtener_todas_las_multas(db: Session = Depends(database.get_db)):
    return multa_service.obtener_todas_las_multas(db)

# ============================
# Obtener multa por ID
# ============================
@router.get("/{multa_id}", response_model=schemas.Multa)
def obtener_multa(multa_id: int, db: Session = Depends(database.get_db)):
    return multa_service.obtener_multa(db, multa_id)


# ============================
# Modificar Multa
# ============================
@router.put("/{multa_id}", response_model=schemas.Multa)
def actualizar_multa(
    multa_id: int,
    datos: schemas.MultaUpdate,
    db: Session = Depends(database.get_db)
):
    return multa_service.actualizar_multa(db, multa_id, datos)


# ============================
# Eliminar Multa
# ============================
@router.delete("/{multa_id}")
def eliminar_multa(multa_id: int, db: Session = Depends(database.get_db)):
    return multa_service.eliminar_multa(db, multa_id)
