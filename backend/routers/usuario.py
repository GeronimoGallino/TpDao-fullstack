from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import database, schemas
from backend.services import usuario as usuario_service
from ..schemas.usuario import UsuarioCreate, Usuario

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# -------------------------------------
# Crear usuario
# -------------------------------------
@router.post("/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(database.get_db)):
    return usuario_service.crear_usuario(db, usuario)


# -------------------------------------
# Obtener usuario por email
# -------------------------------------
@router.get("/{email}", response_model=Usuario)
def obtener_usuario(email: str, db: Session = Depends(database.get_db)):
    return usuario_service.obtener_usuario(db, email)


# -------------------------------------
# Obtener todos los usuarios
# -------------------------------------
@router.get("/", response_model=list[Usuario])
def obtener_todos(db: Session = Depends(database.get_db)):
    return usuario_service.obtener_todos(db)
