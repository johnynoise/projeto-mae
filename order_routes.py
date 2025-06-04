from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from dependecies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    return {"message": "Lista de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario_id=pedido_schema.usuario_id)
    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)
    
    return {"message": "Pedido criado com sucesso"}