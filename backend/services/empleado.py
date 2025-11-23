from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.empleado import Empleado
from backend.schemas.empleado import EmpleadoCreate


# ---------------------------------------------------------
# Crear empleado
# ---------------------------------------------------------
def crear_empleado(db: Session, datos: EmpleadoCreate):
    nuevo_empleado = Empleado(**datos.model_dump())
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
    return nuevo_empleado


# ---------------------------------------------------------
# Listar empleados activos
# ---------------------------------------------------------
def listar_empleados(db: Session):
    return db.query(Empleado).filter(Empleado.estado == True).all()


# ---------------------------------------------------------
# Obtener empleado por ID
# ---------------------------------------------------------
def obtener_empleado(db: Session, empleado_id: int):
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return empleado


# ---------------------------------------------------------
# Actualizar empleado
# ---------------------------------------------------------
def actualizar_empleado(db: Session, empleado_id: int, datos: EmpleadoCreate):
    empleado = obtener_empleado(db, empleado_id)

    if empleado.estado is False:
        raise HTTPException(status_code=404, detail="Empleado eliminado")

    for key, value in datos.model_dump().items():
        setattr(empleado, key, value)

    db.commit()
    db.refresh(empleado)
    return empleado


# ---------------------------------------------------------
# Borrado lógico (estado = False)
# ---------------------------------------------------------
def eliminar_empleado(db: Session, empleado_id: int):
    empleado = obtener_empleado(db, empleado_id)

    if empleado.estado is False:
        raise HTTPException(status_code=404, detail="Empleado ya eliminado")

    empleado.estado = False
    db.commit()

    return {"mensaje": "Empleado eliminado (borrado lógico)"}

# ---------------------------------------------------------
# Filtrar empleados por nombre, dni o cargo
# ---------------------------------------------------------
def filtrar_empleados(db: Session, nombre: str | None, dni: int | None, cargo: str | None):

    query = db.query(Empleado).filter(Empleado.estado == True)

    if nombre:
        query = query.filter(Empleado.nombre.ilike(f"%{nombre}%"))

    if dni:
        query = query.filter(Empleado.dni == dni)

    if cargo:
        query = query.filter(Empleado.cargo.ilike(f"%{cargo}%"))

    return query.all()
    return query.all()