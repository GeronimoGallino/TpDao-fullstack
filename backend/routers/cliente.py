from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from ..schemas import cliente as schemas

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=schemas.Cliente)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(database.get_db)):
    nuevo_cliente = models.Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


@router.get("/", response_model=list[schemas.Cliente])
def listar_clientes(db: Session = Depends(database.get_db)):
    # 👇 Solo clientes activos
    return db.query(models.Cliente).filter(models.Cliente.estado == True).all()


@router.get("/{cliente_id}", response_model=schemas.Cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id == cliente_id,
        models.Cliente.estado == True
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o eliminado")

    return cliente


@router.put("/{cliente_id}", response_model=schemas.Cliente)
def actualizar_cliente(cliente_id: int, datos: schemas.ClienteCreate, db: Session = Depends(database.get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id == cliente_id,
        models.Cliente.estado == True
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o eliminado")

    for key, value in datos.dict().items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id == cliente_id,
        models.Cliente.estado == True
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o ya eliminado")

    # 🔥 Borrado lógico
    cliente.estado = False

    db.commit()
    return {"mensaje": "Cliente eliminado (borrado lógico)"}