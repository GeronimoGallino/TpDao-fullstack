from fastapi import FastAPI
from backend import models
from backend.database import engine, Base
from backend.routers import cliente, vehiculo, empleado, alquiler, reportes

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Inicializar la app
app = FastAPI()

# Incluir routers
app.include_router(cliente.router, prefix="/api")
app.include_router(vehiculo.router, prefix="/api")
app.include_router(empleado.router, prefix="/api")
app.include_router(alquiler.router, prefix="/api")
app.include_router(reportes.router, prefix="/api")

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
