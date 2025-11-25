from fastapi import FastAPI
from backend import models
from backend.database import engine, Base
from backend.routers import cliente, vehiculo, empleado, alquiler, reportes , mantenimiento, multa
from fastapi.middleware.cors import CORSMiddleware

# Crear tablas
Base.metadata.create_all(bind=engine)

# Inicializar
app = FastAPI()

# === CORS ===
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ============

# Routers
app.include_router(cliente.router, prefix="/api")
app.include_router(vehiculo.router, prefix="/api")
app.include_router(empleado.router, prefix="/api")
app.include_router(alquiler.router, prefix="/api")
app.include_router(mantenimiento.router, prefix="/api")
app.include_router(reportes.router, prefix="/api")
app.include_router(multa.router, prefix="/api")

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
