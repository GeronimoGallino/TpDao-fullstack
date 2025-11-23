from pydantic import BaseModel

class VehiculoMasAlquilado(BaseModel):
    id_vehiculo: int
    marca: str
    modelo: str
    patente: str
    veces_alquilado: int

    model_config = {
        "from_attributes": True
    }
