from fastapi import FastAPI
from backend import models
from backend.database import engine
from backend.routers import cliente

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)

# Inicializar la app
app = FastAPI()

# Incluir routers
app.include_router(cliente.router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
