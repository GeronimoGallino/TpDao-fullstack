from fastapi import FastAPI
from backend import models
from backend.database import engine, Base
from backend.routers import cliente

from backend.routers import cliente as cliente_router
from backend.routers import empleado as empleado_router
# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Inicializar la app
app = FastAPI()

# Incluir routers
app.include_router(cliente.router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
