from datetime import datetime, timedelta, timezone
from backend.database import Base, engine, SessionLocal
from backend.models.empleado import Empleado
from backend.models.vehiculo import Vehiculo
from backend.models.cliente import Cliente
from backend.models.alquiler import Alquiler
from backend.models.mantenimiento import Mantenimiento
from backend.models.multa import Multa

def seed():
    print("Iniciando seed de base de datos...")

    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        seed_empleados(db)
        seed_vehiculos(db)
        seed_clientes(db)
        seed_alquileres(db)
        seed_mantenimientos(db)
        seed_multas(db)

        print("✅ Seed completado exitosamente.")

    finally:
        db.close()


def seed_empleados(db):
    # ============================
    # 👥 Empleados de prueba
    # ============================
    empleados = [
        Empleado(
            nombre="Laura Fernández",
            dni=30111222,
            cargo="Administrador",
            telefono="351-5551111",
            email="laura.fernandez@empresa.com",
            id_negocio=1,
            fecha_inicio=datetime(2020, 1, 15, tzinfo=timezone.utc),
            estado=True
        ),
        Empleado(
            nombre="Martín González",
            dni=29222333,
            cargo="Técnico",
            telefono="351-5552222",
            email="martin.gonzalez@empresa.com",
            id_negocio=1,
            fecha_inicio=datetime(2021, 6, 10, tzinfo=timezone.utc),
            estado=True
        ),
        Empleado(
            nombre="Sofía Ramírez",
            dni=28333444,
            cargo="Recepcionista",
            telefono="351-5553333",
            email="sofia.ramirez@empresa.com",
            id_negocio=1,
            fecha_inicio=datetime(2022, 3, 5, tzinfo=timezone.utc),
            estado=True
        ),
        Empleado(
            nombre="Diego Torres",
            dni=27444555,
            cargo="Recepcionista",
            telefono="351-5554444",
            email="diego.torres@empresa.com",
            id_negocio=1,
            fecha_inicio=datetime(2023, 8, 20, tzinfo=timezone.utc),
            estado=True
        ),
        Empleado(
            nombre="Carla Méndez",
            dni=26555666,
            cargo="Recepcionista",
            telefono="351-5555555",
            email="carla.mendez@empresa.com",
            id_negocio=1,
            fecha_inicio=datetime(2024, 2, 12, tzinfo=timezone.utc),
            estado=True
        ),
    ]

    db.add_all(empleados)
    db.commit()

    # Recargar para obtener los IDs
    for e in empleados:
        db.refresh(e)

    print("✅ Empleados cargados exitosamente.")
    return empleados

def seed_vehiculos(db):
    # ============================
    # 🚗 Vehículos de prueba
    # ============================
    vehiculos = [
        Vehiculo(
            marca="Toyota",
            modelo="Corolla",
            anio=2020,
            patente="AB123CD",
            tipo="auto",
            kilometraje=45000,
            disponible=True,
            costo_diario=12000,
            estado="Activo",
            fecha_registro=datetime(2020, 5, 10, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Ford",
            modelo="Ranger",
            anio=2019,
            patente="XYZ789",
            tipo="auto",
            kilometraje=80000,
            disponible=True,
            costo_diario=18000,
            estado="Activo",
            fecha_registro=datetime(2019, 8, 20, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Chevrolet",
            modelo="Captiva",
            anio=2022,
            patente="LMN456",
            tipo="suv",
            kilometraje=25000,
            disponible=True,
            costo_diario=16000,
            estado="Activo",
            fecha_registro=datetime(2022, 7, 1, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Mercedes-Benz",
            modelo="Sprinter",
            anio=2018,
            patente="DEF234",
            tipo="van",
            kilometraje=120000,
            disponible=True, 
            costo_diario=20000,
            estado="Activo",
            fecha_registro=datetime(2018, 11, 30, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Volkswagen",
            modelo="Golf",
            anio=2017,
            patente="AA123BB",
            tipo="auto",
            kilometraje=95000,
            disponible=True,
            costo_diario=11000,
            estado="Activo",
            fecha_registro=datetime(2017, 4, 12, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Renault",
            modelo="Clio",
            anio=2018,
            patente="AC234DE",
            tipo="auto",
            kilometraje=60000,
            disponible=True,
            costo_diario=9500,
            estado="Activo",
            fecha_registro=datetime(2018, 6, 20, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Peugeot",
            modelo="208",
            anio=2020,
            patente="AE345FG",
            tipo="auto",
            kilometraje=30000,
            disponible=True,
            costo_diario=12500,
            estado="Activo",
            fecha_registro=datetime(2020, 9, 5, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Fiat",
            modelo="Cronos",
            anio=2021,
            patente="AF456GH",
            tipo="auto",
            kilometraje=20000,
            disponible=True,
            costo_diario=13000,
            estado="Activo",
            fecha_registro=datetime(2021, 2, 14, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Hyundai",
            modelo="Tucson",
            anio=2019,
            patente="AG567IJ",
            tipo="suv",
            kilometraje=50000,
            disponible=True,
            costo_diario=17000,
            estado="Activo",
            fecha_registro=datetime(2019, 11, 30, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Kia",
            modelo="Sportage",
            anio=2022,
            patente="AH678KL",
            tipo="suv",
            kilometraje=15000,
            disponible=True,
            costo_diario=18500,
            estado="Activo",
            fecha_registro=datetime(2022, 8, 10, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Nissan",
            modelo="X-Trail",
            anio=2020,
            patente="AI789MN",
            tipo="suv",
            kilometraje=35000,
            disponible=True,
            costo_diario=17500,
            estado="Activo",
            fecha_registro=datetime(2020, 12, 1, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Citroën",
            modelo="Berlingo",
            anio=2018,
            patente="AJ890OP",
            tipo="van",
            kilometraje=85000,
            disponible=True,
            costo_diario=14000,
            estado="activo",
            fecha_registro=datetime(2018, 5, 22, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Iveco",
            modelo="Daily",
            anio=2019,
            patente="AK901QR",
            tipo="van",
            kilometraje=70000,
            disponible=True,
            costo_diario=21000,
            estado="Activo",
            fecha_registro=datetime(2019, 10, 18, tzinfo=timezone.utc)
        ),
        Vehiculo(
            marca="Ford",
            modelo="Transit",
            anio=2021,
            patente="AL012ST",
            tipo="van",
            kilometraje=25000,
            disponible=True,
            costo_diario=19500,
            estado="Activo",
            fecha_registro=datetime(2021, 7, 7, tzinfo=timezone.utc)
        ),
    ]

    db.add_all(vehiculos)
    db.commit()

    # Recargar para obtener los IDs
    for v in vehiculos:
        db.refresh(v)

    print("✅ Vehículos cargados exitosamente.")
    return vehiculos

def seed_clientes(db):
    # ============================
    # 👤 Clientes de prueba
    # ============================
    clientes = [
        Cliente(
            nombre="Ana Martínez",
            dni="30111222",
            telefono="3516001111",
            email="ana.martinez@gmail.com",
            direccion="Av. Colón 123, Córdoba",
            fecha_registro=datetime(2021, 5, 10, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Luis Fernández",
            dni="30222333",
            telefono="3516002222",
            email="luis.fernandez@yahoo.com",
            direccion="San Jerónimo 456, Córdoba",
            fecha_registro=datetime(2020, 3, 15, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="María López",
            dni="30333444",
            telefono="3516003333",
            email="maria.lopez@hotmail.com",
            direccion="Belgrano 789, Córdoba",
            fecha_registro=datetime(2022, 7, 1, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Carlos Gómez",
            dni="30444555",
            telefono="3516004444",
            email="carlos.gomez@empresa.com",
            direccion="Ituzaingó 234, Córdoba",
            fecha_registro=datetime(2023, 8, 20, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Laura Torres",
            dni="30555666",
            telefono="3516005555",
            email="laura.torres@gmail.com",
            direccion="Maipú 567, Córdoba",
            fecha_registro=datetime(2024, 2, 12, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Jorge Ramírez",
            dni="30666777",
            telefono="3516006666",
            email="jorge.ramirez@gmail.com",
            direccion="Av. Sabattini 890, Córdoba",
            fecha_registro=datetime(2021, 9, 30, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Sofía Méndez",
            dni="30777888",
            telefono="3516007777",
            email="sofia.mendez@gmail.com",
            direccion="Av. Vélez Sarsfield 321, Córdoba",
            fecha_registro=datetime(2022, 11, 5, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Diego Herrera",
            dni="30888999",
            telefono="3516008888",
            email="diego.herrera@gmail.com",
            direccion="Av. General Paz 654, Córdoba",
            fecha_registro=datetime(2020, 12, 25, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Carla Suárez",
            dni="30999000",
            telefono="3516009999",
            email="carla.suarez@gmail.com",
            direccion="Av. Patria 987, Córdoba",
            fecha_registro=datetime(2023, 4, 18, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Ricardo Díaz",
            dni="31000111",
            telefono="3516010000",
            email="ricardo.diaz@gmail.com",
            direccion="Av. Alem 111, Córdoba",
            fecha_registro=datetime(2021, 1, 10, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Valeria Castro",
            dni="31111222",
            telefono="3516011111",
            email="valeria.castro@gmail.com",
            direccion="Av. Duarte Quirós 222, Córdoba",
            fecha_registro=datetime(2022, 6, 14, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Federico Morales",
            dni="31222333",
            telefono="3516012222",
            email="federico.morales@gmail.com",
            direccion="Av. Santa Fe 333, Córdoba",
            fecha_registro=datetime(2020, 10, 8, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Gabriela Ríos",
            dni="31333444",
            telefono="3516013333",
            email="gabriela.rios@gmail.com",
            direccion="Av. Olmos 444, Córdoba",
            fecha_registro=datetime(2023, 2, 22, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Hernán Paredes",
            dni="31444555",
            telefono="3516014444",
            email="hernan.paredes@gmail.com",
            direccion="Av. Colón 555, Córdoba",
            fecha_registro=datetime(2024, 5, 1, tzinfo=timezone.utc),
            estado=True
        ),
        Cliente(
            nombre="Natalia Vega",
            dni="31555666",
            telefono="3516015555",
            email="natalia.vega@gmail.com",
            direccion="Av. Rivadavia 666, Córdoba",
            fecha_registro=datetime(2022, 8, 19, tzinfo=timezone.utc),
            estado=True
        ),
    ]

    db.add_all(clientes)
    db.commit()

    for c in clientes:
        db.refresh(c)

    print("✅ Clientes cargados exitosamente.")
    return clientes

def seed_alquileres(db):
    # ============================
    # 📑 Alquileres de prueba
    # ============================
    alquileres = [
         # ---------------- FINALIZADOS ----------------
        Alquiler(
            id_cliente=1,
            id_vehiculo=1,  # Toyota Corolla
            id_empleado=2,
            fecha_inicio=datetime(2023, 5, 1, tzinfo=timezone.utc),
            fecha_fin=datetime(2023, 5, 5, tzinfo=timezone.utc),
            kilometraje_inicial=45000,
            kilometraje_final=45200,
            costo_total=4 * 12000,  # 4 días
            estado="Finalizado"
        ),
        Alquiler(
            id_cliente=2,
            id_vehiculo=2,  # Ford Ranger
            id_empleado=3,
            fecha_inicio=datetime(2023, 6, 10, tzinfo=timezone.utc),
            fecha_fin=datetime(2023, 6, 15, tzinfo=timezone.utc),
            kilometraje_inicial=80000,
            kilometraje_final=80500,
            costo_total=5 * 18000,
            estado="Finalizado"
        ),
        Alquiler(
            id_cliente=3,
            id_vehiculo=3,  # Chevrolet Captiva
            id_empleado=4,
            fecha_inicio=datetime(2023, 7, 20, tzinfo=timezone.utc),
            fecha_fin=datetime(2023, 7, 23, tzinfo=timezone.utc),
            kilometraje_inicial=25000,
            kilometraje_final=25200,
            costo_total=3 * 16000,
            estado="Finalizado"
        ),
        Alquiler(
            id_cliente=4,
            id_vehiculo=5,  # Volkswagen Golf
            id_empleado=2,
            fecha_inicio=datetime(2023, 8, 1, tzinfo=timezone.utc),
            fecha_fin=datetime(2023, 8, 4, tzinfo=timezone.utc),
            kilometraje_inicial=95000,
            kilometraje_final=95300,
            costo_total=3 * 11000,
            estado="Finalizado"
        ),
        Alquiler(
            id_cliente=5,
            id_vehiculo=6,  # Renault Clio
            id_empleado=3,
            fecha_inicio=datetime(2023, 9, 10, tzinfo=timezone.utc),
            fecha_fin=datetime(2023, 9, 12, tzinfo=timezone.utc),
            kilometraje_inicial=60000,
            kilometraje_final=60150,
            costo_total=2 * 9500,
            estado="Finalizado"
        ),
        Alquiler(
            id_cliente=6,
            id_vehiculo=9,  # Hyundai Tucson
            id_empleado=4,
            fecha_inicio=datetime(2023, 10, 5, tzinfo=timezone.utc),
            fecha_fin=datetime(2023, 10, 9, tzinfo=timezone.utc),
            kilometraje_inicial=50000,
            kilometraje_final=50400,
            costo_total=4 * 17000,
            estado="Finalizado"
        ),
        Alquiler(
            id_cliente=7,
            id_vehiculo=10,  # Kia Sportage
            id_empleado=2,
            fecha_inicio=datetime(2023, 11, 1, tzinfo=timezone.utc),
            fecha_fin=datetime(2023, 11, 3, tzinfo=timezone.utc),
            kilometraje_inicial=15000,
            kilometraje_final=15100,
            costo_total=2 * 18500,
            estado="Finalizado"
        ),

        # ---------------- ACTIVOS ----------------
        Alquiler(
            id_cliente=8,
            id_vehiculo=7,  # Peugeot 208
            id_empleado=3,
            fecha_inicio=datetime.now(timezone.utc) - timedelta(days=5),
            kilometraje_inicial=30000,
            estado="Activo"
        ),
        Alquiler(
            id_cliente=9,
            id_vehiculo=8,  # Fiat Cronos
            id_empleado=4,
            fecha_inicio=datetime.now(timezone.utc) - timedelta(days=3),
            kilometraje_inicial=20000,
            estado="Activo"
        ),
        Alquiler(
            id_cliente=1,
            id_vehiculo=11,  # Nissan X-Trail
            id_empleado=2,
            fecha_inicio=datetime.now(timezone.utc) - timedelta(days=7),
            kilometraje_inicial=35000,
            estado="Activo"
        ),
    ]

    db.add_all(alquileres)
    db.commit()

    for a in alquileres:
        db.refresh(a)

    print("✅ Alquileres cargados exitosamente.")
    return alquileres

def seed_mantenimientos(db):
    # ============================
    # 🛠️ Mantenimientos de prueba
    # ============================
    mantenimientos = [
        Mantenimiento(
            id_vehiculo=1,
            id_empleado=1,
            fecha=datetime(2020, 5, 10, tzinfo=timezone.utc),
            km_actual=45000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=2,
            id_empleado=1,
            fecha=datetime(2019, 8, 20, tzinfo=timezone.utc),
            km_actual=80000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=3,
            id_empleado=1,
            fecha=datetime(2022, 7, 1, tzinfo=timezone.utc),
            km_actual=25000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=4,
            id_empleado=1,
            fecha=datetime(2018, 11, 30, tzinfo=timezone.utc),
            km_actual=120000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=5,
            id_empleado=1,
            fecha=datetime(2017, 4, 12, tzinfo=timezone.utc),
            km_actual=95000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=6,
            id_empleado=1,
            fecha=datetime(2018, 6, 20, tzinfo=timezone.utc),
            km_actual=60000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=7,
            id_empleado=1,
            fecha=datetime(2020, 9, 5, tzinfo=timezone.utc),
            km_actual=30000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=8,
            id_empleado=1,
            fecha=datetime(2021, 2, 14, tzinfo=timezone.utc),
            km_actual=20000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=9,
            id_empleado=1,
            fecha=datetime(2019, 11, 30, tzinfo=timezone.utc),
            km_actual=50000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=10,
            id_empleado=1,
            fecha=datetime(2022, 8, 10, tzinfo=timezone.utc),
            km_actual=15000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=11,
            id_empleado=1,
            fecha=datetime(2020, 12, 1, tzinfo=timezone.utc),
            km_actual=35000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=12,
            id_empleado=1,
            fecha=datetime(2018, 5, 22, tzinfo=timezone.utc),
            km_actual=85000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=13,
            id_empleado=1,
            fecha=datetime(2019, 10, 18, tzinfo=timezone.utc),
            km_actual=70000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
        Mantenimiento(
            id_vehiculo=14,
            id_empleado=1,
            fecha=datetime(2021, 7, 7, tzinfo=timezone.utc),
            km_actual=25000,
            tipo="confirmacion",
            costo=0,
            observaciones="Mantenimiento inicial de confirmación",
            km_prox_mant=10000,
            meses_prox_mant=12
        ),
    ]


    db.add_all(mantenimientos)
    db.commit()

    for m in mantenimientos:
        db.refresh(m)

    print("✅ Mantenimientos cargados exitosamente.")
    return mantenimientos

def seed_multas(db):
    # ============================
    # ⚠️ Multas de prueba
    # ============================
    multas = [
        Multa(
            id_alquiler=1,   # asociada al primer alquiler
            tipo="Exceso de velocidad",
            descripcion="El cliente superó el límite de velocidad en autopista.",
            costo=15000.0,
            fecha=datetime(2023, 5, 12, tzinfo=timezone.utc)
        ),
        Multa(
            id_alquiler=4,   # asociada a otro alquiler
            tipo="Estacionamiento indebido",
            descripcion="El vehículo fue encontrado estacionado en zona prohibida.",
            costo=8000.0,
            fecha=datetime(2023, 8, 7, tzinfo=timezone.utc)
        ),
        Multa(
            id_alquiler=7,   # asociada a un tercer alquiler
            tipo="Daños al vehículo",
            descripcion="Se detectaron rayones en la carrocería al finalizar el alquiler.",
            costo=25000.0,
            fecha=datetime(2023, 11, 6, tzinfo=timezone.utc)
        ),
    ]

    db.add_all(multas)
    db.commit()

    for m in multas:
        db.refresh(m)

    print("✅ Multas cargadas exitosamente.")
    return multas


if __name__ == "__main__":
    seed()