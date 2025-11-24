import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from datetime import datetime, timedelta, timezone

from backend.database import Base, engine, SessionLocal
from backend.models.mantenimiento import Mantenimiento
from backend.models.vehiculo import Vehiculo
from backend.models.empleado import Empleado


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
# Helper para crear mantenimiento
# ----------------------------------------------------------



def crear_mantenimiento(
        db,
        km_actual=50000,
        fecha=datetime(2024, 1, 1, tzinfo=timezone.utc),
        km_prox_mant=10000,
        meses_prox_mant=6
    ):
    # Crear relaciones mínimas
    v = Vehiculo(
        marca="Toyota",
                modelo="Corolla",
                anio=2020,
                patente="AA123BB",
                tipo="auto",
                kilometraje=45000,
                disponible=True,
                costo_diario=20000
    )
    e = Empleado(nombre="Juan Pérez",
                dni=30123456,
                cargo="administrador",
                telefono="1122334455",
                email="juan.perez@empresa.com",
                fecha_inicio=datetime.now(timezone.utc),
                id_negocio=1,
                estado=True)

    db.add(v)
    db.add(e)
    db.commit()

    m = Mantenimiento(
        id_vehiculo=v.id,
        id_empleado=e.id,
        km_actual=km_actual,
        fecha=fecha,
        tipo="preventivo",
        costo=1000,
        km_prox_mant=km_prox_mant,
        meses_prox_mant=meses_prox_mant
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


# ----------------------------------------------------------
# TESTS
# ----------------------------------------------------------

def test_sumar_meses(db):
    m = crear_mantenimiento(db)

    fecha = datetime(2024, 1, 31, tzinfo=timezone.utc)
    nueva_fecha = m._sumar_meses(fecha, 1)

    # Febrero de 2024 → 29 días (bisiesto)
    assert nueva_fecha == datetime(2024, 2, 29, tzinfo=timezone.utc)


def test_proximo_mantenimiento(db):
    m = crear_mantenimiento(
        db,
        km_actual=50000,
        fecha=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

    resultado = m.calcular_proximo_mantenimiento(
        kilometraje_actual=50000,
        fecha_actual=datetime(2024, 3, 1, tzinfo=timezone.utc)
    )

    assert resultado["proximo_km"] == 60000
    assert resultado["proxima_fecha"] == datetime(2024, 7, 1)
    assert resultado["alerta_km"] is False
    assert resultado["alerta_fecha"] is False


def test_alerta_por_km(db):
    m = crear_mantenimiento(
        db,
        km_actual=50000,
        fecha=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

    fecha_actual = datetime(2024, 3, 1, tzinfo=timezone.utc)

    # No debería haber alerta (faltan 5000 km)
    res = m.calcular_proximo_mantenimiento(
        kilometraje_actual=55000,
        fecha_actual=fecha_actual
    )
    assert res["alerta_km"] is False

    # Dentro del rango de 1000 km → alerta True
    res_alerta = m.calcular_proximo_mantenimiento(
        kilometraje_actual=59500,
        fecha_actual=fecha_actual
    )
    assert res_alerta["alerta_km"] is True
    assert res_alerta["alerta_fecha"] is False


def test_alerta_por_fecha(db):
    m = crear_mantenimiento(
        db,
        km_actual=50000,
        fecha=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

    # Próximo mantenimiento: 1/7/2024 → alerta desde 16/6
    resultado = m.calcular_proximo_mantenimiento(
        kilometraje_actual=50000,
        fecha_actual=datetime(2024, 6, 20, tzinfo=timezone.utc)
    )

    assert resultado["alerta_km"] is False
    assert resultado["alerta_fecha"] is True


def test_sin_alertas(db):
    m = crear_mantenimiento(
        db,
        km_actual=50000,
        fecha=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

    res = m.calcular_proximo_mantenimiento(
        kilometraje_actual=52000,
        fecha_actual=datetime(2024, 5, 1, tzinfo=timezone.utc)
    )

    assert res["alerta_km"] is False
    assert res["alerta_fecha"] is False


def test_alerta_km_y_fecha(db):
    m = crear_mantenimiento(
        db,
        km_actual=50000,
        fecha=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

    res = m.calcular_proximo_mantenimiento(
        kilometraje_actual=59500,
        fecha_actual=datetime(2024, 6, 25, tzinfo=timezone.utc)  # fecha y km en alerta
    )

    assert res["alerta_km"] is True
    assert res["alerta_fecha"] is True