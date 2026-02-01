"""
Extrator e filtro de imagens de produtos Shopee
Melhora a qualidade das imagens extraídas, filtrando logos e ícones
"""
import re
from typing import List, Optional
from urllib.parse import urlparse


# Padrões de URLs que indicam imagens de produto (carrossel)
PRODUCT_IMAGE_PATTERNS = [
    r'.*shopee\..*/([\da-f]{32})(?:_tn)?\.(?:jpg|jpeg|png|webp)$',  # Hash de 32 chars
    r'.*cf\.shopee\..*product.*',  # CDN de produtos
    r'.*down-.*shopee.*',  # Download path
]

# Padrões de URLs a excluir (logos, ícones, badges)
EXCLUDE_PATTERNS = [
    r'.*logo.*',
    r'.*icon.*',
    r'.*badge.*',
    r'.*banner.*',
    r'.*avatar.*',
    r'.*emoji.*',
    r'.*sprite.*',
    r'.*flag.*',
    r'.*payment.*',
    r'.*shipping.*',
    r'.*seller.*',
    r'.*shop_.*',
    r'.*voucher.*',
    r'.*coin.*',
    r'.*reward.*',
    r'.*promo.*',
    r'.*ad_.*',
    r'.*mall.*',
    r'.*brand.*',
    r'.*verified.*',
    r'.*official.*',
    r'.*rating.*',
    r'.*star.*',
    r'.*like.*',
    r'.*heart.*',
    r'.*free.*shipping.*',
    r'.*\_ss.*',  # Small size
    r'.*100x100.*',  # Thumbnails muito pequenas
    r'.*50x50.*',
    r'.*_tn\..*',  # Thumbnails
    r'.*/thumb/.*',  # Diretório de thumbnails
]

# Dimensões mínimas esperadas (baseado na URL)
MIN_IMAGE_SIZE = 200


def is_product_image(url: str) -> bool:
    """
    Verifica se a URL é uma imagem de produto válida
    
    Args:
        url: URL da imagem
        
    Returns:
        True se parece ser uma imagem de produto
    """
    url_lower = url.lower()
    
    # Verifica se é uma URL de imagem
    if not any(url_lower.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
        # Pode não ter extensão (CDN), verifica outros padrões
        if 'image' not in url_lower and 'img' not in url_lower and 'media' not in url_lower:
            return False
    
    # Verifica padrões de exclusão
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, url_lower):
            return False
    
    return True


def is_high_quality_image(url: str) -> bool:
    """
    Verifica se a imagem parece ter qualidade suficiente
    
    Args:
        url: URL da imagem
        
    Returns:
        True se parece ter qualidade adequada
    """
    url_lower = url.lower()
    
    # Procura indicadores de tamanho na URL
    size_patterns = [
        r'(\d+)x(\d+)',  # 800x800
        r'_(\d+)_(\d+)\.',  # _800_800.
        r'w=(\d+)',  # w=800
        r'h=(\d+)',  # h=800
    ]
    
    for pattern in size_patterns:
        match = re.search(pattern, url_lower)
        if match:
            try:
                # Pega o primeiro grupo que é número
                size = int(match.group(1))
                if size < MIN_IMAGE_SIZE:
                    return False
            except (ValueError, IndexError):
                pass
    
    return True


def extract_product_images_from_html(html_content: str) -> List[str]:
    """
    Extrai URLs de imagens de produto de HTML da página Shopee
    
    Args:
        html_content: Conteúdo HTML da página
        
    Returns:
        Lista de URLs de imagens de produto
    """
    # Regex para encontrar URLs de imagens
    image_patterns = [
        # Imagens em tags img
        r'<img[^>]+src=["\']([^"\']+)["\']',
        r'<img[^>]+data-src=["\']([^"\']+)["\']',
        r'<img[^>]+srcset=["\']([^"\']+)["\']',
        
        # Imagens em background
        r'background(?:-image)?:\s*url\(["\']?([^"\')\s]+)["\']?\)',
        
        # Imagens em atributos data
        r'data-(?:image|src|url)=["\']([^"\']+)["\']',
        
        # JSON com URLs
        r'"(?:image|imageUrl|img|url)":\s*"([^"]+\.(jpg|jpeg|png|webp)[^"]*)"',
    ]
    
    all_urls = set()
    
    for pattern in image_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                url = match[0]
            else:
                url = match
            
            # Normaliza URL
            url = url.strip()
            if url.startswith('//'):
                url = 'https:' + url
            
            all_urls.add(url)
    
    return list(all_urls)


def filter_carousel_images(image_urls: List[str]) -> List[str]:
    """
    Filtra lista de URLs para manter apenas imagens do carrossel de produto
    
    Args:
        image_urls: Lista de URLs de imagens
        
    Returns:
        Lista filtrada com imagens de produto de alta qualidade
    """
    filtered = []
    
    for url in image_urls:
        if is_product_image(url) and is_high_quality_image(url):
            filtered.append(url)
    
    # Remove duplicatas mantendo ordem
    seen = set()
    unique = []
    for url in filtered:
        # Normaliza URL para comparação
        normalized = url.split('?')[0].lower()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(url)
    
    return unique


def get_main_product_image(image_urls: List[str]) -> Optional[str]:
    """
    Seleciona a melhor imagem principal do produto
    
    Args:
        image_urls: Lista de URLs de imagens
        
    Returns:
        URL da imagem principal ou None
    """
    filtered = filter_carousel_images(image_urls)
    
    if not filtered:
        return None
    
    # Prioriza imagens que parecem ser a primeira do carrossel
    for url in filtered:
        if any(x in url.lower() for x in ['_0', 'main', 'primary', 'cover']):
            return url
    
    return filtered[0]


def validate_image_url(url: str) -> bool:
    """
    Valida se uma URL de imagem é válida e acessível
    
    Args:
        url: URL para validar
        
    Returns:
        True se a URL parece válida
    """
    try:
        parsed = urlparse(url)
        
        # Deve ter scheme e netloc
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # Scheme deve ser http ou https
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Não deve ter caracteres estranhos
        if any(c in url for c in ['<', '>', '"', "'", '\n', '\r', '\t']):
            return False
        
        return True
        
    except Exception:
        return False


def extract_images_from_shopee_data(product_data: dict) -> List[str]:
    """
    Extrai imagens de dados estruturados do produto Shopee
    
    Args:
        product_data: Dicionário com dados do produto
        
    Returns:
        Lista de URLs de imagens
    """
    images = []
    
    # Campos comuns onde imagens podem estar
    image_fields = [
        'image', 'imageUrl', 'imagem_url', 'imagem',
        'images', 'imagens', 'productImages', 'product_images',
        'imagens_adicionais', 'additional_images'
    ]
    
    for field in image_fields:
        value = product_data.get(field)
        
        if not value:
            continue
        
        if isinstance(value, str):
            if validate_image_url(value):
                images.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and validate_image_url(item):
                    images.append(item)
                elif isinstance(item, dict):
                    # Pode ser {url: '...'} ou {src: '...'}
                    for key in ['url', 'src', 'image', 'imageUrl']:
                        if key in item and validate_image_url(item[key]):
                            images.append(item[key])
    
    return filter_carousel_images(images)
