"""
Algoritmo de pontuação de produtos
"""
from typing import Dict
from config.constants import (
    PESO_COMISSAO,
    PESO_PRECO,
    PESO_RATING,
    PESO_VENDAS,
    PESO_DESCONTO
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProductScorer:
    """
    Calcula score de produtos baseado em múltiplos fatores
    """
    
    def __init__(self):
        self.peso_comissao = PESO_COMISSAO
        self.peso_preco = PESO_PRECO
        self.peso_rating = PESO_RATING
        self.peso_vendas = PESO_VENDAS
        self.peso_desconto = PESO_DESCONTO
    
    def calcular_score(self, produto: Dict) -> tuple[float, str]:
        """
        Calcula score de 0 a 100 para um produto
        
        Args:
            produto: Dados do produto
            
        Returns:
            Tuple (score, explicação)
        """
        scores_parciais = {}
        
        # 1. Score de Comissão (0-100)
        comissao_pct = produto.get("comissao_percentual", 0)
        score_comissao = min(comissao_pct * 5, 100)  # 20% = score 100
        scores_parciais["comissao"] = score_comissao
        
        # 2. Score de Preço (produtos entre R$50-200 são ideais)
        preco = produto.get("preco_promocional") or produto.get("preco_original", 0)
        if 50 <= preco <= 200:
            score_preco = 100
        elif preco < 50:
            score_preco = (preco / 50) * 100
        else:  # preco > 200
            score_preco = max(100 - ((preco - 200) / 10), 0)
        scores_parciais["preco"] = score_preco
        
        # 3. Score de Rating (0-5 -> 0-100)
        rating = produto.get("rating", 0)
        score_rating = (rating / 5) * 100
        scores_parciais["rating"] = score_rating
        
        # 4. Score de Vendas (normalizado)
        vendas = produto.get("total_vendas", 0)
        # Vendas > 1000 = score 100
        score_vendas = min((vendas / 1000) * 100, 100)
        scores_parciais["vendas"] = score_vendas
        
        # 5. Score de Desconto (0-100)
        desconto = produto.get("desconto_percentual", 0)
        score_desconto = min(desconto * 2, 100)  # 50% desconto = score 100
        scores_parciais["desconto"] = score_desconto
        
        # Calcula score final ponderado
        score_final = (
            scores_parciais["comissao"] * self.peso_comissao +
            scores_parciais["preco"] * self.peso_preco +
            scores_parciais["rating"] * self.peso_rating +
            scores_parciais["vendas"] * self.peso_vendas +
            scores_parciais["desconto"] * self.peso_desconto
        )
        
        # Gera explicação
        explicacao = self._gerar_explicacao(scores_parciais, score_final)
        
        logger.debug(
            "Score calculado",
            produto_id=produto.get("shopee_id"),
            score=round(score_final, 2)
        )
        
        return round(score_final, 2), explicacao
    
    def _gerar_explicacao(self, scores: Dict[str, float], score_final: float) -> str:
        """
        Gera explicação textual do score
        
        Args:
            scores: Scores parciais
            score_final: Score final
            
        Returns:
            Texto explicativo
        """
        explicacao_partes = []
        
        # Destaca os pontos fortes
        if scores["comissao"] >= 80:
            explicacao_partes.append("excelente comissão")
        if scores["rating"] >= 90:
            explicacao_partes.append("altamente avaliado")
        if scores["vendas"] >= 70:
            explicacao_partes.append("muitas vendas")
        if scores["desconto"] >= 60:
            explicacao_partes.append("bom desconto")
        
        # Destaca pontos fracos
        if scores["comissao"] < 40:
            explicacao_partes.append("comissão baixa")
        if scores["rating"] < 60:
            explicacao_partes.append("rating mediano")
        
        if explicacao_partes:
            explicacao = "Score {:.1f}/100: {}".format(
                score_final,
                ", ".join(explicacao_partes)
            )
        else:
            explicacao = "Score {:.1f}/100: produto balanceado".format(score_final)
        
        return explicacao
    
    def comparar_produtos(self, produto_a: Dict, produto_b: Dict) -> int:
        """
        Compara dois produtos
        
        Args:
            produto_a: Primeiro produto
            produto_b: Segundo produto
            
        Returns:
            1 se A > B, -1 se A < B, 0 se iguais
        """
        score_a, _ = self.calcular_score(produto_a)
        score_b, _ = self.calcular_score(produto_b)
        
        if score_a > score_b:
            return 1
        elif score_a < score_b:
            return -1
        return 0
