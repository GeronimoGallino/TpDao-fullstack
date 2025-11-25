from pydantic import BaseModel


class UsuarioBase(BaseModel):
    email: str
    id: int
    role: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    password: str

    class Config:
        from_attributes = True
