"""
Script para inicializar o banco de dados
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.database.connection import init_db, engine
from src.database.models import Base
from src.utils.logger import get_logger

logger = get_logger(__name__)


def setup_database():
    """
    Inicializa o banco de dados criando todas as tabelas
    """
    try:
        logger.info("Iniciando setup do banco de dados...")
        
        # Cria todas as tabelas
        init_db()
        
        logger.info("✅ Banco de dados inicializado com sucesso!")
        logger.info(f"📊 Tabelas criadas: {', '.join(Base.metadata.tables.keys())}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco de dados: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("SHOPEE AFFILIATE OPS - Setup do Banco de Dados")
    print("=" * 60)
    print()
    
    success = setup_database()
    
    if success:
        print()
        print("✨ Setup concluído! Você pode agora:")
        print("  1. Rodar o servidor: python -m uvicorn src.api.main:app --reload")
        print("  2. Testar as APIs: python scripts/test_apis.py")
        print("  3. Executar primeiro ciclo: python scripts/first_run.py")
    else:
        print()
        print("❌ Setup falhou. Verifique os logs acima.")
        sys.exit(1)
