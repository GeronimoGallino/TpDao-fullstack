import sys, os
import uuid
import random
import string
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from backend.main import app
from backend.database import Base, engine, SessionLocal
from backend import models
from backend.models.vehiculo import Vehiculo
from backend.models.plan_mantenimiento import PlanMantenimiento
from backend.models.mantenimiento import Mantenimiento


# ----------------------------------------------------------
# FIXTURES
# ----------------------------------------------------------

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


# ----------------------------------------------------------
# HELPERS
# ----------------------------------------------------------

def generar_patente_valida(formato='viejo'):
    """Genera una patente aleatoria que cumple con el formato regex (ej: ABC123)."""
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=3))
    
    # Usaremos el formato viejo ABC123 para simplicidad en los tests
    return f"{letras}{numeros}"

def crear_vehiculo_en_bd(db, marca="Ford", modelo="Focus", anio=2020, patente=None, **overrides):
    """
    Helper seguro para tests:
    - acepta overrides (kilometraje, costo_diario, tipo, etc.)
    - hace rollback si hay error (validación, unique, FK)
    - devuelve la instancia refrescada
    """
    if not patente:
        patente = generar_patente_valida() 

    data = {
        "marca": marca,
        "modelo": modelo,
        "anio": anio,
        "patente": patente,
        "tipo": "auto",
        "kilometraje": 10000,
        "disponible": True,
        "costo_diario": 5000,
        "estado": "activo",
        "fecha_registro": datetime.now(timezone.utc)
    }

    # aplicar overrides (por ejemplo kilometraje=50000)
    data.update(overrides)

    vehiculo = Vehiculo(**data)

    try:
        db.add(vehiculo)
        db.commit()
        db.refresh(vehiculo)
        return vehiculo
    except IntegrityError as ie:
        db.rollback()
        # Mensaje útil para debugging en tests
        raise AssertionError(f"Error de integridad al crear Vehiculo: {ie.orig}") from ie
    except ValueError as ve:
        db.rollback()
        # Validaciones con @validates u otros
        raise AssertionError(f"Validación al crear Vehiculo falló: {ve}") from ve
    except Exception as e:
        db.rollback()
        raise


def crear_plan(
    db,
    tipo_vehiculo="auto",
    km_intervalo=10000,
    meses_intervalo=6,
    **extra
    ):
    """
    Crea un PlanMantenimiento válido según el modelo real.
    Permite argumentos opcionales extra para flexibilidad en tests.
    """

    data = {
        "tipo_vehiculo": tipo_vehiculo,
        "km_intervalo": km_intervalo,
        "meses_intervalo": meses_intervalo,
    }

    # Permite sobreescribir campos o agregar nuevos
    data.update(extra)

    plan = PlanMantenimiento(**data)

    try:
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    except IntegrityError as ie:
        db.rollback()
        raise AssertionError(f"Error al crear PlanMantenimiento: {ie.orig}")

    except Exception:
        db.rollback()
        raise


from sqlalchemy.exc import IntegrityError

def crear_mantenimiento(db, vehiculo, fecha, km_actual, tipo="preventivo", costo=0, observaciones=None, empleado_id=1):
    """
    Crea un mantenimiento válido según el modelo real.
    """

    data = {
        "id_vehiculo": vehiculo.id,
        "id_empleado": empleado_id,
        "fecha": fecha,
        "km_actual": km_actual,
        "tipo": tipo,
        "costo": costo,
        "observaciones": observaciones
    }

    mant = Mantenimiento(**data)

    try:
        db.add(mant)
        db.commit()
        db.refresh(mant)
        return mant

    except IntegrityError as e:
        db.rollback()
        raise AssertionError(f"Error al crear mantenimiento: {e.orig}")

    except Exception:
        db.rollback()
        raise


# ----------------------------------------------------------
# TESTS API (tus tests)
# ----------------------------------------------------------

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


# ----------------------------------------------------------
# TESTS DE LÓGICA INTERNA (mis tests)
# ----------------------------------------------------------

def test_registrar_mantenimiento(db):
    veh = crear_vehiculo_en_bd(db)
    fecha = datetime(2024, 1, 1, tzinfo=timezone.utc)

    mant = crear_mantenimiento(db, veh, fecha, 50000)
    #veh.registrar_mantenimiento(mant)
    print("Mantenimiento creado:", mant)

    assert len(veh.mantenimientos) == 1
    assert veh.mantenimientos[0].km_actual == 50000


def test_historial_mantenimientos(db):
    veh = crear_vehiculo_en_bd(db)
    m1 = crear_mantenimiento(db, veh, datetime(2024, 1, 1, tzinfo=timezone.utc), 50000)
    m2 = crear_mantenimiento(db, veh, datetime(2024, 6, 1, tzinfo=timezone.utc), 60000)

    historial = veh.obtener_historial_mantenimientos()

    assert len(historial) == 2
    assert historial[0].id == m1.id
    assert historial[1].id == m2.id


def test_asignar_plan_mantenimiento(db):
    veh = crear_vehiculo_en_bd(db)
    plan = crear_plan(db)
    veh.asignar_plan_mantenimiento(plan)
    db.commit()

    assert veh.plan_mantenimiento_id == plan.id


def test_consultar_proximo_mantenimiento_sin_plan(db):
    veh = crear_vehiculo_en_bd(db)
    with pytest.raises(ValueError):
        veh.consultar_proximo_mantenimiento()


def test_consultar_proximo_mantenimiento(db):
    veh = crear_vehiculo_en_bd(db, kilometraje=50000)
    plan = crear_plan(db)
    veh.asignar_plan_mantenimiento(plan)
    db.commit()

    fecha_mant = datetime(2024, 1, 1, tzinfo=timezone.utc)
    crear_mantenimiento(db, veh, fecha_mant, 50000)

    resultado = veh.consultar_proximo_mantenimiento()

    assert resultado["proximo_km"] == 60000
    assert resultado["proxima_fecha"].month == 7  # 6 meses después
    assert "alerta_km" in resultado
    assert "alerta_fecha" in resultado


def test_alertas_desde_vehiculo(db):
    veh = crear_vehiculo_en_bd(db, kilometraje=59500)
    plan = crear_plan(db)

    veh.asignar_plan_mantenimiento(plan)
    db.commit()

    crear_mantenimiento(
        db,
        veh,
        fecha=datetime(2024, 1, 1, tzinfo=timezone.utc),
        km_actual=50000
    )

    resultado = veh.consultar_proximo_mantenimiento()

    assert resultado["alerta_km"] is True