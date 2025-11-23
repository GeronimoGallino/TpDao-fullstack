from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.cliente import Cliente
from backend.schemas.cliente import ClienteCreate


# ---------------------------------------------------------
# Crear cliente
# ---------------------------------------------------------
def crear_cliente(db: Session, datos: ClienteCreate):
    nuevo_cliente = Cliente(**datos.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


# ---------------------------------------------------------
# Listar clientes (solo activos)
# ---------------------------------------------------------
def listar_clientes(db: Session):
    return db.query(Cliente).filter(Cliente.estado == True).all()


# ---------------------------------------------------------
# Obtener cliente por ID
# ---------------------------------------------------------
def obtener_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(
        Cliente.id_cliente == cliente_id,
        Cliente.estado == True
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o eliminado")

    return cliente


# ---------------------------------------------------------
# Actualizar cliente
# ---------------------------------------------------------
def actualizar_cliente(db: Session, cliente_id: int, datos: ClienteCreate):
    cliente = obtener_cliente(db, cliente_id)

    for key, value in datos.model_dump().items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente


# ---------------------------------------------------------
# Borrado lógico (cliente.estado = False)
# ---------------------------------------------------------
def eliminar_cliente(db: Session, cliente_id: int):
    cliente = obtener_cliente(db, cliente_id)

    cliente.estado = False
    db.commit()

    return {"mensaje": "Cliente eliminado (borrado lógico)"}


# ---------------------------------------------------------
# Filtrar clientes por nombre, apellido o DNI
# ---------------------------------------------------------
def filtrar_clientes(db: Session, nombre: str | None, dni: str | None):

    query = db.query(Cliente).filter(Cliente.estado == True)

    if nombre:
        query = query.filter(Cliente.nombre.ilike(f"%{nombre}%"))

    if dni:
        query = query.filter(Cliente.dni == dni)

    return query.all()
