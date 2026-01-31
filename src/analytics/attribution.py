"""
Sistema de atribuição de conversões por SubIds
"""
from typing import Dict, List
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)


class AttributionSystem:
    """
    Sistema de atribuição de conversões baseado em SubIds
    """
    
    def attribute_conversion(
        self,
        sub_id1: str,  # canal
        sub_id2: str,  # nicho
        sub_id3: str,  # formato
        sub_id4: str,  # campanha
        sub_id5: str,  # data
        revenue: float
    ) -> Dict:
        """
        Atribui conversão aos seus componentes
        
        Args:
            sub_id1 a sub_id5: SubIds da conversão
            revenue: Valor da conversão
            
        Returns:
            Dict com atribuição detalhada
        """
        attribution = {
            "canal": sub_id1,
            "nicho": sub_id2,
            "formato": sub_id3,
            "campanha": sub_id4,
            "data": sub_id5,
            "revenue": revenue,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(
            "Conversão atribuída",
            canal=sub_id1,
            nicho=sub_id2,
            revenue=revenue
        )
        
        return attribution
    
    def aggregate_by_channel(
        self,
        conversions: List[Dict]
    ) -> Dict[str, Dict]:
        """
        Agrega conversões por canal
        
        Args:
            conversions: Lista de conversões
            
        Returns:
            Agregado por canal
        """
        aggregated = {}
        
        for conv in conversions:
            canal = conv.get("canal", "unknown")
            
            if canal not in aggregated:
                aggregated[canal] = {
                    "count": 0,
                    "total_revenue": 0.0
                }
            
            aggregated[canal]["count"] += 1
            aggregated[canal]["total_revenue"] += conv.get("revenue", 0.0)
        
        return aggregated
    
    def aggregate_by_nicho(
        self,
        conversions: List[Dict]
    ) -> Dict[str, Dict]:
        """
        Agrega conversões por nicho
        
        Args:
            conversions: Lista de conversões
            
        Returns:
            Agregado por nicho
        """
        aggregated = {}
        
        for conv in conversions:
            nicho = conv.get("nicho", "unknown")
            
            if nicho not in aggregated:
                aggregated[nicho] = {
                    "count": 0,
                    "total_revenue": 0.0
                }
            
            aggregated[nicho]["count"] += 1
            aggregated[nicho]["total_revenue"] += conv.get("revenue", 0.0)
        
        return aggregated
    
    def get_top_performers(
        self,
        conversions: List[Dict],
        by: str = "canal",
        limit: int = 5
    ) -> List[tuple]:
        """
        Retorna top performers
        
        Args:
            conversions: Lista de conversões
            by: Agrupar por (canal, nicho, campanha, formato)
            limit: Limite de resultados
            
        Returns:
            Lista de tuplas (key, metrics)
        """
        if by == "canal":
            aggregated = self.aggregate_by_channel(conversions)
        elif by == "nicho":
            aggregated = self.aggregate_by_nicho(conversions)
        else:
            return []
        
        # Ordena por revenue
        sorted_items = sorted(
            aggregated.items(),
            key=lambda x: x[1]["total_revenue"],
            reverse=True
        )
        
        return sorted_items[:limit]


# Instância global
attribution_system = AttributionSystem()
