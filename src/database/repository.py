"""
Repository - CRUD operations para o banco de dados
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from src.database.models import Produto, ConteudoGerado, Link, Analytics
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProdutoRepository:
    """Repository para operações com Produtos"""
    
    @staticmethod
    def criar(db: Session, produto_data: dict) -> Produto:
        """
        Cria um novo produto no banco
        
        Args:
            db: Sessão do banco
            produto_data: Dados do produto
            
        Returns:
            Produto criado
        """
        produto = Produto(**produto_data)
        db.add(produto)
        db.commit()
        db.refresh(produto)
        logger.info("Produto criado", produto_id=produto.id, shopee_id=produto.shopee_id)
        return produto
    
    @staticmethod
    def buscar_por_shopee_id(db: Session, shopee_id: str) -> Optional[Produto]:
        """Busca produto pelo ID da Shopee"""
        return db.query(Produto).filter(Produto.shopee_id == shopee_id).first()
    
    @staticmethod
    def listar_por_nicho(db: Session, nicho: str, limit: int = 50) -> List[Produto]:
        """Lista produtos de um nicho específico"""
        return db.query(Produto).filter(
            and_(Produto.nicho == nicho, Produto.ativo == True)
        ).order_by(desc(Produto.score_ranking)).limit(limit).all()
    
    @staticmethod
    def top_ranqueados(db: Session, nicho: str, limit: int = 10) -> List[Produto]:
        """Retorna top N produtos ranqueados de um nicho"""
        return db.query(Produto).filter(
            and_(Produto.nicho == nicho, Produto.ativo == True)
        ).order_by(desc(Produto.score_ranking)).limit(limit).all()
    
    @staticmethod
    def atualizar_score(db: Session, produto_id: int, score: float, motivo: str):
        """Atualiza o score de ranking de um produto"""
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if produto:
            produto.score_ranking = score
            produto.motivo_ranking = motivo
            produto.atualizado_em = datetime.utcnow()
            db.commit()
            logger.info("Score atualizado", produto_id=produto_id, score=score)
    
    @staticmethod
    def marcar_como_publicado(db: Session, produto_id: int):
        """Marca produto como já publicado"""
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if produto:
            produto.ja_publicado = True
            db.commit()


class ConteudoRepository:
    """Repository para operações com Conteúdos"""
    
    @staticmethod
    def criar(db: Session, conteudo_data: dict) -> ConteudoGerado:
        """Cria novo conteúdo gerado"""
        conteudo = ConteudoGerado(**conteudo_data)
        db.add(conteudo)
        db.commit()
        db.refresh(conteudo)
        logger.info("Conteúdo criado", conteudo_id=conteudo.id, canal=conteudo.canal)
        return conteudo
    
    @staticmethod
    def listar_por_produto(db: Session, produto_id: int) -> List[ConteudoGerado]:
        """Lista todos os conteúdos de um produto"""
        return db.query(ConteudoGerado).filter(
            ConteudoGerado.produto_id == produto_id
        ).all()
    
    @staticmethod
    def buscar_para_publicar(
        db: Session,
        canal: str,
        nicho: str,
        limit: int = 5
    ) -> List[ConteudoGerado]:
        """
        Busca conteúdos prontos para publicação
        """
        return db.query(ConteudoGerado).join(Produto).filter(
            and_(
                ConteudoGerado.canal == canal,
                ConteudoGerado.aprovado == True,
                ConteudoGerado.publicado == False,
                Produto.nicho == nicho
            )
        ).limit(limit).all()
    
    @staticmethod
    def marcar_como_publicado(db: Session, conteudo_id: int):
        """Marca conteúdo como publicado"""
        conteudo = db.query(ConteudoGerado).filter(
            ConteudoGerado.id == conteudo_id
        ).first()
        if conteudo:
            conteudo.publicado = True
            conteudo.publicado_em = datetime.utcnow()
            db.commit()


class LinkRepository:
    """Repository para operações com Links"""
    
    @staticmethod
    def criar(db: Session, link_data: dict) -> Link:
        """Cria novo link de afiliado"""
        link = Link(**link_data)
        db.add(link)
        db.commit()
        db.refresh(link)
        logger.info("Link criado", link_id=link.id, link_curto=link.link_curto)
        return link
    
    @staticmethod
    def buscar_por_link_curto(db: Session, link_curto: str) -> Optional[Link]:
        """Busca link pelo short code"""
        return db.query(Link).filter(Link.link_curto == link_curto).first()
    
    @staticmethod
    def atualizar_metricas(
        db: Session,
        link_id: int,
        cliques: int = 0,
        conversoes: int = 0,
        receita: float = 0.0
    ):
        """Atualiza métricas de um link"""
        link = db.query(Link).filter(Link.id == link_id).first()
        if link:
            link.total_cliques += cliques
            link.total_conversoes += conversoes
            link.receita_gerada += receita
            if cliques > 0:
                link.ultimo_clique_em = datetime.utcnow()
            db.commit()


class AnalyticsRepository:
    """Repository para operações com Analytics"""
    
    @staticmethod
    def criar(db: Session, analytics_data: dict) -> Analytics:
        """Registra analytics"""
        analytics = Analytics(**analytics_data)
        db.add(analytics)
        db.commit()
        db.refresh(analytics)
        return analytics
    
    @staticmethod
    def buscar_por_periodo(
        db: Session,
        data_inicio: datetime,
        data_fim: datetime,
        canal: Optional[str] = None,
        nicho: Optional[str] = None
    ) -> List[Analytics]:
        """Busca analytics em um período"""
        query = db.query(Analytics).filter(
            and_(
                Analytics.data >= data_inicio,
                Analytics.data <= data_fim
            )
        )
        
        if canal:
            query = query.filter(Analytics.canal == canal)
        if nicho:
            query = query.filter(Analytics.nicho == nicho)
        
        return query.all()
    
    @staticmethod
    def resumo_ultimos_dias(db: Session, dias: int = 7) -> dict:
        """Retorna resumo dos últimos N dias"""
        data_inicio = datetime.utcnow() - timedelta(days=dias)
        
        analytics = db.query(Analytics).filter(
            Analytics.data >= data_inicio
        ).all()
        
        return {
            "total_cliques": sum(a.cliques for a in analytics),
            "total_conversoes": sum(a.conversoes for a in analytics),
            "total_receita": sum(a.receita for a in analytics),
            "total_comissao": sum(a.comissao for a in analytics),
            "ctr_medio": sum(a.ctr for a in analytics) / len(analytics) if analytics else 0,
            "taxa_conversao_media": sum(a.taxa_conversao for a in analytics) / len(analytics) if analytics else 0,
        }
