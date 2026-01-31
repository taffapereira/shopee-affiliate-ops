"""
Gerador de short links de afiliado
"""
import hashlib
from typing import Optional
from src.collectors.shopee_api import ShopeeAffiliateAPI
from src.links.subid_builder import SubIdBuilder
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LinkShortener:
    """
    Gera e gerencia links curtos de afiliado
    """
    
    def __init__(self):
        self.api = ShopeeAffiliateAPI()
        self.subid_builder = SubIdBuilder()
    
    async def generate_short_link(
        self,
        item_id: str,
        shop_id: str,
        canal: str,
        nicho: str,
        formato: str,
        campanha: str
    ) -> Optional[dict]:
        """
        Gera um link curto de afiliado com tracking
        
        Args:
            item_id: ID do item na Shopee
            shop_id: ID da loja
            canal: Canal de publicação
            nicho: Nicho do produto
            formato: Formato do conteúdo
            campanha: Tipo de campanha
            
        Returns:
            Dict com link_completo, link_curto e sub_ids
        """
        # Constrói SubIds
        sub_ids = self.subid_builder.build(canal, nicho, formato, campanha)
        
        # Gera link via API Shopee
        link_completo = await self.api.generate_affiliate_link(
            item_id=item_id,
            shop_id=shop_id,
            sub_ids=sub_ids
        )
        
        if not link_completo:
            logger.error("Falha ao gerar link", item_id=item_id)
            return None
        
        # Gera hash curto para identificação
        link_hash = self._generate_short_hash(link_completo)
        
        result = {
            "link_completo": link_completo,
            "link_curto": link_hash,
            "sub_id1": sub_ids[0],
            "sub_id2": sub_ids[1],
            "sub_id3": sub_ids[2],
            "sub_id4": sub_ids[3],
            "sub_id5": sub_ids[4],
        }
        
        logger.info(
            "Link gerado com sucesso",
            item_id=item_id,
            link_curto=link_hash,
            canal=canal
        )
        
        return result
    
    def _generate_short_hash(self, url: str, length: int = 8) -> str:
        """
        Gera hash curto para URL
        
        Args:
            url: URL completa
            length: Tamanho do hash
            
        Returns:
            Hash curto
        """
        hash_object = hashlib.md5(url.encode())
        return hash_object.hexdigest()[:length]
    
    def build_tracking_url(self, base_url: str, sub_ids: list) -> str:
        """
        Constrói URL com parâmetros de tracking
        
        Args:
            base_url: URL base do afiliado
            sub_ids: Lista de SubIds
            
        Returns:
            URL completa com tracking
        """
        params = []
        for i, sub_id in enumerate(sub_ids, 1):
            params.append(f"subId{i}={sub_id}")
        
        separator = "&" if "?" in base_url else "?"
        tracking_url = f"{base_url}{separator}{'&'.join(params)}"
        
        return tracking_url
