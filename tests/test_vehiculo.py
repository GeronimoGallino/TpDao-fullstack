import sys, os
import uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine, SessionLocal
from backend import models
from datetime import datetime

# ----------------------------------------
# FIXTURES
# ----------------------------------------

@pytest.fixture(autouse=True)
def setup_database():
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

def crear_vehiculo_en_bd(db, marca="Ford", modelo="Focus", anio=2020, patente=None):
    if not patente:
        patente = str(uuid.uuid4())[:8]  # Patente corta y única

    vehiculo = models.Vehiculo(
        marca=marca,
        modelo=modelo,
        anio=anio,
        patente=patente,
        tipo="auto",
        kilometraje=10000,
        disponible=True,
        costo_diario=5000,
        estado="activo",
        fecha_registro=datetime.now()
    )

    db.add(vehiculo)
    db.commit()
    db.refresh(vehiculo)
    return vehiculo

# ----------------------------------------
# TESTS
# ----------------------------------------

def test_crear_vehiculo(client):
    data = {
        "marca": "Toyota",
        "modelo": "Corolla",
        "anio": 2022,
        "patente": "XYZ123",
        "tipo": "auto",
        "kilometraje": 5000,
        "disponible": True,
        "costo_diario": 6000,
        "estado": "activo"
    }

    response = client.post("/api/vehiculos/", json=data)
    assert response.status_code == 200

    result = response.json()
    assert result["marca"] == "Toyota"
    assert result["modelo"] == "Corolla"
    assert "id" in result


def test_listar_vehiculos(client, db):
    crear_vehiculo_en_bd(db, "Ford", "Focus", 2020)
    crear_vehiculo_en_bd(db, "Chevrolet", "Onix", 2021)

    response = client.get("/api/vehiculos/")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2
    assert result[0]["disponible"] is True


def test_obtener_vehiculo(client, db):
    vehiculo = crear_vehiculo_en_bd(db)

    response = client.get(f"/api/vehiculos/{vehiculo.id}")
    assert response.status_code == 200

    result = response.json()
    assert result["id"] == vehiculo.id
    assert result["marca"] == vehiculo.marca


def test_obtener_vehiculo_no_existente(client):
    response = client.get("/api/vehiculos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Vehículo no encontrado"


def test_actualizar_vehiculo(client, db):
    vehiculo = crear_vehiculo_en_bd(db)

    new_data = {
        "marca": "Honda",
        "modelo": "Civic",
        "anio": 2021,
        "patente": "ABC987",
        "tipo": "auto",
        "kilometraje": 12000,
        "disponible": True,
        "costo_diario": 7000,
        "estado": "activo"
    }

    response = client.put(f"/api/vehiculos/{vehiculo.id}", json=new_data)
    assert response.status_code == 200

    result = response.json()
    assert result["marca"] == "Honda"
    assert result["modelo"] == "Civic"


def test_eliminar_vehiculo(client, db):
    vehiculo = crear_vehiculo_en_bd(db)

    response = client.delete(f"/api/vehiculos/{vehiculo.id}")
    assert response.status_code == 200

    db.expire_all()
    vehiculo_db = db.query(models.Vehiculo).filter_by(id=vehiculo.id).first()
    assert vehiculo_db.disponible is False


def test_listar_vehiculos_excluye_no_disponibles(client, db):
    v1 = crear_vehiculo_en_bd(db, "Ford", "Focus", 2020)
    v2 = crear_vehiculo_en_bd(db, "Chevrolet", "Onix", 2021)

    v2.disponible = False
    db.commit()

    response = client.get("/api/vehiculos/")
    result = response.json()

    assert len(result) == 1
    assert result[0]["marca"] == "Ford"
