"""
Parser e normalização de ofertas da Shopee
"""
from typing import Dict, Optional
from datetime import datetime

from config.constants import NICHOS
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OfferParser:
    """
    Parser para normalizar dados de ofertas da API Shopee
    """
    
    @staticmethod
    def parse_offer(raw_offer: Dict, nicho: str) -> Optional[Dict]:
        """
        Converte oferta raw da API Shopee para formato do nosso banco
        
        Args:
            raw_offer: Dados raw da API Shopee
            nicho: Nicho do produto (casa, tech, pet, cosmeticos)
            
        Returns:
            Dict com dados normalizados ou None se inválido
        """
        try:
            # Extrai dados básicos
            item_id = raw_offer.get("item_id")
            shop_id = raw_offer.get("shop_id")
            
            if not item_id or not shop_id:
                logger.warning("Oferta sem item_id ou shop_id")
                return None
            
            # Preços
            preco_original = raw_offer.get("price_max", 0) / 100000  # Shopee usa centavos * 1000
            preco_promocional = raw_offer.get("price_min", 0) / 100000
            
            # Calcula desconto
            desconto_percentual = 0.0
            if preco_original > 0 and preco_promocional < preco_original:
                desconto_percentual = ((preco_original - preco_promocional) / preco_original) * 100
            
            # Comissão
            comissao_percentual = raw_offer.get("commission_rate", 0) / 100  # Vem em centésimos
            comissao_valor = (preco_promocional or preco_original) * (comissao_percentual / 100)
            
            # Métricas
            rating = raw_offer.get("item_rating", {}).get("rating_star", 0.0)
            total_vendas = raw_offer.get("item_sold", 0)
            total_avaliacoes = raw_offer.get("item_rating", {}).get("rating_count", [0])[0]
            
            # URLs e imagens
            url_produto = raw_offer.get("product_link", "")
            imagem_url = raw_offer.get("image", "")
            imagens_adicionais = raw_offer.get("images", [])
            
            # Monta produto normalizado
            produto = {
                "shopee_id": f"{shop_id}_{item_id}",
                "nome": raw_offer.get("product_name", "Produto sem nome"),
                "descricao": raw_offer.get("product_description", ""),
                "preco_original": preco_original,
                "preco_promocional": preco_promocional if preco_promocional > 0 else None,
                "desconto_percentual": desconto_percentual if desconto_percentual > 0 else None,
                "comissao_percentual": comissao_percentual,
                "comissao_valor": comissao_valor,
                "rating": rating,
                "total_vendas": total_vendas,
                "total_avaliacoes": total_avaliacoes,
                "nicho": nicho,
                "categoria_shopee": raw_offer.get("category_name", ""),
                "url_produto": url_produto,
                "imagem_url": imagem_url,
                "imagens_adicionais": imagens_adicionais,
                "ativo": True,
                "ja_publicado": False,
            }
            
            logger.debug("Oferta parseada com sucesso", shopee_id=produto["shopee_id"])
            return produto
            
        except Exception as e:
            logger.error(f"Erro ao parsear oferta: {e}", raw_offer=raw_offer)
            return None
    
    @staticmethod
    def validar_produto(produto: Dict) -> tuple[bool, str]:
        """
        Valida se um produto atende aos critérios mínimos
        
        Args:
            produto: Dados do produto
            
        Returns:
            Tuple (é_válido, motivo)
        """
        # Preço mínimo
        preco = produto.get("preco_promocional") or produto.get("preco_original", 0)
        if preco < 10:
            return False, "Preço muito baixo (< R$ 10)"
        
        # Comissão mínima
        if produto.get("comissao_percentual", 0) < 2:
            return False, "Comissão muito baixa (< 2%)"
        
        # Rating mínimo
        if produto.get("rating", 0) < 3.5:
            return False, "Rating muito baixo (< 3.5)"
        
        # Número mínimo de avaliações
        if produto.get("total_avaliacoes", 0) < 10:
            return False, "Poucas avaliações (< 10)"
        
        # Tem imagem
        if not produto.get("imagem_url"):
            return False, "Produto sem imagem"
        
        return True, "Produto válido"
    
    @staticmethod
    def enriquecer_com_nicho(produto: Dict, nicho: str) -> Dict:
        """
        Adiciona informações do nicho ao produto
        
        Args:
            produto: Dados do produto
            nicho: Nome do nicho
            
        Returns:
            Produto enriquecido
        """
        nicho_config = NICHOS.get(nicho, {})
        
        produto["nicho_nome"] = nicho_config.get("nome", nicho)
        produto["persona"] = nicho_config.get("persona", "")
        produto["palavras_chave"] = nicho_config.get("palavras_chave", [])
        
        return produto
    
    @staticmethod
    def calcular_metricas_adicionais(produto: Dict) -> Dict:
        """
        Calcula métricas adicionais para o produto
        
        Args:
            produto: Dados do produto
            
        Returns:
            Produto com métricas adicionais
        """
        # Taxa de conversão estimada (baseado em rating e vendas)
        rating = produto.get("rating", 0)
        vendas = produto.get("total_vendas", 0)
        
        # Fórmula simplificada de estimativa de conversão
        if vendas > 0 and rating > 0:
            produto["taxa_conversao_estimada"] = min((rating / 5) * (vendas / 1000), 1.0)
        else:
            produto["taxa_conversao_estimada"] = 0.0
        
        # Potencial de receita (comissão * vendas estimadas)
        comissao = produto.get("comissao_valor", 0)
        produto["potencial_receita_mensal"] = comissao * min(vendas, 100)  # Cap em 100 vendas/mês
        
        return produto
