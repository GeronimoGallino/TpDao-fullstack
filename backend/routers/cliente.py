from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from ..schemas import cliente as schemas

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# ============================
# Crear Cliente
# ============================
@router.post("/", response_model=schemas.Cliente)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(database.get_db)):
    nuevo_cliente = models.Cliente(**cliente.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


# ============================
# Listar Clientes activos
# ============================
@router.get("/", response_model=list[schemas.Cliente])
def listar_clientes(db: Session = Depends(database.get_db)):
    return db.query(models.Cliente).filter(models.Cliente.estado == True).all()


# ============================
# Obtener Cliente por ID
# ============================
@router.get("/{cliente_id}", response_model=schemas.Cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id_cliente == cliente_id,
        models.Cliente.estado == True
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o eliminado")

    return cliente


# ============================
# Actualizar Cliente
# ============================
@router.put("/{cliente_id}", response_model=schemas.Cliente)
def actualizar_cliente(cliente_id: int, datos: schemas.ClienteCreate, db: Session = Depends(database.get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id_cliente == cliente_id,
        models.Cliente.estado == True
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o eliminado")

    for key, value in datos.model_dump().items():

        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente


# ============================
# Borrado Lógico
# ============================
@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id_cliente == cliente_id,
        models.Cliente.estado == True
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o ya eliminado")

    cliente.estado = False  # 🔥 borrado lógico

    db.commit()

    return {"mensaje": "Cliente eliminado (borrado lógico)"}
