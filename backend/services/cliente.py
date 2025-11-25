from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.cliente import Cliente
from backend.schemas.cliente import ClienteCreate


# ---------------------------------------------------------
# Crear cliente
# ---------------------------------------------------------
def crear_cliente(db: Session, datos: ClienteCreate):
    # 1️⃣ Validar que no exista otro cliente con el mismo DNI
    existing = db.query(Cliente).filter(Cliente.dni == datos.dni).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Ya existe un cliente con DNI {datos.dni}")

    # 2️⃣ Crear cliente
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
# ---------------------------------------------------------
# Actualizar cliente con validación de DNI único
# ---------------------------------------------------------
def actualizar_cliente(db: Session, cliente_id: int, datos: ClienteCreate):
    cliente = obtener_cliente(db, cliente_id)

    # Validar que el nuevo DNI no exista en otro cliente
    if datos.dni:
        dni_existente = (
            db.query(Cliente)
            .filter(Cliente.dni == datos.dni, Cliente.id_cliente != cliente_id)
            .first()
        )
        if dni_existente:
            raise HTTPException(status_code=400, detail=f"Ya existe otro cliente con DNI {datos.dni}")

    # Actualizar los campos
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
