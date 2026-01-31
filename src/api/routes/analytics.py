"""
Rotas de Analytics - Relatórios e métricas
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.database.connection import get_db
from src.database import repository
from src.analytics.metrics import metrics_calculator
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/summary")
async def get_summary(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Retorna resumo de analytics dos últimos N dias
    
    Args:
        days: Número de dias
        db: Sessão do banco
        
    Returns:
        Resumo de métricas
    """
    resumo = repository.AnalyticsRepository.resumo_ultimos_dias(db, days)
    
    return {
        "periodo": f"Últimos {days} dias",
        "metricas": resumo
    }


@router.get("/by-canal")
async def analytics_by_canal(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """
    Analytics por canal
    
    Args:
        start_date: Data início (YYYY-MM-DD)
        end_date: Data fim (YYYY-MM-DD)
        db: Sessão do banco
        
    Returns:
        Métricas por canal
    """
    if not start_date:
        start = datetime.now() - timedelta(days=7)
    else:
        start = datetime.fromisoformat(start_date)
    
    if not end_date:
        end = datetime.now()
    else:
        end = datetime.fromisoformat(end_date)
    
    analytics = repository.AnalyticsRepository.buscar_por_periodo(
        db, start, end
    )
    
    # Agrupa por canal
    by_canal = {}
    for a in analytics:
        canal = a.canal or "unknown"
        
        if canal not in by_canal:
            by_canal[canal] = {
                "cliques": 0,
                "conversoes": 0,
                "receita": 0.0,
                "comissao": 0.0
            }
        
        by_canal[canal]["cliques"] += a.cliques
        by_canal[canal]["conversoes"] += a.conversoes
        by_canal[canal]["receita"] += a.receita
        by_canal[canal]["comissao"] += a.comissao
    
    return {
        "periodo": {
            "inicio": start.strftime("%Y-%m-%d"),
            "fim": end.strftime("%Y-%m-%d")
        },
        "por_canal": by_canal
    }


@router.get("/by-nicho")
async def analytics_by_nicho(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """
    Analytics por nicho
    
    Args:
        start_date: Data início
        end_date: Data fim
        db: Sessão do banco
        
    Returns:
        Métricas por nicho
    """
    if not start_date:
        start = datetime.now() - timedelta(days=7)
    else:
        start = datetime.fromisoformat(start_date)
    
    if not end_date:
        end = datetime.now()
    else:
        end = datetime.fromisoformat(end_date)
    
    analytics = repository.AnalyticsRepository.buscar_por_periodo(
        db, start, end
    )
    
    # Agrupa por nicho
    by_nicho = {}
    for a in analytics:
        nicho = a.nicho or "unknown"
        
        if nicho not in by_nicho:
            by_nicho[nicho] = {
                "cliques": 0,
                "conversoes": 0,
                "receita": 0.0,
                "comissao": 0.0
            }
        
        by_nicho[nicho]["cliques"] += a.cliques
        by_nicho[nicho]["conversoes"] += a.conversoes
        by_nicho[nicho]["receita"] += a.receita
        by_nicho[nicho]["comissao"] += a.comissao
    
    return {
        "periodo": {
            "inicio": start.strftime("%Y-%m-%d"),
            "fim": end.strftime("%Y-%m-%d")
        },
        "por_nicho": by_nicho
    }


@router.get("/metrics")
async def calculate_metrics(
    impressions: int = 0,
    clicks: int = 0,
    conversions: int = 0,
    revenue: float = 0.0,
    cost: float = 0.0
):
    """
    Calcula métricas a partir de dados brutos
    
    Args:
        impressions: Impressões
        clicks: Cliques
        conversions: Conversões
        revenue: Receita
        cost: Custo
        
    Returns:
        Métricas calculadas
    """
    data = {
        "impressions": impressions,
        "clicks": clicks,
        "conversions": conversions,
        "revenue": revenue,
        "cost": cost
    }
    
    metrics = metrics_calculator.generate_summary_metrics(data)
    
    return {
        "input": data,
        "metrics": metrics
    }
