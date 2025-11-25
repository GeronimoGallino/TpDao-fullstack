from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    # Email como PRIMARY KEY
    email = Column(String, primary_key=True, index=True)

    # FK al empleado
    id = Column(Integer, ForeignKey("empleados.id"), nullable=False, unique=True)

    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # Relación opcional (si querés acceder al empleado desde el usuario)
    empleado = relationship("Empleado")
