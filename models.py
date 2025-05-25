from sqlalchemy import create_engine,Column,Integer,String, Boolean,Float, ForeignKey # type: ignore
from sqlalchemy.orm import declarative_base # type: ignore
from sqlalchemy import Enum # type: ignore

#Conexão banco de dados
db = create_engine("sqlite:///banco.db")

#Base do banco de dados
Base = declarative_base()

#Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True,autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha = Column(String(50), nullable=False)
    ativo = Column(Boolean, default=True)
    telefone = Column(String(15), nullable=True)
    endereco = Column(String(100), nullable=True)
    admin = Column(Boolean, default=False)
    
    def __init__(self, nome, email, senha, ativo=True, telefone=None, endereco=None, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.telefone = telefone
        self.endereco = endereco
        self.admin = admin
#Pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    STATUS_PEDIDOS = ("Pendente", "Aprovado", "Entregue", "Cancelado")

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status = Column(Enum(*STATUS_PEDIDOS, name="status_pedido"), nullable=False)
    valor_total = Column(Float, nullable=False)
    
    def __init__(self, usuario_id, status="Pendente", valor_total=0):
        self.usuario_id = usuario_id
        self.status = status
        self.valor_total = valor_total
#ItensPedido

class ItensPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    sabor = Column(String(50), nullable=True)
    tamanho = Column(String(50), nullable=True)
    preco_unitario = Column(Float, nullable=False)
    
    
    def __init__(self, pedido_id, sabor, tamanho,preco_unitario, quantidade):
        self.pedido_id = pedido_id
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade
        
