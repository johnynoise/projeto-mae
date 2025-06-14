from fastapi import APIRouter,Depends, HTTPException
from dependecies import pegar_sessao
from models import db, Usuario
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema
from sqlalchemy.orm import Session
from schemas import loginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone



auth_router = APIRouter(prefix="/auth",tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        "sub": id_usuario,
        "data_expiracao": data_expiracao.isoformat(),
    }
    jwt_codificado = jwt.encode(dic_info,SECRET_KEY, ALGORITHM)
    return jwt_codificado

def verificar_token(token, session: Session = Depends(pegar_sessao)):
    #verifica se o token é válido
    #extrair o id do usuário do token
    Usuario = session.query(Usuario).filter(Usuario.id == 1).first()
    return Usuario

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario
 
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

@auth_router.post("/login")
async def login(login_schema: loginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    if not bcrypt_context.verify(login_schema.senha, usuario.senha):
        raise HTTPException(status_code=400, detail="Senha incorreta")
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7)) 
    return {"access_token": access_token,
            "refresh_token":refresh_token,
            "token_type": "bearer"}
    
@auth_router.get("/verificar_token")
async def atualizar_token(token: str, session: Session = Depends(pegar_sessao)):
    usuario = verificar_token(token, session)
    access_token = criar_token(criar_token(usuario.id))
    return {"access_token": access_token, "token_type": "bearer", "usuario_id": usuario.id}