import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from datetime import datetime, timedelta

from backend.database import Base, engine, SessionLocal
from backend.models.plan_mantenimiento import PlanMantenimiento


# ----------------------------------------------------------
# FIXTURES
# ----------------------------------------------------------

@pytest.fixture(autouse=True)
def setup_database():
    """Recrea la base antes de cada test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# ----------------------------------------------------------
# Helper para crear plan
# ----------------------------------------------------------

def crear_plan(db, km_intervalo=10000, meses_intervalo=6):
    plan = PlanMantenimiento(
        tipo_vehiculo="auto",
        km_intervalo=km_intervalo,
        meses_intervalo=meses_intervalo,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


# ----------------------------------------------------------
# TESTS
# ----------------------------------------------------------

def test_sumar_meses(db):
    plan = crear_plan(db)

    fecha = datetime(2024, 1, 31)
    nueva_fecha = plan._sumar_meses(fecha, 1)

    assert nueva_fecha == datetime(2024, 2, 29)  # febrero correcto (2024 es bisiesto)


def test_proximo_mantenimiento(db):
    plan = crear_plan(db)

    resultado = plan.calcular_proximo_mantenimiento(
        ultimo_km=50000,
        ultimo_fecha=datetime(2024, 1, 1),
        kilometraje_actual=50000,
        fecha_actual=datetime(2024, 3, 1)
    )

    assert resultado["proximo_km"] == 60000
    assert resultado["proxima_fecha"] == datetime(2024, 7, 1)
    assert resultado["alerta_km"] is False
    assert resultado["alerta_fecha"] is False


def test_alerta_por_km(db):
    plan = crear_plan(db)

    ultimo_km = 50000
    ultimo_fecha = datetime(2024, 1, 1)
    fecha_actual = datetime(2024, 3, 1)

    # Sin alerta todavía
    resultado = plan.calcular_proximo_mantenimiento(
        ultimo_km=ultimo_km,
        ultimo_fecha=ultimo_fecha,
        kilometraje_actual=55000,
        fecha_actual=fecha_actual
    )
    assert resultado["alerta_km"] is False

    # Dentro de los últimos 1000 km → alerta True
    resultado_alerta = plan.calcular_proximo_mantenimiento(
        ultimo_km=ultimo_km,
        ultimo_fecha=ultimo_fecha,
        kilometraje_actual=59500,   # faltan 500 km
        fecha_actual=fecha_actual
    )
    assert resultado_alerta["alerta_km"] is True
    assert resultado_alerta["alerta_fecha"] is False


def test_alerta_por_fecha(db):
    plan = crear_plan(db)

    resultado = plan.calcular_proximo_mantenimiento(
        ultimo_km=50000,
        ultimo_fecha=datetime(2024, 1, 1),
        kilometraje_actual=50000,
        fecha_actual=datetime(2024, 6, 20)   # mantenimiento el 1/7 → alerta desde 15/6
    )

    assert resultado["alerta_km"] is False
    assert resultado["alerta_fecha"] is True


def test_sin_alertas(db):
    plan = crear_plan(db)

    resultado = plan.calcular_proximo_mantenimiento(
        ultimo_km=50000,
        ultimo_fecha=datetime(2024, 1, 1),
        kilometraje_actual=52000,
        fecha_actual=datetime(2024, 5, 1),
    )

    assert resultado["alerta_km"] is False
    assert resultado["alerta_fecha"] is False


def test_alerta_km_y_fecha(db):
    plan = crear_plan(db)

    resultado = plan.calcular_proximo_mantenimiento(
        ultimo_km=50000,
        ultimo_fecha=datetime(2024, 1, 1),
        kilometraje_actual=59500,                     # km alerta
        fecha_actual=datetime(2024, 6, 25),            # fecha alerta
    )

    assert resultado["alerta_km"] is True
    assert resultado["alerta_fecha"] is True
# ----------------------------------------------------------
