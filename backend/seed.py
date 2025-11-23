from datetime import datetime, timedelta, timezone
from backend.database import Base, engine, SessionLocal
from backend.models.vehiculo import Vehiculo
from backend.models.plan_mantenimiento import PlanMantenimiento
from backend.models.mantenimiento import Mantenimiento
from backend.models.empleado import Empleado

def seed():
    print("Iniciando seed de base de datos...")

    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        empleados = [
            Empleado(
                nombre="Juan Pérez",
                dni=30123456,
                cargo="administrador",
                telefono="1122334455",
                email="juan.perez@empresa.com",
                fecha_inicio=datetime.now(timezone.utc),
                id_negocio=1,
                estado=True
            ),
            Empleado(
                nombre="María Gómez",
                dni=28999888,
                cargo="mecanico",
                telefono="1166778899",
                email="maria.gomez@empresa.com",
                fecha_inicio=datetime.now(timezone.utc),
                id_negocio=1,
                estado=True
            ),
            Empleado(
                nombre="Luis Fernández",
                dni=31555777,
                cargo="mecanico",
                telefono="1144455566",
                email="luis.fernandez@empresa.com",
                fecha_inicio=datetime.now(timezone.utc),
                id_negocio=1,
                estado=True
            )
        ]   

        db.add_all(empleados)
        db.commit()

        # Recargar para obtener los IDs
        for e in empleados:
            db.refresh(e)

        # ---------------------------------------------
        # 1) Crear Planes de Mantenimiento
        # ---------------------------------------------
        plan_auto = PlanMantenimiento(
            tipo_vehiculo="auto",
            km_intervalo=10000,
            meses_intervalo=12
        )

        plan_pickup = PlanMantenimiento(
            tipo_vehiculo="pickup",
            km_intervalo=15000,
            meses_intervalo=10
        )

        plan_moto = PlanMantenimiento(
            tipo_vehiculo="moto",
            km_intervalo=6000,
            meses_intervalo=6
        )

        db.add_all([plan_auto, plan_pickup, plan_moto])
        db.commit()

        # ---------------------------------------------
        # 2) Crear Vehículos
        # ---------------------------------------------
        vehiculos = [
            Vehiculo(
                marca="Toyota",
                modelo="Corolla",
                anio=2020,
                patente="AA123BB",
                tipo="auto",
                kilometraje=45000,
                disponible=True,
                costo_diario=20000,
                plan_mantenimiento_id=plan_auto.id
            ),
            Vehiculo(
                marca="Ford",
                modelo="Ranger",
                anio=2019,
                patente="AD456CD",
                tipo="pickup",
                kilometraje=80000,
                disponible=True,
                costo_diario=30000,
                plan_mantenimiento_id=plan_pickup.id
            ),
            Vehiculo(
                marca="Yamaha",
                modelo="FZ",
                anio=2022,
                patente="A123BCD",
                tipo="moto",
                kilometraje=12000,
                disponible=True,
                costo_diario=10000,
                plan_mantenimiento_id=plan_moto.id
            ),
            Vehiculo(
                marca="Chevrolet",
                modelo="Onix",
                anio=2021,
                patente="AF789GH",
                tipo="auto",
                kilometraje=15000,
                disponible=True,
                costo_diario=18000,
                plan_mantenimiento_id=plan_auto.id
            ),
            Vehiculo(
                marca="Volkswagen",
                modelo="Amarok",
                anio=2018,
                patente="AC345EF",
                tipo="pickup",
                kilometraje=120000,
                disponible=False,
                costo_diario=32000,
                estado="mantenimiento",
                plan_mantenimiento_id=plan_pickup.id
            ),
        ]

        db.add_all(vehiculos)
        db.commit()

        # Recargar con IDs
        db.refresh(vehiculos[0])
        db.refresh(vehiculos[1])
        db.refresh(vehiculos[2])

        # ---------------------------------------------
        # 3) Crear Mantenimientos
        # ---------------------------------------------
        mantenimientos = [
            Mantenimiento(
                id_vehiculo=vehiculos[0].id,
                id_empleado=1,  # este valor debe existir en tu sistema
                fecha=datetime.now(timezone.utc) - timedelta(days=200),
                km_actual=40000,
                tipo="preventivo",
                costo=35000,
                observaciones="Cambio de aceite y filtros"
            ),
            Mantenimiento(
                id_vehiculo=vehiculos[1].id,
                id_empleado=1,
                fecha=datetime.now(timezone.utc) - timedelta(days=400),
                km_actual=75000,
                tipo="correctivo",
                costo=80000,
                observaciones="Cambio de correa de distribución"
            ),
            Mantenimiento(
                id_vehiculo=vehiculos[2].id,
                id_empleado=1,
                fecha=datetime.now(timezone.utc) - timedelta(days=90),
                km_actual=12000,
                tipo="preventivo",
                costo=15000,
                observaciones="Service general moto"
            ),
        ]

        db.add_all(mantenimientos)
        db.commit()

        print("Seed completado exitosamente.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
