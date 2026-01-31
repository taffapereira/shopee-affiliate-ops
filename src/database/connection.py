"""
Conexão com o banco de dados usando SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from config.credentials import credentials

# Engine do SQLAlchemy
engine = create_engine(
    credentials.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in credentials.DATABASE_URL else {},
    echo=credentials.ENVIRONMENT == "development"
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection para FastAPI - retorna sessão do banco
    
    Yields:
        Session do SQLAlchemy
        
    Exemplo:
        @app.get("/produtos")
        def get_produtos(db: Session = Depends(get_db)):
            return db.query(Produto).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas
    """
    from src.database.models import Produto, ConteudoGerado, Link, Analytics
    
    Base.metadata.create_all(bind=engine)
