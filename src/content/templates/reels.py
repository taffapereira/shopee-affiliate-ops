"""
Templates para Instagram Reels (similar ao TikTok)
"""
from src.content.templates.tiktok import (
    TikTokTemplate,
    ProblemasolucaoTemplate,
    UnboxingRapidoTemplate,
    AntesDopoisTemplate,
    ReviewHonestoTemplate
)


class ReelsTemplate(TikTokTemplate):
    """Template base para Reels - herda de TikTok com adaptações"""
    pass


# Reels usam os mesmos templates do TikTok com duração estendida
REELS_TEMPLATES = {
    "problema_solucao": ProblemasolucaoTemplate(),
    "unboxing_rapido": UnboxingRapidoTemplate(),
    "antes_depois": AntesDopoisTemplate(),
    "review_honesto": ReviewHonestoTemplate(),
    # Reels podem ter até 90s
}


def get_reels_template(nome: str) -> ReelsTemplate:
    """Retorna template Reels pelo nome"""
    return REELS_TEMPLATES.get(nome, ProblemasolucaoTemplate())
