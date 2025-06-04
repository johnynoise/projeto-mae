from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: Optional[bool] 
    telefone: Optional[str] 
    admin: Optional[bool]

    class Config:
        from_attributes = True

class PedidoSchema(BaseModel):
    usuario_id: int


    class Config:
        from_attributes = True
        
        
class loginSchema(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True