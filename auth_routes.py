from fastapi import APIRouter,Depends, HTTPException
from dependecies import pegar_sessao
from models import db, Usuario
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.get("/")
async def autenticar():
    return {"message": "Voce está autenticado", "autenticado": False}

@auth_router.post("/criar_conta") 
async def registro(usuario_schema:UsuarioSchema, session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    # Não precisa de else aqui
    senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(
        nome=usuario_schema.nome,
        email=usuario_schema.email,
        senha=senha_criptografada,
        ativo=usuario_schema.ativo,
        telefone=usuario_schema.telefone,
        admin=usuario_schema.admin
    )
    session.add(novo_usuario)
    session.commit()
    return {"message": "Usuário criado com sucesso", "email": usuario_schema.email}