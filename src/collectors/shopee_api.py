"""
Cliente da API Shopee Affiliate para coleta de produtos
"""
import hashlib
import hmac
import time
from typing import List, Dict, Optional
import httpx

from config.credentials import credentials
from config.constants import SHOPEE_API_RATE_LIMIT, PRODUTOS_POR_COLETA
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ShopeeAffiliateAPI:
    """
    Cliente para interagir com a Shopee Affiliate API
    
    Documentação: https://open.shopee.com/documents/v2/affiliate
    """
    
    BASE_URL = "https://partner.shopeemobile.com/api/v3/affiliate"
    
    def __init__(self):
        self.partner_id = credentials.SHOPEE_PARTNER_ID
        self.api_key = credentials.SHOPEE_AFFILIATE_API_KEY
        self.secret = credentials.SHOPEE_AFFILIATE_SECRET
        
        if not all([self.partner_id, self.api_key, self.secret]):
            raise ValueError("Credenciais da Shopee não configuradas")
    
    def _generate_signature(self, path: str, timestamp: int, body: str = "") -> str:
        """
        Gera assinatura para autenticação na API Shopee
        
        Args:
            path: Caminho da API (ex: /product/get_offer_list)
            timestamp: Unix timestamp
            body: Corpo da requisição (JSON string)
            
        Returns:
            Assinatura HMAC-SHA256
        """
        base_string = f"{self.partner_id}{path}{timestamp}{body}"
        signature = hmac.new(
            self.secret.encode(),
            base_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    async def get_product_offers(
        self,
        category_id: Optional[int] = None,
        keyword: Optional[str] = None,
        limit: int = PRODUTOS_POR_COLETA
    ) -> List[Dict]:
        """
        Busca ofertas de produtos da Shopee
        
        Args:
            category_id: ID da categoria (opcional)
            keyword: Palavra-chave para busca (opcional)
            limit: Número máximo de produtos
            
        Returns:
            Lista de produtos/ofertas
        """
        path = "/product/get_offer_list"
        timestamp = int(time.time())
        
        # Parâmetros da requisição
        params = {
            "partner_id": self.partner_id,
            "timestamp": timestamp,
            "limit": limit,
        }
        
        if category_id:
            params["category_id"] = category_id
        if keyword:
            params["keyword"] = keyword
        
        # Gera assinatura
        signature = self._generate_signature(path, timestamp)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{self.api_key}:{signature}"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}{path}",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("error"):
                    logger.error(
                        "Erro na API Shopee",
                        error=data.get("message"),
                        code=data.get("error")
                    )
                    return []
                
                products = data.get("data", {}).get("offers", [])
                logger.info(
                    "Produtos coletados da Shopee",
                    total=len(products),
                    category_id=category_id,
                    keyword=keyword
                )
                
                return products
                
        except httpx.HTTPError as e:
            logger.error(f"Erro HTTP ao buscar produtos: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar produtos: {e}")
            return []
    
    async def get_product_detail(self, item_id: str, shop_id: str) -> Optional[Dict]:
        """
        Busca detalhes de um produto específico
        
        Args:
            item_id: ID do item
            shop_id: ID da loja
            
        Returns:
            Detalhes do produto
        """
        path = "/product/get_detail"
        timestamp = int(time.time())
        
        params = {
            "partner_id": self.partner_id,
            "timestamp": timestamp,
            "item_id": item_id,
            "shop_id": shop_id
        }
        
        signature = self._generate_signature(path, timestamp)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{self.api_key}:{signature}"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}{path}",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("error"):
                    logger.error("Erro ao buscar detalhe", item_id=item_id)
                    return None
                
                return data.get("data", {})
                
        except Exception as e:
            logger.error(f"Erro ao buscar detalhe do produto: {e}")
            return None
    
    async def generate_affiliate_link(
        self,
        item_id: str,
        shop_id: str,
        sub_ids: List[str]
    ) -> Optional[str]:
        """
        Gera link de afiliado para um produto
        
        Args:
            item_id: ID do item
            shop_id: ID da loja
            sub_ids: Lista de 5 sub_ids para tracking
            
        Returns:
            Link de afiliado ou None
        """
        path = "/link/generate"
        timestamp = int(time.time())
        
        body = {
            "partner_id": self.partner_id,
            "timestamp": timestamp,
            "item_id": item_id,
            "shop_id": shop_id,
            "sub_id1": sub_ids[0] if len(sub_ids) > 0 else "",
            "sub_id2": sub_ids[1] if len(sub_ids) > 1 else "",
            "sub_id3": sub_ids[2] if len(sub_ids) > 2 else "",
            "sub_id4": sub_ids[3] if len(sub_ids) > 3 else "",
            "sub_id5": sub_ids[4] if len(sub_ids) > 4 else "",
        }
        
        import json
        body_str = json.dumps(body)
        signature = self._generate_signature(path, timestamp, body_str)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{self.api_key}:{signature}"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}{path}",
                    json=body,
                    headers=headers
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("error"):
                    logger.error("Erro ao gerar link", item_id=item_id)
                    return None
                
                link = data.get("data", {}).get("affiliate_link")
                logger.info("Link de afiliado gerado", item_id=item_id)
                
                return link
                
        except Exception as e:
            logger.error(f"Erro ao gerar link de afiliado: {e}")
            return None
