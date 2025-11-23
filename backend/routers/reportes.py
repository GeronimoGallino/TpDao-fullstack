
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database
from ..schemas import reportes as schemas_reportes
from ..schemas import alquiler as schemas_alquiler
from ..services import reportes as reportes_service
from ..database import get_db
from typing import Optional
from fastapi import Query

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/alquileres-por-cliente/{cliente_id}", response_model=list[schemas_alquiler.AlquilerClienteDetalle])
def obtener_alquileres_por_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    result = reportes_service.get_alquileres_por_cliente(db, cliente_id)

    if not result:
        raise HTTPException(404, "Este cliente no tiene alquileres")

    return result

@router.get("/vehiculos-mas-alquilados", response_model=list[schemas_reportes.VehiculoMasAlquilado])
def vehiculos_mas_alquilados(limite: int = 5, db: Session = Depends(get_db)):
    resultados = reportes_service.get_vehiculos_mas_alquilados(db, limite)

    respuesta = []
    for vehiculo, cantidad in resultados:
        respuesta.append({
            "id_vehiculo": vehiculo.id,
            "marca": vehiculo.marca,
            "modelo": vehiculo.modelo,
            "patente": vehiculo.patente,
            "veces_alquilado": cantidad
        })

    return respuesta

@router.get("/alquileres-por-periodo", response_model=dict)
def alquileres_por_periodo(
    tipo: str,
    anio: int,
    valor: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    resultado = reportes_service.alquileres_por_periodo(db, tipo, anio, valor)
    return resultado