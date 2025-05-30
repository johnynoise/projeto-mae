from fastapi import APIRouter,Depends
from dependecies import pegar_sessao
from models import db, Usuario


auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.get("/")
async def autenticar():
    return {"message": "Voce está autenticado", "autenticado": False}

@auth_router.post("/criar_conta") 
async def registro(nome: str, email: str, senha: str, session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        return {"message": "Email já cadastrado"}
    # Verifica se o email já está cadastrado
    else:
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        session.add(novo_usuario)
        session.commit()
        return {"message": "Usuário criado com sucesso", "email": email}
