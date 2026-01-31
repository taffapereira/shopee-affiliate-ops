"""
Configurações compartilhadas para testes
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.connection import Base


@pytest.fixture(scope="function")
def db_session():
    """
    Cria uma sessão de banco de dados temporária para testes
    """
    # Usa SQLite in-memory para testes
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()


@pytest.fixture
def sample_produto():
    """Produto de exemplo para testes"""
    return {
        "shopee_id": "12345_67890",
        "nome": "Fone Bluetooth Test",
        "descricao": "Fone de teste",
        "preco_original": 100.0,
        "preco_promocional": 80.0,
        "desconto_percentual": 20.0,
        "comissao_percentual": 10.0,
        "comissao_valor": 8.0,
        "rating": 4.5,
        "total_vendas": 100,
        "total_avaliacoes": 50,
        "nicho": "tech",
        "categoria_shopee": "Electronics",
        "url_produto": "https://shopee.com.br/test",
        "imagem_url": "https://example.com/image.jpg"
    }
