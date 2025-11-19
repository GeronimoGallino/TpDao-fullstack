from fastapi import FastAPI
from backend.database import Base, engine
from backend.models import cliente, empleado  # importa solo los modelos, NO toda la carpeta models

from backend.routers import cliente as cliente_router
from backend.routers import empleado as empleado_router
# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Inicializar la app
app = FastAPI()

# Incluir routers
app.include_router(cliente_router.router)
app.include_router(empleado_router.router)


@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
