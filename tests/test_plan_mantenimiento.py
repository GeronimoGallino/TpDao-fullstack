import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from datetime import datetime, timedelta

from backend.database import Base, engine, SessionLocal
from backend.models.plan_mantenimiento import PlanMantenimiento


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
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# ----------------------------------------
# HELPERS
# ----------------------------------------

def crear_plan(db, tipo="auto", km_intervalo=10000, meses_intervalo=6):
    plan = PlanMantenimiento(
        tipo_vehiculo=tipo,
        km_intervalo=km_intervalo,
        meses_intervalo=meses_intervalo
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


# ----------------------------------------
# TESTS
# ----------------------------------------

def test_calcular_proximo_mantenimiento(db):
    plan = crear_plan(db, km_intervalo=10000, meses_intervalo=6)

    ultimo_km = 50000
    ultimo_fecha = datetime(2024, 1, 1)

    proximo_km, proxima_fecha = plan.calcular_proximo_mantenimiento(ultimo_km, ultimo_fecha)

    assert proximo_km == 60000               # 50000 + 10000
    assert proxima_fecha.month == 7          # Enero + 6 meses = Julio
    assert proxima_fecha.year == 2024


def test_calcular_alertas_sin_alerta(db):
    plan = crear_plan(db, km_intervalo=10000, meses_intervalo=6)

    kilometraje_actual = 54000
    fecha_actual = datetime(2024, 5, 1)

    ultimo_km = 50000
    ultimo_fecha = datetime(2024, 1, 1)

    alerta_km, alerta_fecha = plan.calcular_alertas(
        kilometraje_actual, fecha_actual, ultimo_km, ultimo_fecha
    )

    assert alerta_km is False
    assert alerta_fecha is False


def test_calcular_alertas_por_km(db):
    plan = crear_plan(db, km_intervalo=10000, meses_intervalo=6)

    kilometraje_actual = 59500  # dentro del aviso 1000 km antes
    fecha_actual = datetime(2024, 4, 1)

    ultimo_km = 50000
    ultimo_fecha = datetime(2024, 1, 1)

    alerta_km, alerta_fecha = plan.calcular_alertas(
        kilometraje_actual, fecha_actual, ultimo_km, ultimo_fecha
    )

    assert alerta_km is True
    assert alerta_fecha is False


def test_calcular_alertas_por_fecha(db):
    plan = crear_plan(db, km_intervalo=10000, meses_intervalo=6)

    kilometraje_actual = 52000
    fecha_actual = datetime(2024, 6, 20)  # mantenimiento desde 1/7 → alerta desde 15/6

    ultimo_km = 50000
    ultimo_fecha = datetime(2024, 1, 1)

    alerta_km, alerta_fecha = plan.calcular_alertas(
        kilometraje_actual, fecha_actual, ultimo_km, ultimo_fecha
    )

    assert alerta_km is False
    assert alerta_fecha is True