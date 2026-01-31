"""
Rotas de Links - Geração de links de afiliado
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database import repository
from src.links.shortener import LinkShortener
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/generate/{produto_id}")
async def generate_link(
    produto_id: int,
    canal: str,
    formato: str,
    campanha: str = "oferta_dia",
    db: Session = Depends(get_db)
):
    """
    Gera link de afiliado para produto
    
    Args:
        produto_id: ID do produto
        canal: Canal (tiktok, reels, stories, grupo)
        formato: Formato do conteúdo
        campanha: Tipo de campanha
        db: Sessão do banco
        
    Returns:
        Link gerado
    """
    from src.database.models import Produto
    
    # Busca produto
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    try:
        # Extrai IDs da Shopee (formato: shop_id_item_id)
        parts = produto.shopee_id.split("_")
        if len(parts) < 2:
            raise ValueError("shopee_id inválido")
        
        shop_id = parts[0]
        item_id = "_".join(parts[1:])
        
        # Gera link
        shortener = LinkShortener()
        link_data = await shortener.generate_short_link(
            item_id=item_id,
            shop_id=shop_id,
            canal=canal,
            nicho=produto.nicho,
            formato=formato,
            campanha=campanha
        )
        
        if not link_data:
            raise HTTPException(
                status_code=500,
                detail="Erro ao gerar link de afiliado"
            )
        
        # Salva no banco
        link_data["produto_id"] = produto_id
        link = repository.LinkRepository.criar(db, link_data)
        
        logger.info("Link gerado", produto_id=produto_id, link_id=link.id)
        
        return {
            "link_id": link.id,
            "link_curto": link.link_curto,
            "link_completo": link.link_completo,
            "produto_id": produto_id,
            "canal": canal,
            "tracking": {
                "sub_id1": link.sub_id1,
                "sub_id2": link.sub_id2,
                "sub_id3": link.sub_id3,
                "sub_id4": link.sub_id4,
                "sub_id5": link.sub_id5
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar link: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{link_id}")
async def get_link(
    link_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca link por ID
    
    Args:
        link_id: ID do link
        db: Sessão do banco
        
    Returns:
        Detalhes do link
    """
    from src.database.models import Link
    
    link = db.query(Link).filter(Link.id == link_id).first()
    
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")
    
    return {
        "id": link.id,
        "link_curto": link.link_curto,
        "link_completo": link.link_completo,
        "produto_id": link.produto_id,
        "tracking": {
            "canal": link.sub_id1,
            "nicho": link.sub_id2,
            "formato": link.sub_id3,
            "campanha": link.sub_id4,
            "data": link.sub_id5
        },
        "metricas": {
            "cliques": link.total_cliques,
            "conversoes": link.total_conversoes,
            "receita": link.receita_gerada
        },
        "criado_em": link.criado_em.isoformat()
    }
