from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.plan_mantenimiento import PlanMantenimiento
from .. import database
from ..schemas import plan_mantenimiento as schemas

router = APIRouter(prefix="/planes_mantenimiento", tags=["Planes de Mantenimiento"])

@router.post("/", response_model=schemas.PlanMantenimiento)
def crear_plan_mantenimiento(plan: schemas.PlanMantenimientoCreate, db: Session = Depends(database.get_db)):
    nuevo_plan = PlanMantenimiento(**plan.model_dump())
    db.add(nuevo_plan)
    db.commit()
    db.refresh(nuevo_plan)
    return nuevo_plan   

@router.get("/", response_model=list[schemas.PlanMantenimiento])
def listar_planes_mantenimiento(db: Session = Depends(database.get_db)):
    return db.query(PlanMantenimiento).all()    

@router.get("/{plan_id}", response_model=schemas.PlanMantenimiento)
def obtener_plan_mantenimiento(plan_id: int, db: Session = Depends(database.get_db)):
    plan = db.query(PlanMantenimiento).filter(PlanMantenimiento.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de mantenimiento no encontrado")
    return plan

@router.put("/{plan_id}", response_model=schemas.PlanMantenimiento)
def actualizar_plan_mantenimiento(plan_id: int, datos: schemas.PlanMantenimientoCreate, db: Session = Depends(database.get_db)):
    plan = db.query(PlanMantenimiento).filter(PlanMantenimiento.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de mantenimiento no encontrado")
    for key, value in datos.model_dump().items():
        setattr(plan, key, value)
    db.commit()
    db.refresh(plan)
    return plan

@router.delete("/{plan_id}")
def eliminar_plan_mantenimiento(plan_id: int, db: Session = Depends(database.get_db)):
    plan = db.query(PlanMantenimiento).filter(PlanMantenimiento.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de mantenimiento no encontrado")
    db.delete(plan)
    db.commit()
    return {"mensaje": "Plan de mantenimiento eliminado correctamente"}



