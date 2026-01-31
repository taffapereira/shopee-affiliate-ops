"""
Rotas de Conteúdo - Geração de conteúdo
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from src.database.connection import get_db
from src.database import repository
from src.content.generator import ContentGenerator
from src.llm.router import llm_router, LLMTask
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/generate/{produto_id}")
async def generate_content(
    produto_id: int,
    canal: str,
    template: Optional[str] = None,
    num_variacoes: int = 5,
    db: Session = Depends(get_db)
):
    """
    Gera conteúdo para um produto
    
    Args:
        produto_id: ID do produto
        canal: Canal de publicação (tiktok, reels, stories, grupo)
        template: Template específico (opcional)
        num_variacoes: Número de variações
        db: Sessão do banco
        
    Returns:
        Conteúdos gerados
    """
    from src.database.models import Produto
    
    # Busca produto
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Converte para dict
    produto_dict = {
        "id": produto.id,
        "nome": produto.nome,
        "preco_original": produto.preco_original,
        "preco_promocional": produto.preco_promocional,
        "desconto_percentual": produto.desconto_percentual,
        "nicho": produto.nicho,
        "rating": produto.rating,
        "total_vendas": produto.total_vendas,
        "imagem_url": produto.imagem_url,
        "url_produto": produto.url_produto
    }
    
    # Gera conteúdo
    generator = ContentGenerator()
    
    try:
        if num_variacoes > 1:
            conteudos = generator.generate_variacoes(
                canal=canal,
                produto=produto_dict,
                num_variacoes=num_variacoes
            )
        else:
            conteudo = generator.generate_for_canal(
                canal=canal,
                produto=produto_dict,
                template_nome=template
            )
            conteudos = [conteudo]
        
        # Para conteúdos que precisam LLM (TikTok, Reels)
        if canal in ['tiktok', 'reels']:
            for conteudo in conteudos:
                if 'prompt_llm' in conteudo:
                    # Gera copy usando GPT
                    result = await llm_router.execute(
                        LLMTask.COPYWRITING,
                        prompt=conteudo['prompt_llm']
                    )
                    conteudo['copy_gerada'] = result.get('copy') if result else None
        
        # Salva conteúdos no banco
        conteudos_salvos = []
        for conteudo in conteudos:
            conteudo_data = {
                "produto_id": produto_id,
                "canal": conteudo.get('canal'),
                "formato": conteudo.get('formato'),
                "persona": conteudo.get('persona'),
                "template": conteudo.get('template'),
                "copy_texto": conteudo.get('copy_gerada') or conteudo.get('copy_texto', ''),
                "variacao_numero": conteudo.get('variacao_numero', 1),
                "aprovado": False
            }
            
            conteudo_obj = repository.ConteudoRepository.criar(db, conteudo_data)
            conteudos_salvos.append(conteudo_obj)
        
        logger.info(
            f"Gerados {len(conteudos_salvos)} conteúdos",
            produto_id=produto_id,
            canal=canal
        )
        
        return {
            "total": len(conteudos_salvos),
            "canal": canal,
            "conteudos": [
                {
                    "id": c.id,
                    "template": c.template,
                    "persona": c.persona,
                    "variacao": c.variacao_numero
                }
                for c in conteudos_salvos
            ]
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar conteúdo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conteudo_id}")
async def get_content(
    conteudo_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca conteúdo gerado
    
    Args:
        conteudo_id: ID do conteúdo
        db: Sessão do banco
        
    Returns:
        Detalhes do conteúdo
    """
    from src.database.models import ConteudoGerado
    
    conteudo = db.query(ConteudoGerado).filter(
        ConteudoGerado.id == conteudo_id
    ).first()
    
    if not conteudo:
        raise HTTPException(status_code=404, detail="Conteúdo não encontrado")
    
    return {
        "id": conteudo.id,
        "produto_id": conteudo.produto_id,
        "canal": conteudo.canal,
        "formato": conteudo.formato,
        "persona": conteudo.persona,
        "template": conteudo.template,
        "copy_texto": conteudo.copy_texto,
        "hashtags": conteudo.hashtags,
        "variacao": conteudo.variacao_numero,
        "aprovado": conteudo.aprovado,
        "publicado": conteudo.publicado
    }


@router.post("/{conteudo_id}/approve")
async def approve_content(
    conteudo_id: int,
    db: Session = Depends(get_db)
):
    """
    Aprova conteúdo para publicação
    
    Args:
        conteudo_id: ID do conteúdo
        db: Sessão do banco
        
    Returns:
        Confirmação
    """
    from src.database.models import ConteudoGerado
    
    conteudo = db.query(ConteudoGerado).filter(
        ConteudoGerado.id == conteudo_id
    ).first()
    
    if not conteudo:
        raise HTTPException(status_code=404, detail="Conteúdo não encontrado")
    
    conteudo.aprovado = True
    db.commit()
    
    logger.info("Conteúdo aprovado", conteudo_id=conteudo_id)
    
    return {"message": "Conteúdo aprovado", "id": conteudo_id}
