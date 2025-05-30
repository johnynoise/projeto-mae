from sqlalchemy.orm import sessionmaker
from models import db, Usuario


def pegar_sessao():
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
    finally:
        session.close()
   