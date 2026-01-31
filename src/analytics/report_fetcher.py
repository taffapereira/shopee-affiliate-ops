"""
Fetcher de relatórios da API Shopee
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from src.collectors.shopee_api import ShopeeAffiliateAPI
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ReportFetcher:
    """
    Busca relatórios de performance da API Shopee
    """
    
    def __init__(self):
        self.api = ShopeeAffiliateAPI()
    
    async def fetch_daily_report(self, date: datetime = None) -> Optional[Dict]:
        """
        Busca relatório diário
        
        Args:
            date: Data do relatório (padrão: ontem)
            
        Returns:
            Dict com dados do relatório
        """
        if date is None:
            date = datetime.now() - timedelta(days=1)
        
        logger.info("Buscando relatório diário", date=date.strftime("%Y-%m-%d"))
        
        # Implementação placeholder
        # Na API real da Shopee, usaríamos endpoint específico
        return {
            "date": date.strftime("%Y-%m-%d"),
            "clicks": 0,
            "orders": 0,
            "revenue": 0.0,
            "commission": 0.0
        }
    
    async def fetch_performance_by_product(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        Busca performance por produto
        
        Args:
            start_date: Data início
            end_date: Data fim
            
        Returns:
            Lista de produtos com métricas
        """
        logger.info(
            "Buscando performance por produto",
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d")
        )
        
        # Placeholder
        return []
    
    async def fetch_performance_by_channel(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Dict]:
        """
        Busca performance por canal (baseado em subIds)
        
        Args:
            start_date: Data início
            end_date: Data fim
            
        Returns:
            Dict com performance por canal
        """
        logger.info("Buscando performance por canal")
        
        # Placeholder
        return {
            "tiktok": {"clicks": 0, "conversions": 0, "revenue": 0.0},
            "reels": {"clicks": 0, "conversions": 0, "revenue": 0.0},
            "stories": {"clicks": 0, "conversions": 0, "revenue": 0.0},
            "grupo": {"clicks": 0, "conversions": 0, "revenue": 0.0}
        }


# Instância global
report_fetcher = ReportFetcher()
