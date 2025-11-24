
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.vehiculo import Vehiculo
from backend.schemas.vehiculo import VehiculoCreate


# ---------------------------------------------------------
# Crear vehículo
# ---------------------------------------------------------
def crear_vehiculo(db: Session, datos: VehiculoCreate):
    nuevo_vehiculo = Vehiculo(**datos.model_dump())
    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)
    return nuevo_vehiculo


# ---------------------------------------------------------
# Listar vehículos (solo disponibles)
# ---------------------------------------------------------
def listar_vehiculos(db: Session):
    return db.query(Vehiculo).filter(Vehiculo.disponible == True).all()


# ---------------------------------------------------------
# Listar vehículos que no estén eliminados (pueden estar no disponibles)
# ---------------------------------------------------------
def listar_todos_vehiculos(db: Session):
    return db.query(Vehiculo).filter(Vehiculo.estado == "activo").all()


# ---------------------------------------------------------
# Obtener vehículo por ID
# ---------------------------------------------------------
def obtener_vehiculo(db: Session, vehiculo_id: int):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()

    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    return vehiculo


# ---------------------------------------------------------
# Actualizar vehículo
# ---------------------------------------------------------
def actualizar_vehiculo(db: Session, vehiculo_id: int, datos: VehiculoCreate):
    vehiculo = obtener_vehiculo(db, vehiculo_id)

    # Actualizar atributos
    for key, value in datos.model_dump().items():
        setattr(vehiculo, key, value)

    db.commit()
    db.refresh(vehiculo)
    return vehiculo


# ---------------------------------------------------------
# Borrado lógico (vehiculo.disponible = False)
# ---------------------------------------------------------
def eliminar_vehiculo(db: Session, vehiculo_id: int):
    vehiculo = obtener_vehiculo(db, vehiculo_id)

    vehiculo.estado = "inactivo"
    db.commit()
    return {"mensaje": "Vehículo eliminado correctamente"}


# ---------------------------------------------------------
# Filtrar vehículos por patente, marca o modelo
# ---------------------------------------------------------
def filtrar_vehiculos(
    db: Session,
    patente: str | None = None,
    marca: str | None = None,
    modelo: str | None = None
):
    query = db.query(Vehiculo)

    if patente:
        query = query.filter(Vehiculo.patente.ilike(f"%{patente}%"))

    if marca:
        query = query.filter(Vehiculo.marca.ilike(f"%{marca}%"))

    if modelo:
        query = query.filter(Vehiculo.modelo.ilike(f"%{modelo}%"))

    return query.all()


# GET /vehiculos/filtrar?patente=AB123
# GET /vehiculos/filtrar?modelo=Corolla
# GET /vehiculos/filtrar?marca=Toyota
# GET /vehiculos/filtrar?marca=Ford&modelo=Fiesta BUSQUEDA MULTIPLE
