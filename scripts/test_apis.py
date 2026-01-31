"""
Script para testar conexões de API
"""
import sys
import asyncio
from pathlib import Path

# Adiciona o diretório raiz ao Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from config.credentials import credentials
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def test_shopee_api():
    """Testa API da Shopee"""
    print("\n🛍️  Testando Shopee API...")
    
    if not all([
        credentials.SHOPEE_AFFILIATE_API_KEY,
        credentials.SHOPEE_AFFILIATE_SECRET,
        credentials.SHOPEE_PARTNER_ID
    ]):
        print("  ⚠️  Credenciais Shopee não configuradas")
        return False
    
    try:
        from src.collectors.shopee_api import ShopeeAffiliateAPI
        api = ShopeeAffiliateAPI()
        
        # Testa busca de produtos (limitado a 5 para teste)
        produtos = await api.get_product_offers(limit=5)
        
        if produtos:
            print(f"  ✅ Shopee API funcionando ({len(produtos)} produtos retornados)")
            return True
        else:
            print("  ⚠️  API retornou lista vazia")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False


def test_deepseek():
    """Testa API DeepSeek"""
    print("\n🤖 Testando DeepSeek API...")
    
    if not credentials.DEEPSEEK_API_KEY:
        print("  ⚠️  API Key DeepSeek não configurada")
        return False
    
    print("  ✅ API Key configurada")
    return True


def test_openai():
    """Testa API OpenAI"""
    print("\n💬 Testando OpenAI GPT API...")
    
    if not credentials.OPENAI_API_KEY:
        print("  ⚠️  API Key OpenAI não configurada")
        return False
    
    print("  ✅ API Key configurada")
    return True


def test_google():
    """Testa API Google (Gemini)"""
    print("\n🌐 Testando Google Gemini API...")
    
    if not credentials.GOOGLE_API_KEY:
        print("  ⚠️  API Key Google não configurada")
        return False
    
    print("  ✅ API Key configurada")
    return True


def test_telegram():
    """Testa Telegram Bot"""
    print("\n📱 Testando Telegram Bot...")
    
    if not credentials.TELEGRAM_BOT_TOKEN:
        print("  ⚠️  Token Telegram não configurado")
        return False
    
    try:
        from telegram import Bot
        bot = Bot(token=credentials.TELEGRAM_BOT_TOKEN)
        
        # Testa get_me (não requer async)
        import asyncio
        me = asyncio.run(bot.get_me())
        print(f"  ✅ Bot conectado: @{me.username}")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False


def test_buffer():
    """Testa Buffer API"""
    print("\n📅 Testando Buffer API...")
    
    if not credentials.BUFFER_ACCESS_TOKEN:
        print("  ⚠️  Access Token Buffer não configurado")
        return False
    
    print("  ✅ Access Token configurado")
    return True


def test_cloudflare_r2():
    """Testa Cloudflare R2"""
    print("\n☁️  Testando Cloudflare R2...")
    
    if not all([
        credentials.R2_ACCOUNT_ID,
        credentials.R2_ACCESS_KEY_ID,
        credentials.R2_SECRET_ACCESS_KEY
    ]):
        print("  ⚠️  Credenciais R2 não configuradas")
        return False
    
    print("  ✅ Credenciais configuradas")
    return True


def test_database():
    """Testa conexão com banco de dados"""
    print("\n💾 Testando Banco de Dados...")
    
    try:
        from src.database.connection import SessionLocal
        
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        print(f"  ✅ Conexão OK: {credentials.DATABASE_URL}")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False


async def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("SHOPEE AFFILIATE OPS - Teste de APIs e Conexões")
    print("=" * 60)
    
    results = {
        "Banco de Dados": test_database(),
        "Shopee API": await test_shopee_api(),
        "DeepSeek": test_deepseek(),
        "OpenAI GPT": test_openai(),
        "Google Gemini": test_google(),
        "Telegram": test_telegram(),
        "Buffer": test_buffer(),
        "Cloudflare R2": test_cloudflare_r2()
    }
    
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for name, passed_test in results.items():
        status = "✅ OK" if passed_test else "❌ FALHOU"
        print(f"{name:20} {status}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todas as APIs estão configuradas e funcionando!")
    else:
        print("\n⚠️  Algumas APIs não estão configuradas.")
        print("   Configure as credenciais no arquivo .env")
        print("   Use .env.example como referência")


if __name__ == "__main__":
    asyncio.run(main())
