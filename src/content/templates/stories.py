"""
Templates para Instagram Stories
"""
from typing import Dict


class StoriesTemplate:
    """Template base para Stories"""
    
    def __init__(self, nome: str, descricao: str):
        self.nome = nome
        self.descricao = descricao
    
    def generate(self, produto: Dict, link: str) -> Dict:
        """
        Gera conteúdo para Stories
        
        Args:
            produto: Dados do produto
            link: Link de afiliado
            
        Returns:
            Dict com texto, stickers, etc
        """
        raise NotImplementedError


class ProdutoDescontoTemplate(StoriesTemplate):
    """Template 1: Produto em destaque com desconto"""
    
    def __init__(self):
        super().__init__(
            nome="produto_desconto",
            descricao="Story focado no desconto"
        )
    
    def generate(self, produto: Dict, link: str) -> Dict:
        preco = produto.get('preco_promocional') or produto.get('preco_original', 0)
        desconto = produto.get('desconto_percentual', 0)
        
        return {
            "tipo": "imagem_produto",
            "imagem_url": produto.get('imagem_url'),
            "texto_principal": f"{desconto:.0f}% OFF",
            "texto_secundario": f"R$ {preco:.2f}",
            "sticker_swipe_up": "Arrasta pra cima!",
            "link": link,
            "cor_fundo": "#FF6B6B",
            "duracao": 15
        }


class EnqueteTemplate(StoriesTemplate):
    """Template 2: Enquete interativa"""
    
    def __init__(self):
        super().__init__(
            nome="enquete",
            descricao="Story com enquete de engajamento"
        )
    
    def generate(self, produto: Dict, link: str) -> Dict:
        return {
            "tipo": "enquete",
            "imagem_url": produto.get('imagem_url'),
            "pergunta": f"Vale a pena por R$ {produto.get('preco_promocional') or produto.get('preco_original', 0):.2f}?",
            "opcoes": ["SIM! 😍", "Não sei 🤔"],
            "link": link,
            "texto_cta": "Link nos destaques!",
            "duracao": 15
        }


class AntesDepoisStoriesTemplate(StoriesTemplate):
    """Template 3: Antes/Depois para Stories"""
    
    def __init__(self):
        super().__init__(
            nome="antes_depois_stories",
            descricao="Comparação antes/depois em Story"
        )
    
    def generate(self, produto: Dict, link: str) -> Dict:
        return {
            "tipo": "split_screen",
            "lado_esquerdo": {
                "titulo": "ANTES",
                "descricao": "Situação sem o produto"
            },
            "lado_direito": {
                "titulo": "DEPOIS",
                "descricao": "Com o produto"
            },
            "imagem_url": produto.get('imagem_url'),
            "link": link,
            "texto_cta": "Quer também? Arrasta!",
            "duracao": 15
        }


# Dicionário de templates
STORIES_TEMPLATES = {
    "produto_desconto": ProdutoDescontoTemplate(),
    "enquete": EnqueteTemplate(),
    "antes_depois": AntesDepoisStoriesTemplate(),
}


def get_stories_template(nome: str) -> StoriesTemplate:
    """Retorna template Stories pelo nome"""
    return STORIES_TEMPLATES.get(nome, ProdutoDescontoTemplate())
