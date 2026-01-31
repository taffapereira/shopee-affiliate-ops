"""
Configurações gerais da aplicação
"""
from typing import Dict, List
from config.constants import NICHOS, CANAIS, FORMATOS, CAMPANHAS


class Settings:
    """Configurações gerais do sistema"""
    
    # Versão do sistema
    VERSION = "1.0.0"
    APP_NAME = "Shopee Affiliate Ops"
    
    # Nichos e configurações
    NICHOS = NICHOS
    CANAIS = CANAIS
    FORMATOS = FORMATOS
    CAMPANHAS = CAMPANHAS
    
    # Configurações de coleta
    COLETA_HORA_INICIO = "06:00"
    COLETA_PRODUTOS_POR_NICHO = 50
    COLETA_TOP_N = 10
    
    # Configurações de conteúdo
    VARIACOES_POR_PRODUTO = 5
    VIDEO_DURACAO_PADRAO = 30  # segundos
    
    # Configurações de publicação
    INTERVALO_ENTRE_POSTS_MINUTOS = 120  # 2 horas
    
    # Analytics
    ANALYTICS_HORA_FETCH = "23:00"
    DIAS_HISTORICO_ANALYTICS = 30
    
    @staticmethod
    def get_nicho_config(nicho: str) -> Dict:
        """
        Retorna a configuração de um nicho específico
        
        Args:
            nicho: Nome do nicho (casa, tech, pet, cosmeticos)
            
        Returns:
            Dicionário com configuração do nicho
        """
        return NICHOS.get(nicho, {})
    
    @staticmethod
    def get_canal_config(canal: str) -> Dict:
        """
        Retorna a configuração de um canal específico
        
        Args:
            canal: Nome do canal (tiktok, reels, stories, grupo)
            
        Returns:
            Dicionário com configuração do canal
        """
        return CANAIS.get(canal, {})
    
    @staticmethod
    def get_nichos_ativos() -> List[str]:
        """
        Retorna lista de nichos ativos
        
        Returns:
            Lista com nomes dos nichos
        """
        return list(NICHOS.keys())
    
    @staticmethod
    def get_canais_ativos() -> List[str]:
        """
        Retorna lista de canais ativos ordenados por prioridade
        
        Returns:
            Lista com nomes dos canais
        """
        return sorted(CANAIS.keys(), key=lambda x: CANAIS[x]["prioridade"])


# Instância global
settings = Settings()
