"""
Loader de credenciais a partir de variáveis de ambiente
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class Credentials:
    """Gerenciador de credenciais da aplicação"""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./shopee_affiliate.db")
    
    # Shopee Affiliate API
    SHOPEE_AFFILIATE_API_KEY: Optional[str] = os.getenv("SHOPEE_AFFILIATE_API_KEY")
    SHOPEE_AFFILIATE_SECRET: Optional[str] = os.getenv("SHOPEE_AFFILIATE_SECRET")
    SHOPEE_PARTNER_ID: Optional[str] = os.getenv("SHOPEE_PARTNER_ID")
    
    # LLM APIs
    DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_GROUP_CASA_ID: Optional[str] = os.getenv("TELEGRAM_GROUP_CASA_ID")
    TELEGRAM_GROUP_TECH_ID: Optional[str] = os.getenv("TELEGRAM_GROUP_TECH_ID")
    TELEGRAM_GROUP_PET_ID: Optional[str] = os.getenv("TELEGRAM_GROUP_PET_ID")
    TELEGRAM_GROUP_COSMETICOS_ID: Optional[str] = os.getenv("TELEGRAM_GROUP_COSMETICOS_ID")
    TELEGRAM_ALERT_CHANNEL_ID: Optional[str] = os.getenv("TELEGRAM_ALERT_CHANNEL_ID")
    
    # Buffer
    BUFFER_ACCESS_TOKEN: Optional[str] = os.getenv("BUFFER_ACCESS_TOKEN")
    
    # Cloudflare R2
    R2_ACCOUNT_ID: Optional[str] = os.getenv("R2_ACCOUNT_ID")
    R2_ACCESS_KEY_ID: Optional[str] = os.getenv("R2_ACCESS_KEY_ID")
    R2_SECRET_ACCESS_KEY: Optional[str] = os.getenv("R2_SECRET_ACCESS_KEY")
    R2_BUCKET_NAME: str = os.getenv("R2_BUCKET_NAME", "shopee-videos")
    
    # Configurações gerais
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    TIMEZONE: str = os.getenv("TIMEZONE", "America/Sao_Paulo")
    
    # Limites
    MAX_POSTS_TIKTOK_PER_DAY: int = int(os.getenv("MAX_POSTS_TIKTOK_PER_DAY", "4"))
    MAX_POSTS_REELS_PER_DAY: int = int(os.getenv("MAX_POSTS_REELS_PER_DAY", "3"))
    MAX_POSTS_STORIES_PER_DAY: int = int(os.getenv("MAX_POSTS_STORIES_PER_DAY", "6"))
    MAX_POSTS_TELEGRAM_PER_DAY: int = int(os.getenv("MAX_POSTS_TELEGRAM_PER_DAY", "10"))
    
    # Nichos ativos
    ACTIVE_NICHES: list[str] = os.getenv("ACTIVE_NICHES", "casa,tech,pet,cosmeticos").split(",")
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Valida se todas as credenciais necessárias estão configuradas
        
        Returns:
            tuple: (is_valid, missing_credentials)
        """
        required_fields = [
            "SHOPEE_AFFILIATE_API_KEY",
            "SHOPEE_AFFILIATE_SECRET",
            "SHOPEE_PARTNER_ID",
        ]
        
        missing = []
        for field in required_fields:
            if not getattr(cls, field):
                missing.append(field)
        
        return len(missing) == 0, missing
    
    @classmethod
    def get_telegram_group_id(cls, nicho: str) -> Optional[str]:
        """
        Retorna o ID do grupo Telegram para um nicho específico
        
        Args:
            nicho: Nome do nicho (casa, tech, pet, cosmeticos)
            
        Returns:
            ID do grupo Telegram ou None
        """
        mapping = {
            "casa": cls.TELEGRAM_GROUP_CASA_ID,
            "tech": cls.TELEGRAM_GROUP_TECH_ID,
            "pet": cls.TELEGRAM_GROUP_PET_ID,
            "cosmeticos": cls.TELEGRAM_GROUP_COSMETICOS_ID,
        }
        return mapping.get(nicho)


# Instância global
credentials = Credentials()
