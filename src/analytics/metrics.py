"""
Cálculo de métricas de performance
"""
from typing import Dict, List
from datetime import datetime, timedelta

from src.utils.logger import get_logger

logger = get_logger(__name__)


class MetricsCalculator:
    """
    Calcula métricas de performance (CTR, conversão, ROI, etc)
    """
    
    def calculate_ctr(self, clicks: int, impressions: int) -> float:
        """
        Calcula Click-Through Rate
        
        Args:
            clicks: Número de cliques
            impressions: Número de impressões
            
        Returns:
            CTR em percentual
        """
        if impressions == 0:
            return 0.0
        
        ctr = (clicks / impressions) * 100
        return round(ctr, 2)
    
    def calculate_conversion_rate(self, conversions: int, clicks: int) -> float:
        """
        Calcula taxa de conversão
        
        Args:
            conversions: Número de conversões
            clicks: Número de cliques
            
        Returns:
            Taxa de conversão em percentual
        """
        if clicks == 0:
            return 0.0
        
        rate = (conversions / clicks) * 100
        return round(rate, 2)
    
    def calculate_average_order_value(
        self,
        total_revenue: float,
        total_orders: int
    ) -> float:
        """
        Calcula ticket médio
        
        Args:
            total_revenue: Receita total
            total_orders: Número de pedidos
            
        Returns:
            Ticket médio
        """
        if total_orders == 0:
            return 0.0
        
        aov = total_revenue / total_orders
        return round(aov, 2)
    
    def calculate_epc(self, earnings: float, clicks: int) -> float:
        """
        Calcula Earnings Per Click
        
        Args:
            earnings: Ganhos totais
            clicks: Total de cliques
            
        Returns:
            EPC
        """
        if clicks == 0:
            return 0.0
        
        epc = earnings / clicks
        return round(epc, 2)
    
    def calculate_roi(self, revenue: float, cost: float) -> float:
        """
        Calcula Return on Investment
        
        Args:
            revenue: Receita gerada
            cost: Custo investido
            
        Returns:
            ROI em percentual
        """
        if cost == 0:
            return 0.0
        
        roi = ((revenue - cost) / cost) * 100
        return round(roi, 2)
    
    def generate_summary_metrics(self, data: Dict) -> Dict:
        """
        Gera resumo de todas as métricas
        
        Args:
            data: Dict com dados brutos
            
        Returns:
            Dict com métricas calculadas
        """
        impressions = data.get("impressions", 0)
        clicks = data.get("clicks", 0)
        conversions = data.get("conversions", 0)
        revenue = data.get("revenue", 0.0)
        cost = data.get("cost", 0.0)
        
        summary = {
            "ctr": self.calculate_ctr(clicks, impressions),
            "conversion_rate": self.calculate_conversion_rate(conversions, clicks),
            "aov": self.calculate_average_order_value(revenue, conversions),
            "epc": self.calculate_epc(revenue, clicks),
            "roi": self.calculate_roi(revenue, cost),
            "total_impressions": impressions,
            "total_clicks": clicks,
            "total_conversions": conversions,
            "total_revenue": revenue,
            "total_cost": cost,
            "profit": revenue - cost
        }
        
        logger.debug("Métricas calculadas", summary=summary)
        
        return summary
    
    def compare_periods(
        self,
        current_metrics: Dict,
        previous_metrics: Dict
    ) -> Dict:
        """
        Compara métricas entre períodos
        
        Args:
            current_metrics: Métricas período atual
            previous_metrics: Métricas período anterior
            
        Returns:
            Dict com comparações e variações
        """
        comparison = {}
        
        for key in current_metrics:
            current_value = current_metrics.get(key, 0)
            previous_value = previous_metrics.get(key, 0)
            
            if previous_value == 0:
                variation = 0.0
            else:
                variation = ((current_value - previous_value) / previous_value) * 100
            
            comparison[key] = {
                "current": current_value,
                "previous": previous_value,
                "variation_percent": round(variation, 2)
            }
        
        return comparison


# Instância global
metrics_calculator = MetricsCalculator()
