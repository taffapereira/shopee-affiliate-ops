"""
Seletor de produtos top ranqueados
"""
from typing import List, Dict
from src.ranking.scorer import ProductScorer
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProductSelector:
    """
    Seleciona os melhores produtos baseado em score
    """
    
    def __init__(self):
        self.scorer = ProductScorer()
    
    def selecionar_top_n(
        self,
        produtos: List[Dict],
        n: int = 10,
        filtros: Dict = None
    ) -> List[Dict]:
        """
        Seleciona os top N produtos
        
        Args:
            produtos: Lista de produtos
            n: Número de produtos a selecionar
            filtros: Filtros opcionais (ex: {"preco_max": 200})
            
        Returns:
            Lista dos top N produtos ordenados por score
        """
        if not produtos:
            logger.warning("Lista de produtos vazia")
            return []
        
        # Aplica filtros se existirem
        produtos_filtrados = produtos
        if filtros:
            produtos_filtrados = self._aplicar_filtros(produtos, filtros)
        
        # Calcula scores para todos os produtos
        produtos_com_score = []
        for produto in produtos_filtrados:
            score, explicacao = self.scorer.calcular_score(produto)
            produto_scored = produto.copy()
            produto_scored["score_calculado"] = score
            produto_scored["explicacao_score"] = explicacao
            produtos_com_score.append(produto_scored)
        
        # Ordena por score (maior primeiro)
        produtos_ordenados = sorted(
            produtos_com_score,
            key=lambda p: p["score_calculado"],
            reverse=True
        )
        
        # Retorna top N
        top_n = produtos_ordenados[:n]
        
        logger.info(
            "Produtos selecionados",
            total_analisados=len(produtos),
            total_selecionados=len(top_n),
            score_max=top_n[0]["score_calculado"] if top_n else 0,
            score_min=top_n[-1]["score_calculado"] if top_n else 0
        )
        
        return top_n
    
    def _aplicar_filtros(self, produtos: List[Dict], filtros: Dict) -> List[Dict]:
        """
        Aplica filtros aos produtos
        
        Args:
            produtos: Lista de produtos
            filtros: Dicionário de filtros
            
        Returns:
            Produtos filtrados
        """
        produtos_filtrados = produtos.copy()
        
        # Filtro de preço máximo
        if "preco_max" in filtros:
            produtos_filtrados = [
                p for p in produtos_filtrados
                if (p.get("preco_promocional") or p.get("preco_original", 0)) <= filtros["preco_max"]
            ]
        
        # Filtro de preço mínimo
        if "preco_min" in filtros:
            produtos_filtrados = [
                p for p in produtos_filtrados
                if (p.get("preco_promocional") or p.get("preco_original", 0)) >= filtros["preco_min"]
            ]
        
        # Filtro de rating mínimo
        if "rating_min" in filtros:
            produtos_filtrados = [
                p for p in produtos_filtrados
                if p.get("rating", 0) >= filtros["rating_min"]
            ]
        
        # Filtro de comissão mínima
        if "comissao_min" in filtros:
            produtos_filtrados = [
                p for p in produtos_filtrados
                if p.get("comissao_percentual", 0) >= filtros["comissao_min"]
            ]
        
        logger.debug(
            "Filtros aplicados",
            total_antes=len(produtos),
            total_depois=len(produtos_filtrados)
        )
        
        return produtos_filtrados
    
    def agrupar_por_faixa_preco(self, produtos: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Agrupa produtos por faixa de preço
        
        Args:
            produtos: Lista de produtos
            
        Returns:
            Dict com produtos agrupados por faixa
        """
        faixas = {
            "ate_50": [],
            "50_100": [],
            "100_200": [],
            "acima_200": []
        }
        
        for produto in produtos:
            preco = produto.get("preco_promocional") or produto.get("preco_original", 0)
            
            if preco <= 50:
                faixas["ate_50"].append(produto)
            elif preco <= 100:
                faixas["50_100"].append(produto)
            elif preco <= 200:
                faixas["100_200"].append(produto)
            else:
                faixas["acima_200"].append(produto)
        
        return faixas
    
    def diversificar_selecao(
        self,
        produtos: List[Dict],
        n: int = 10
    ) -> List[Dict]:
        """
        Seleciona produtos diversificados (diferentes faixas de preço)
        
        Args:
            produtos: Lista de produtos
            n: Número total de produtos a selecionar
            
        Returns:
            Lista diversificada de produtos
        """
        # Agrupa por faixa de preço
        por_faixa = self.agrupar_por_faixa_preco(produtos)
        
        # Distribui seleção entre faixas
        produtos_por_faixa = n // 4  # Divide igualmente
        resto = n % 4
        
        selecionados = []
        
        for i, (faixa, produtos_faixa) in enumerate(por_faixa.items()):
            # Adiciona 1 extra para as primeiras faixas se houver resto
            quantidade = produtos_por_faixa + (1 if i < resto else 0)
            
            # Seleciona top da faixa
            top_faixa = self.selecionar_top_n(produtos_faixa, quantidade)
            selecionados.extend(top_faixa)
        
        # Ordena resultado final por score
        selecionados_ordenados = sorted(
            selecionados,
            key=lambda p: p.get("score_calculado", 0),
            reverse=True
        )
        
        logger.info("Seleção diversificada realizada", total=len(selecionados_ordenados))
        
        return selecionados_ordenados[:n]
