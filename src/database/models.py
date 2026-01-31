"""
Modelos do banco de dados - SQLAlchemy Models
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.database.connection import Base


class Produto(Base):
    """
    Modelo de Produto coletado da API Shopee
    """
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Dados do produto
    shopee_id = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    preco_original = Column(Float, nullable=False)
    preco_promocional = Column(Float, nullable=True)
    desconto_percentual = Column(Float, nullable=True)
    
    # Comissão
    comissao_percentual = Column(Float, nullable=False)
    comissao_valor = Column(Float, nullable=False)
    
    # Métricas
    rating = Column(Float, default=0.0)
    total_vendas = Column(Integer, default=0)
    total_avaliacoes = Column(Integer, default=0)
    
    # Categorização
    nicho = Column(String, index=True, nullable=False)  # casa, tech, pet, cosmeticos
    categoria_shopee = Column(String, nullable=True)
    
    # URLs e Imagens
    url_produto = Column(String, nullable=False)
    imagem_url = Column(String, nullable=True)
    imagens_adicionais = Column(JSON, nullable=True)  # Lista de URLs
    
    # Ranking
    score_ranking = Column(Float, default=0.0, index=True)
    motivo_ranking = Column(Text, nullable=True)  # Explicação do DeepSeek
    
    # Status
    ativo = Column(Boolean, default=True)
    ja_publicado = Column(Boolean, default=False)
    
    # Timestamps
    coletado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    conteudos = relationship("ConteudoGerado", back_populates="produto")
    links = relationship("Link", back_populates="produto")
    analytics = relationship("Analytics", back_populates="produto")
    
    def __repr__(self):
        return f"<Produto {self.shopee_id}: {self.nome}>"


class ConteudoGerado(Base):
    """
    Modelo de Conteúdo gerado para um produto
    """
    __tablename__ = "conteudos_gerados"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamento com produto
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    
    # Tipo de conteúdo
    canal = Column(String, nullable=False)  # tiktok, reels, stories, grupo
    formato = Column(String, nullable=False)  # video15s, video30s, texto, etc
    persona = Column(String, nullable=False)  # Cléo, Léo, Pri, Tati
    template = Column(String, nullable=False)  # problema_solucao, unboxing, etc
    
    # Conteúdo gerado
    titulo = Column(String, nullable=True)
    copy_texto = Column(Text, nullable=False)
    hashtags = Column(String, nullable=True)
    cta = Column(String, nullable=True)  # Call to action
    
    # Vídeo (se aplicável)
    roteiro_video = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)  # URL no R2
    duracao_segundos = Column(Integer, nullable=True)
    
    # Metadata
    variacao_numero = Column(Integer, default=1)  # 1 a 5
    aprovado = Column(Boolean, default=False)
    publicado = Column(Boolean, default=False)
    
    # Timestamps
    gerado_em = Column(DateTime, default=datetime.utcnow)
    publicado_em = Column(DateTime, nullable=True)
    
    # Relacionamentos
    produto = relationship("Produto", back_populates="conteudos")
    
    def __repr__(self):
        return f"<Conteudo {self.canal}/{self.template} - Produto {self.produto_id}>"


class Link(Base):
    """
    Modelo de Link de afiliado gerado
    """
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamento com produto
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    
    # Link
    link_curto = Column(String, unique=True, index=True, nullable=False)
    link_completo = Column(String, nullable=False)
    
    # SubIds para rastreamento
    sub_id1 = Column(String, nullable=False)  # canal
    sub_id2 = Column(String, nullable=False)  # nicho
    sub_id3 = Column(String, nullable=False)  # formato
    sub_id4 = Column(String, nullable=False)  # campanha
    sub_id5 = Column(String, nullable=False)  # data AAAAMMDD
    
    # Métricas
    total_cliques = Column(Integer, default=0)
    total_conversoes = Column(Integer, default=0)
    receita_gerada = Column(Float, default=0.0)
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)
    ultimo_clique_em = Column(DateTime, nullable=True)
    
    # Relacionamentos
    produto = relationship("Produto", back_populates="links")
    
    def __repr__(self):
        return f"<Link {self.link_curto} - Produto {self.produto_id}>"


class Analytics(Base):
    """
    Modelo de Analytics - métricas de performance
    """
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamento com produto (opcional)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=True)
    
    # Período
    data = Column(DateTime, nullable=False, index=True)
    
    # Dimensões
    canal = Column(String, nullable=True)
    nicho = Column(String, nullable=True)
    campanha = Column(String, nullable=True)
    
    # Métricas
    impressoes = Column(Integer, default=0)
    cliques = Column(Integer, default=0)
    conversoes = Column(Integer, default=0)
    receita = Column(Float, default=0.0)
    comissao = Column(Float, default=0.0)
    
    # CTR e taxa de conversão
    ctr = Column(Float, default=0.0)  # Click-through rate
    taxa_conversao = Column(Float, default=0.0)
    
    # Timestamps
    coletado_em = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    produto = relationship("Produto", back_populates="analytics")
    
    def __repr__(self):
        return f"<Analytics {self.data} - Canal: {self.canal}>"
