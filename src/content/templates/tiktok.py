"""
Templates para TikTok - 5 tipos por nicho
"""
from typing import Dict, List


class TikTokTemplate:
    """Classe base para templates TikTok"""
    
    def __init__(self, nome: str, descricao: str, estrutura: List[str], duracao: int = 30):
        self.nome = nome
        self.descricao = descricao
        self.estrutura = estrutura
        self.duracao = duracao
    
    def get_prompt(self, produto: Dict, persona_context: str) -> str:
        """
        Gera prompt para LLM criar o conteúdo
        
        Args:
            produto: Dados do produto
            persona_context: Contexto da persona
            
        Returns:
            Prompt formatado
        """
        raise NotImplementedError


class ProblemasolucaoTemplate(TikTokTemplate):
    """Template: Problema → Solução"""
    
    def __init__(self):
        super().__init__(
            nome="problema_solucao",
            descricao="Apresenta um problema comum e mostra o produto como solução",
            estrutura=[
                "Hook: Apresenta o problema (3s)",
                "Agravamento: Por que é frustrante (3s)",
                "Solução: Apresenta o produto (10s)",
                "Benefícios: Como resolve (10s)",
                "CTA: Call to action (4s)"
            ],
            duracao=30
        )
    
    def get_prompt(self, produto: Dict, persona_context: str) -> str:
        return f"""{persona_context}

**Template: Problema → Solução**

Crie um roteiro de TikTok de 30 segundos sobre o produto abaixo:

**Produto:** {produto.get('nome')}
**Preço:** R$ {produto.get('preco_promocional') or produto.get('preco_original')}
**Desconto:** {produto.get('desconto_percentual', 0):.0f}%

**Estrutura:**
1. HOOK (3s): Mostre o problema que o produto resolve
2. AGRAVAMENTO (3s): Por que esse problema é frustrante
3. SOLUÇÃO (10s): Apresente o produto como solução
4. BENEFÍCIOS (10s): Liste 2-3 benefícios principais
5. CTA (4s): Call to action com urgência

**Requisitos:**
- Use linguagem natural e conversacional
- Inclua emojis relevantes
- Crie senso de urgência pelo desconto
- Máximo 150 palavras
- Tom: {persona_context.split('Tom de voz:')[1].split('**')[0].strip() if 'Tom de voz:' in persona_context else 'casual'}
"""


class UnboxingRapidoTemplate(TikTokTemplate):
    """Template: Unboxing Rápido"""
    
    def __init__(self):
        super().__init__(
            nome="unboxing_rapido",
            descricao="Unboxing dinâmico mostrando o produto",
            estrutura=[
                "Hook: O que vamos abrir (2s)",
                "Unboxing: Abrindo e mostrando (15s)",
                "Primeiras impressões (10s)",
                "CTA (3s)"
            ],
            duracao=30
        )
    
    def get_prompt(self, produto: Dict, persona_context: str) -> str:
        return f"""{persona_context}

**Template: Unboxing Rápido**

Crie roteiro de TikTok (30s) tipo unboxing do produto:

**Produto:** {produto.get('nome')}
**Preço:** R$ {produto.get('preco_promocional') or produto.get('preco_original')}

**Estrutura:**
1. HOOK (2s): "Chegou! Vamos abrir..."
2. UNBOXING (15s): Descreva o que vem na caixa
3. PRIMEIRAS IMPRESSÕES (10s): Qualidade, acabamento, tamanho
4. CTA (3s): Link na bio

Seja empolgado mas autêntico. Use emojis.
"""


class AntesDopoisTemplate(TikTokTemplate):
    """Template: Antes/Depois"""
    
    def __init__(self):
        super().__init__(
            nome="antes_depois",
            descricao="Mostra transformação ou comparação antes/depois",
            estrutura=[
                "Antes: Situação sem o produto (8s)",
                "Transição (2s)",
                "Depois: Com o produto (15s)",
                "CTA (5s)"
            ],
            duracao=30
        )
    
    def get_prompt(self, produto: Dict, persona_context: str) -> str:
        return f"""{persona_context}

**Template: Antes/Depois**

Roteiro TikTok comparando antes e depois de usar o produto:

**Produto:** {produto.get('nome')}
**Categoria:** {produto.get('nicho')}

**Estrutura:**
1. ANTES (8s): Como era sem o produto (problema/situação)
2. TRANSIÇÃO (2s): "Aí eu descobri isso..."
3. DEPOIS (15s): Como ficou com o produto (solução/resultado)
4. CTA (5s): Aproveita que está em promoção!

Mostre contraste claro. Use emojis de transformação ✨
"""


class POVViralTemplate(TikTokTemplate):
    """Template: POV (Point of View) Viral"""
    
    def __init__(self):
        super().__init__(
            nome="pov_viral",
            descricao="Formato POV viral do TikTok",
            estrutura=[
                "Setup POV (5s)",
                "Desenvolvimento (20s)",
                "Punchline/CTA (5s)"
            ],
            duracao=30
        )
    
    def get_prompt(self, produto: Dict, persona_context: str) -> str:
        return f"""{persona_context}

**Template: POV Viral**

Crie um POV viral sobre o produto:

**Produto:** {produto.get('nome')}
**Nicho:** {produto.get('nicho')}

**Estrutura:**
POV: [situação relatable] e você descobre {produto.get('nome')}

Desenvolva a história de forma divertida/relatable.
Use trending sounds/frases do TikTok.
Máximo 120 palavras.
"""


class ReviewHonestoTemplate(TikTokTemplate):
    """Template: Review Honesto"""
    
    def __init__(self):
        super().__init__(
            nome="review_honesto",
            descricao="Review direto e honesto do produto",
            estrutura=[
                "Hook: Review rápido (3s)",
                "Contexto: Quanto tempo testou (3s)",
                "Pontos positivos (12s)",
                "Pontos negativos se houver (5s)",
                "Veredicto e CTA (7s)"
            ],
            duracao=30
        )
    
    def get_prompt(self, produto: Dict, persona_context: str) -> str:
        return f"""{persona_context}

**Template: Review Honesto**

Review autêntico do produto:

**Produto:** {produto.get('nome')}
**Rating:** {produto.get('rating'):.1f}⭐
**Preço:** R$ {produto.get('preco_promocional') or produto.get('preco_original')}

**Estrutura:**
1. HOOK (3s): "Review sincero de [produto]"
2. CONTEXTO (3s): Há quanto tempo usa
3. PRÓS (12s): 3-4 pontos positivos
4. CONTRAS (5s): 1 ponto de atenção (seja honesto)
5. VEREDICTO (7s): Vale a pena? + CTA

Seja autêntico. Honestidade gera confiança.
"""


# Dicionário com todos os templates TikTok
TIKTOK_TEMPLATES = {
    "problema_solucao": ProblemasolucaoTemplate(),
    "unboxing_rapido": UnboxingRapidoTemplate(),
    "antes_depois": AntesDopoisTemplate(),
    "pov_viral": POVViralTemplate(),
    "review_honesto": ReviewHonestoTemplate(),
}


def get_tiktok_template(nome: str) -> TikTokTemplate:
    """
    Retorna template TikTok pelo nome
    
    Args:
        nome: Nome do template
        
    Returns:
        Instância do template
    """
    return TIKTOK_TEMPLATES.get(nome, ProblemasolucaoTemplate())


def get_all_tiktok_templates() -> List[TikTokTemplate]:
    """Retorna todos os templates TikTok"""
    return list(TIKTOK_TEMPLATES.values())
