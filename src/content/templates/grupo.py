"""
Templates para Grupo Telegram - 5 tipos
"""
from typing import Dict


class GrupoTemplate:
    """Classe base para templates de Grupo Telegram"""
    
    def __init__(self, nome: str, descricao: str):
        self.nome = nome
        self.descricao = descricao
    
    def generate(self, produto: Dict, link: str) -> str:
        """
        Gera conteúdo para Telegram
        
        Args:
            produto: Dados do produto
            link: Link de afiliado
            
        Returns:
            Mensagem formatada
        """
        raise NotImplementedError


class OfertaCompletaTemplate(GrupoTemplate):
    """Template 1: Oferta Completa com emojis e benefícios"""
    
    def __init__(self):
        super().__init__(
            nome="oferta_completa",
            descricao="Formato completo com emoji, benefícios e link"
        )
    
    def generate(self, produto: Dict, link: str) -> str:
        preco = produto.get('preco_promocional') or produto.get('preco_original', 0)
        desconto = produto.get('desconto_percentual', 0)
        
        # Emoji baseado no nicho
        emoji_map = {
            "casa": "🏠",
            "tech": "📱",
            "pet": "🐾",
            "cosmeticos": "💄"
        }
        emoji = emoji_map.get(produto.get('nicho'), "⭐")
        
        message = f"""{emoji} **{produto.get('nome')}**

💰 R$ {preco:.2f}"""
        
        if desconto > 0:
            preco_original = produto.get('preco_original', 0)
            message += f""" ~~R$ {preco_original:.2f}~~
🔥 {desconto:.0f}% OFF"""
        
        message += f"""

✅ Rating: {produto.get('rating', 0):.1f}⭐ ({produto.get('total_avaliacoes', 0)} avaliações)
✅ {produto.get('total_vendas', 0)} vendas

🔗 {link}

{DISCLAIMER}"""
        
        return message


class UrgenteTemplate(GrupoTemplate):
    """Template 2: URGENTE com preço riscado"""
    
    def __init__(self):
        super().__init__(
            nome="urgente",
            descricao="Formato urgente com senso de escassez"
        )
    
    def generate(self, produto: Dict, link: str) -> str:
        preco = produto.get('preco_promocional') or produto.get('preco_original', 0)
        preco_original = produto.get('preco_original', 0)
        desconto = produto.get('desconto_percentual', 0)
        
        message = f"""🚨 CORRE! PROMOÇÃO RELÂMPAGO

{produto.get('nome')}

De: ~~R$ {preco_original:.2f}~~
Por: R$ {preco:.2f} 💥

{desconto:.0f}% DE DESCONTO!

Aproveita antes que acabe! 👇
{link}

{DISCLAIMER}"""
        
        return message


class MinimalistaTemplate(GrupoTemplate):
    """Template 3: Minimalista (produto + preço + link)"""
    
    def __init__(self):
        super().__init__(
            nome="minimalista",
            descricao="Formato clean e direto"
        )
    
    def generate(self, produto: Dict, link: str) -> str:
        preco = produto.get('preco_promocional') or produto.get('preco_original', 0)
        
        message = f"""{produto.get('nome')}
R$ {preco:.2f}
{link}"""
        
        return message


class ComparativoPrecoTemplate(GrupoTemplate):
    """Template 4: Com comparativo de preço"""
    
    def __init__(self):
        super().__init__(
            nome="comparativo_preco",
            descricao="Mostra comparação com outros lugares"
        )
    
    def generate(self, produto: Dict, link: str) -> str:
        preco = produto.get('preco_promocional') or produto.get('preco_original', 0)
        preco_original = produto.get('preco_original', 0)
        
        # Simula preço "em outros lugares" (15% a mais)
        preco_outros = preco * 1.15
        
        message = f"""💰 ACHADO DE PREÇO!

{produto.get('nome')}

🏪 Em outros lugares: R$ {preco_outros:.2f}
🛒 Na Shopee: R$ {preco:.2f}

💵 Você economiza: R$ {preco_outros - preco:.2f}

Pega logo! 👇
{link}

{DISCLAIMER}"""
        
        return message


class ListaAchadosTemplate(GrupoTemplate):
    """Template 5: Lista de achados"""
    
    def __init__(self):
        super().__init__(
            nome="lista_achados",
            descricao="Formato de lista para múltiplos produtos"
        )
    
    def generate(self, produto: Dict, link: str) -> str:
        preco = produto.get('preco_promocional') or produto.get('preco_original', 0)
        desconto = produto.get('desconto_percentual', 0)
        
        emoji = "🔥" if desconto > 30 else "✨"
        
        message = f"""{emoji} {produto.get('nome')}
   R$ {preco:.2f}"""
        
        if desconto > 0:
            message += f" ({desconto:.0f}% OFF)"
        
        message += f"""
   {link}"""
        
        return message


# Disclaimer padrão
DISCLAIMER = "🔗 Link de afiliado | ⚠️ Preço sujeito a alteração"


# Dicionário com todos os templates
GRUPO_TEMPLATES = {
    "oferta_completa": OfertaCompletaTemplate(),
    "urgente": UrgenteTemplate(),
    "minimalista": MinimalistaTemplate(),
    "comparativo_preco": ComparativoPrecoTemplate(),
    "lista_achados": ListaAchadosTemplate(),
}


def get_grupo_template(nome: str) -> GrupoTemplate:
    """
    Retorna template de grupo pelo nome
    
    Args:
        nome: Nome do template
        
    Returns:
        Instância do template
    """
    return GRUPO_TEMPLATES.get(nome, OfertaCompletaTemplate())
