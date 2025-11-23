from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database
from ..schemas import cliente as schemas
from backend.services import cliente as cliente_service

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# ============================
# Crear Cliente
# ============================
@router.post("/", response_model=schemas.Cliente)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(database.get_db)):
    return cliente_service.crear_cliente(db, cliente)


# ============================
# Listar Clientes activos
# ============================
@router.get("/", response_model=list[schemas.Cliente])
def listar_clientes(db: Session = Depends(database.get_db)):
    return cliente_service.listar_clientes(db)

# ============================
# Filtrar Clientes
# ============================
@router.get("/filtrar", response_model=list[schemas.Cliente])
def filtrar_clientes(
    nombre: str | None = None,
    dni: str | None = None,
    db: Session = Depends(database.get_db)
):
    return cliente_service.filtrar_clientes(db, nombre, dni)




# ============================
# Obtener Cliente por ID
# ============================
@router.get("/{cliente_id}", response_model=schemas.Cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    return cliente_service.obtener_cliente(db, cliente_id)


# ============================
# Actualizar Cliente
# ============================
@router.put("/{cliente_id}", response_model=schemas.Cliente)
def actualizar_cliente(cliente_id: int, datos: schemas.ClienteCreate, db: Session = Depends(database.get_db)):
    return cliente_service.actualizar_cliente(db, cliente_id, datos)


# ============================
# Borrado Lógico
# ============================
@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    return cliente_service.eliminar_cliente(db, cliente_id)
