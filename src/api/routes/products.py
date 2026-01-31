"""
Rotas de Produtos - CRUD e coleta
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.connection import get_db
from src.database import repository
from src.collectors.shopee_api import ShopeeAffiliateAPI
from src.collectors.offer_parser import OfferParser
from src.ranking.selector import ProductSelector
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/collect")
async def collect_products(
    nicho: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Coleta produtos da API Shopee para um nicho
    
    Args:
        nicho: Nome do nicho (casa, tech, pet, cosmeticos)
        limit: Número máximo de produtos
        db: Sessão do banco
        
    Returns:
        Lista de produtos coletados
    """
    try:
        api = ShopeeAffiliateAPI()
        parser = OfferParser()
        
        # Busca ofertas
        raw_offers = await api.get_product_offers(limit=limit)
        
        produtos_salvos = []
        
        for raw_offer in raw_offers:
            # Parse da oferta
            produto_data = parser.parse_offer(raw_offer, nicho)
            
            if not produto_data:
                continue
            
            # Valida produto
            is_valid, motivo = parser.validar_produto(produto_data)
            if not is_valid:
                logger.debug(f"Produto rejeitado: {motivo}")
                continue
            
            # Verifica se já existe
            existing = repository.ProdutoRepository.buscar_por_shopee_id(
                db,
                produto_data["shopee_id"]
            )
            
            if existing:
                logger.debug(f"Produto já existe: {produto_data['shopee_id']}")
                continue
            
            # Salva no banco
            produto = repository.ProdutoRepository.criar(db, produto_data)
            produtos_salvos.append(produto)
        
        logger.info(f"Coletados {len(produtos_salvos)} produtos", nicho=nicho)
        
        return {
            "total_coletados": len(produtos_salvos),
            "nicho": nicho,
            "produtos": [p.shopee_id for p in produtos_salvos]
        }
        
    except Exception as e:
        logger.error(f"Erro ao coletar produtos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top/{nicho}")
async def get_top_products(
    nicho: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retorna top N produtos ranqueados de um nicho
    
    Args:
        nicho: Nome do nicho
        limit: Número de produtos
        db: Sessão do banco
        
    Returns:
        Top produtos ranqueados
    """
    produtos = repository.ProdutoRepository.top_ranqueados(db, nicho, limit)
    
    return {
        "nicho": nicho,
        "total": len(produtos),
        "produtos": [
            {
                "id": p.id,
                "nome": p.nome,
                "preco": p.preco_promocional or p.preco_original,
                "comissao": f"{p.comissao_percentual}%",
                "rating": p.rating,
                "score": p.score_ranking
            }
            for p in produtos
        ]
    }


@router.post("/rank")
async def rank_products(
    nicho: str,
    db: Session = Depends(get_db)
):
    """
    Ranqueia produtos de um nicho
    
    Args:
        nicho: Nome do nicho
        db: Sessão do banco
        
    Returns:
        Produtos ranqueados
    """
    from src.ranking.scorer import ProductScorer
    
    # Busca produtos do nicho
    produtos = repository.ProdutoRepository.listar_por_nicho(db, nicho, limit=100)
    
    if not produtos:
        return {"message": "Nenhum produto encontrado", "total": 0}
    
    # Ranqueia
    scorer = ProductScorer()
    
    for produto in produtos:
        produto_dict = {
            "id": produto.id,
            "shopee_id": produto.shopee_id,
            "comissao_percentual": produto.comissao_percentual,
            "preco_original": produto.preco_original,
            "preco_promocional": produto.preco_promocional,
            "desconto_percentual": produto.desconto_percentual,
            "rating": produto.rating,
            "total_vendas": produto.total_vendas
        }
        
        score, motivo = scorer.calcular_score(produto_dict)
        
        # Atualiza score no banco
        repository.ProdutoRepository.atualizar_score(
            db,
            produto.id,
            score,
            motivo
        )
    
    logger.info(f"Ranqueados {len(produtos)} produtos", nicho=nicho)
    
    return {
        "message": "Produtos ranqueados com sucesso",
        "total": len(produtos),
        "nicho": nicho
    }


@router.get("/{produto_id}")
async def get_product(
    produto_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca detalhes de um produto
    
    Args:
        produto_id: ID do produto
        db: Sessão do banco
        
    Returns:
        Detalhes do produto
    """
    from src.database.models import Produto
    
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return {
        "id": produto.id,
        "shopee_id": produto.shopee_id,
        "nome": produto.nome,
        "descricao": produto.descricao,
        "preco_original": produto.preco_original,
        "preco_promocional": produto.preco_promocional,
        "desconto": produto.desconto_percentual,
        "comissao": {
            "percentual": produto.comissao_percentual,
            "valor": produto.comissao_valor
        },
        "rating": produto.rating,
        "total_vendas": produto.total_vendas,
        "nicho": produto.nicho,
        "score_ranking": produto.score_ranking,
        "motivo_ranking": produto.motivo_ranking,
        "url": produto.url_produto,
        "imagem": produto.imagem_url
    }
