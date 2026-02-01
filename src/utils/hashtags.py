"""
Gerador de hashtags baseado no nome do produto
"""
import re
import unicodedata
from typing import List, Optional


# Stopwords em português para filtrar
STOPWORDS_PT = {
    'de', 'da', 'do', 'das', 'dos', 'e', 'em', 'um', 'uma', 'uns', 'umas',
    'para', 'por', 'com', 'sem', 'sob', 'sobre', 'entre', 'a', 'o', 'as', 'os',
    'que', 'se', 'na', 'no', 'nas', 'nos', 'ao', 'aos', 'pela', 'pelo', 'pelas',
    'pelos', 'sua', 'seu', 'suas', 'seus', 'este', 'esta', 'estes', 'estas',
    'esse', 'essa', 'esses', 'essas', 'aquele', 'aquela', 'aqueles', 'aquelas',
    'isso', 'isto', 'aquilo', 'qual', 'quais', 'quanto', 'quantos', 'quanta',
    'quantas', 'mais', 'menos', 'muito', 'muita', 'muitos', 'muitas', 'pouco',
    'pouca', 'poucos', 'poucas', 'todo', 'toda', 'todos', 'todas', 'outro',
    'outra', 'outros', 'outras', 'mesmo', 'mesma', 'mesmos', 'mesmas', 'tal',
    'tais', 'quando', 'onde', 'como', 'porque', 'porquê', 'pois', 'já', 'ainda',
    'também', 'só', 'apenas', 'kit', 'pcs', 'pçs', 'unidades', 'unidade',
    'peças', 'peça', 'conjunto', 'jogo', 'pç', 'pc', 'un', 'cx', 'caixa',
    'pacote', 'pack', 'novo', 'nova', 'novos', 'novas', 'original', 'original',
    'hot', 'sale', 'promo', 'premium', 'top', 'best', 'super', 'mega', 'ultra',
    'pro', 'max', 'plus', 'mini', 'grande', 'pequeno', 'medio', 'médio'
}

# Hashtags padrão por nicho
HASHTAGS_NICHO = {
    'casa': ['casa', 'decoracao', 'cozinha', 'organizacao', 'lar'],
    'tech': ['tech', 'tecnologia', 'gadgets', 'eletronicos'],
    'pet': ['pet', 'cachorro', 'gato', 'petlovers', 'animais'],
    'cosmeticos': ['beleza', 'skincare', 'makeup', 'cosmeticos', 'beauty']
}

# Hashtags sempre incluídas
HASHTAGS_BASE = ['shopee', 'oferta', 'promocao']


def normalize_text(text: str) -> str:
    """
    Normaliza texto removendo acentos e caracteres especiais
    
    Args:
        text: Texto para normalizar
        
    Returns:
        Texto normalizado (lowercase, sem acentos, sem caracteres especiais)
    """
    # Remove acentos
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    
    # Converte para lowercase
    text = text.lower()
    
    # Remove caracteres especiais, mantém apenas letras e números
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    return text


def extract_keywords(product_name: str) -> List[str]:
    """
    Extrai palavras-chave do nome do produto
    
    Args:
        product_name: Nome do produto
        
    Returns:
        Lista de palavras-chave relevantes
    """
    normalized = normalize_text(product_name)
    
    # Divide em palavras
    words = normalized.split()
    
    # Filtra stopwords e palavras muito curtas
    keywords = [
        word for word in words
        if len(word) >= 3 and word not in STOPWORDS_PT
    ]
    
    # Remove duplicatas mantendo ordem
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    
    return unique_keywords


def generate_hashtags(
    product_name: str,
    nicho: Optional[str] = None,
    max_hashtags: int = 7,
    include_base: bool = True
) -> List[str]:
    """
    Gera hashtags relevantes baseadas no nome do produto
    
    Args:
        product_name: Nome do produto
        nicho: Nicho do produto (casa, tech, pet, cosmeticos)
        max_hashtags: Número máximo de hashtags a gerar
        include_base: Se True, inclui hashtags base (shopee, oferta, etc)
        
    Returns:
        Lista de hashtags (sem #)
        
    Exemplo:
        >>> generate_hashtags("Fone Bluetooth Sem Fio TWS", nicho="tech")
        ['fone', 'bluetooth', 'tws', 'tech', 'tecnologia', 'shopee', 'oferta']
    """
    hashtags = []
    
    # 1. Extrai keywords do produto
    keywords = extract_keywords(product_name)
    
    # Adiciona as primeiras keywords (limite de 3-4 do nome do produto)
    base_count = len(HASHTAGS_BASE) if include_base else 0
    product_keywords_limit = min(4, max_hashtags - base_count) if include_base else max_hashtags
    hashtags.extend(keywords[:product_keywords_limit])
    
    # 2. Adiciona hashtags do nicho
    if nicho and nicho in HASHTAGS_NICHO:
        nicho_tags = HASHTAGS_NICHO[nicho]
        for tag in nicho_tags:
            if tag not in hashtags and len(hashtags) < max_hashtags - len(HASHTAGS_BASE):
                hashtags.append(tag)
    
    # 3. Adiciona hashtags base
    if include_base:
        for tag in HASHTAGS_BASE:
            if tag not in hashtags and len(hashtags) < max_hashtags:
                hashtags.append(tag)
    
    return hashtags[:max_hashtags]


def format_hashtags(
    hashtags: List[str],
    with_hash: bool = True,
    separator: str = ' '
) -> str:
    """
    Formata lista de hashtags como string
    
    Args:
        hashtags: Lista de hashtags
        with_hash: Se True, adiciona # antes de cada hashtag
        separator: Separador entre hashtags
        
    Returns:
        String formatada com hashtags
        
    Exemplo:
        >>> format_hashtags(['shopee', 'oferta', 'tech'])
        '#shopee #oferta #tech'
    """
    if with_hash:
        return separator.join(f'#{tag}' for tag in hashtags)
    return separator.join(hashtags)


def generate_hashtags_string(
    product_name: str,
    nicho: Optional[str] = None,
    max_hashtags: int = 7
) -> str:
    """
    Gera string de hashtags pronta para uso
    
    Args:
        product_name: Nome do produto
        nicho: Nicho do produto
        max_hashtags: Número máximo de hashtags
        
    Returns:
        String com hashtags formatadas
        
    Exemplo:
        >>> generate_hashtags_string("Kit 2 Pijamas Americanos", nicho="casa")
        '#pijamas #americanos #casa #decoracao #shopee #oferta #promocao'
    """
    hashtags = generate_hashtags(product_name, nicho, max_hashtags)
    return format_hashtags(hashtags)
