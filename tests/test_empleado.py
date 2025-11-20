import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine, SessionLocal
from backend import models
from datetime import datetime, timezone
import uuid
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

def crear_empleado_en_bd(db, nombre="Juan", dni=None, cargo="Administrador", id_negocio=1):
    if dni is None:
        dni = int(str(uuid.uuid4().int)[:8])  # genera DNI único

    empleado = models.Empleado(
        nombre=nombre,
        dni=dni,
        cargo=cargo,
        telefono="123456789",
        email=f"{nombre.lower()}@test.com",
        fecha_inicio=datetime.now(timezone.utc),
        id_negocio=id_negocio,
        estado=True
    )
    db.add(empleado)
    db.commit()
    db.refresh(empleado)
    return empleado

# ----------------------------------------
# TESTS
# ----------------------------------------

def test_crear_empleado(client):
    data = {
        "nombre": "Juan",
        "dni": 12345678,
        "cargo": "Administrador",
        "telefono": "123456789",
        "email": "juan@empresa.com",
        "fecha_inicio": "2025-11-20T14:30:00Z",
        "id_negocio": 1,
        "estado": True
    }

    response = client.post("/api/empleados/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["nombre"] == "Juan"
    assert result["cargo"] == "Administrador"
    assert "id" in result


def test_listar_empleados(client, db):
    crear_empleado_en_bd(db, "Ana", 11111111, "Vendedor")
    crear_empleado_en_bd(db, "Luis", 22222222, "Contador")

    response = client.get("/api/empleados/")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0]["estado"] is True


def test_obtener_empleado(client, db):
    empleado = crear_empleado_en_bd(db)

    response = client.get(f"/api/empleados/{empleado.id}")
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == empleado.id
    assert result["nombre"] == empleado.nombre


def test_obtener_empleado_no_existente(client):
    response = client.get("/api/empleados/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Empleado no encontrado o eliminado"


def test_actualizar_empleado(client, db):
    empleado = crear_empleado_en_bd(db)

    new_data = {
        "nombre": "Carlos",
        "dni": 87654321,
        "cargo": "Gerente",
        "telefono": "111222333",
        "email": "nuevo@empresa.com",
        "fecha_inicio": "2025-11-20T14:30:00Z",
        "id_negocio": 1,
        "estado": True
    }

    response = client.put(f"/api/empleados/{empleado.id}", json=new_data)
    assert response.status_code == 200
    result = response.json()
    assert result["nombre"] == "Carlos"
    assert result["cargo"] == "Gerente"


def test_eliminar_empleado(client, db):
    empleado = crear_empleado_en_bd(db)

    response = client.delete(f"/api/empleados/{empleado.id}")
    assert response.status_code == 200

    db.expire_all()
    empleado_db = db.query(models.Empleado).filter_by(id=empleado.id).first()
    assert empleado_db.estado is False


def test_listar_empleados_excluye_eliminados(client, db):
    e1 = crear_empleado_en_bd(db, "Ana", 11111111)
    e2 = crear_empleado_en_bd(db, "Pedro", 22222222)

    e2.estado = False
    db.commit()

    response = client.get("/api/empleados/")
    result = response.json()
    assert len(result) == 1
    assert result[0]["nombre"] == "Ana"
