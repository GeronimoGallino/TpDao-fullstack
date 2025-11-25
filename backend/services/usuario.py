from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend import models, schemas
from ..schemas.usuario import UsuarioCreate, Usuario


# -------------------------------------
# Crear usuario
# -------------------------------------
def crear_usuario(db: Session, usuario: UsuarioCreate):
    # Verificar si ya existe ese email (PK)
    existente = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese email")

    # Verificar si el empleado existe
    empleado = db.query(models.Empleado).filter(
        models.Empleado.id == usuario.id   # ← corregido
    ).first()

    if not empleado:
        raise HTTPException(status_code=400, detail="Empleado asociado no existe")

    nuevo_usuario = models.Usuario(
        email=usuario.email,
        id=usuario.id,  # FK a empleado
        password=usuario.password,
        role=usuario.role
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


# -------------------------------------
# Obtener usuario por email
# -------------------------------------
def obtener_usuario(db: Session, email: str):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == email
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario


# -------------------------------------
# Obtener todos los usuarios
# -------------------------------------
def obtener_todos(db: Session):
    return db.query(models.Usuario).all()
