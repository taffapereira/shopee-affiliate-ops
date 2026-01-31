"""
Construtor de SubIds para rastreamento de links
"""
from datetime import datetime
from typing import List
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SubIdBuilder:
    """
    Constrói SubIds estruturados para rastreamento de conversões
    
    Estrutura:
    - subId1 = canal (tiktok|reels|stories|grupo)
    - subId2 = nicho (casa|tech|pet|cosmeticos)
    - subId3 = formato (video15s|video30s|texto|stories|carrossel)
    - subId4 = campanha (oferta_dia|top_comissao|achado|flash)
    - subId5 = data (AAAAMMDD)
    """
    
    @staticmethod
    def build(
        canal: str,
        nicho: str,
        formato: str,
        campanha: str,
        data: datetime = None
    ) -> List[str]:
        """
        Constrói lista de 5 SubIds
        
        Args:
            canal: Nome do canal (tiktok, reels, stories, grupo)
            nicho: Nome do nicho (casa, tech, pet, cosmeticos)
            formato: Formato do conteúdo (video15s, video30s, texto, etc)
            campanha: Tipo de campanha (oferta_dia, top_comissao, achado, flash)
            data: Data do link (padrão: hoje)
            
        Returns:
            Lista com 5 SubIds
            
        Exemplo:
            >>> builder = SubIdBuilder()
            >>> sub_ids = builder.build("tiktok", "tech", "video30s", "oferta_dia")
            >>> # ['tiktok', 'tech', 'video30s', 'oferta_dia', '20260131']
        """
        if data is None:
            data = datetime.now()
        
        data_str = data.strftime("%Y%m%d")
        
        sub_ids = [
            canal,
            nicho,
            formato,
            campanha,
            data_str
        ]
        
        logger.debug("SubIds construídos", sub_ids=sub_ids)
        
        return sub_ids
    
    @staticmethod
    def parse(sub_ids: List[str]) -> dict:
        """
        Faz parsing de SubIds para extrair informações
        
        Args:
            sub_ids: Lista de 5 SubIds
            
        Returns:
            Dict com informações parseadas
        """
        if len(sub_ids) < 5:
            logger.warning("SubIds incompletos", sub_ids=sub_ids)
            return {}
        
        try:
            data_str = sub_ids[4]
            data = datetime.strptime(data_str, "%Y%m%d")
        except (ValueError, IndexError):
            data = None
        
        return {
            "canal": sub_ids[0],
            "nicho": sub_ids[1],
            "formato": sub_ids[2],
            "campanha": sub_ids[3],
            "data": data,
            "data_str": sub_ids[4] if len(sub_ids) > 4 else None
        }
    
    @staticmethod
    def generate_link_id(sub_ids: List[str]) -> str:
        """
        Gera um ID único para o link baseado nos SubIds
        
        Args:
            sub_ids: Lista de SubIds
            
        Returns:
            String ID único
        """
        return "_".join(sub_ids)
