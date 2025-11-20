import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine, SessionLocal
from backend import models
import uuid
from datetime import datetime
# ----------------------------------------
# FIXTURES
# ----------------------------------------

@pytest.fixture(autouse=True)
def setup_database():
    """Recrea la base antes de cada test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# ----------------------------------------
# HELPERS
# ----------------------------------------

import uuid
from datetime import datetime
from backend import models

def crear_cliente_en_bd(db, nombre="Juan", apellido="Perez"):
    dni_unico = str(uuid.uuid4())[:8]  # DNI único para cada cliente

    cliente = models.Cliente(
        nombre=nombre,
        apellido=apellido,
        dni=dni_unico,
        telefono="123456789",
        email="test@test.com",
        direccion="Calle falsa 123",
        fecha_registro=datetime.now(),
        estado=True
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

# ----------------------------------------
# TESTS
# ----------------------------------------

def test_crear_cliente(client):
    data = {
        "nombre": "Juan",
        "apellido": "Perez",
        "dni": "12345678",
        "email": "juan@test.com",
        "telefono": "123456789",
        "estado": True
    }

    response = client.post("/api/clientes/", json=data)
    assert response.status_code == 200

    result = response.json()
    assert result["nombre"] == "Juan"
    assert result["apellido"] == "Perez"
    assert "id_cliente" in result


def test_listar_clientes(client, db):
    crear_cliente_en_bd(db, "Ana", "Lopez")
    crear_cliente_en_bd(db, "Luis", "Gomez")

    response = client.get("/api/clientes/")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2
    assert result[0]["estado"] is True


def test_obtener_cliente(client, db):
    cliente = crear_cliente_en_bd(db)

    response = client.get(f"/api/clientes/{cliente.id_cliente}")
    assert response.status_code == 200

    result = response.json()
    assert result["id_cliente"] == cliente.id_cliente
    assert result["nombre"] == cliente.nombre


def test_obtener_cliente_no_existente(client):
    response = client.get("/api/clientes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado o eliminado"


def test_actualizar_cliente(client, db):
    cliente = crear_cliente_en_bd(db)

    new_data = {
        "nombre": "Carlos",
        "apellido": "Martinez",
        "dni": "87654321",
        "email": "nuevo@test.com",
        "telefono": "111222333",
        "estado": True
    }

    response = client.put(f"/api/clientes/{cliente.id_cliente}", json=new_data)
    assert response.status_code == 200

    result = response.json()
    assert result["nombre"] == "Carlos"
    assert result["apellido"] == "Martinez"


def test_eliminar_cliente(client, db):
    cliente = crear_cliente_en_bd(db)

    # Ejecutar DELETE
    response = client.delete(f"/api/clientes/{cliente.id_cliente}")
    assert response.status_code == 200

    # Refrescar sesión para ver cambios hechos por otras sesiones
    db.expire_all()

    cliente_db = db.query(models.Cliente).filter_by(id_cliente=cliente.id_cliente).first()
    assert cliente_db.estado is False



def test_listar_clientes_excluye_eliminados(client, db):
    c1 = crear_cliente_en_bd(db, "Ana", "Lopez")
    c2 = crear_cliente_en_bd(db, "Pedro", "Garcia")

    c2.estado = False
    db.commit()

    response = client.get("/api/clientes/")
    result = response.json()

    assert len(result) == 1
    assert result[0]["nombre"] == "Ana"
