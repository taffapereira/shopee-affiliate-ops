"""
Testes para módulo de extração de imagens
"""
import pytest
from src.utils.image_extractor import (
    is_product_image,
    is_high_quality_image,
    filter_carousel_images,
    get_main_product_image,
    validate_image_url,
    extract_images_from_shopee_data
)


class TestIsProductImage:
    """Testes para validação de imagens de produto"""
    
    def test_valid_product_image(self):
        """Aceita URLs válidas de imagens de produto"""
        valid_urls = [
            "https://cf.shopee.com.br/file/abc123def456.jpg",
            "https://down-br.img.susercontent.com/file/abc.jpg",
            "https://example.com/product/image.png",
        ]
        
        for url in valid_urls:
            assert is_product_image(url), f"Should accept: {url}"
    
    def test_rejects_logo_images(self):
        """Rejeita imagens de logo"""
        logo_urls = [
            "https://example.com/logo.png",
            "https://cdn.shopee.com/shop_logo/abc.jpg",
        ]
        
        for url in logo_urls:
            assert not is_product_image(url), f"Should reject logo: {url}"
    
    def test_rejects_icon_images(self):
        """Rejeita imagens de ícone"""
        icon_urls = [
            "https://example.com/icon_cart.png",
            "https://cdn.shopee.com/icons/star.svg",
        ]
        
        for url in icon_urls:
            assert not is_product_image(url), f"Should reject icon: {url}"
    
    def test_rejects_badge_images(self):
        """Rejeita badges e vouchers"""
        badge_urls = [
            "https://example.com/badge_verified.png",
            "https://cdn.shopee.com/voucher_label.png",
            "https://cdn.shopee.com/free_shipping_badge.jpg",
        ]
        
        for url in badge_urls:
            assert not is_product_image(url), f"Should reject badge: {url}"


class TestIsHighQualityImage:
    """Testes para validação de qualidade de imagem"""
    
    def test_accepts_large_images(self):
        """Aceita imagens grandes"""
        large_urls = [
            "https://example.com/product_800x800.jpg",
            "https://cdn.shopee.com/image?w=600",
        ]
        
        for url in large_urls:
            assert is_high_quality_image(url), f"Should accept large: {url}"
    
    def test_rejects_small_thumbnails(self):
        """Rejeita thumbnails pequenas"""
        small_urls = [
            "https://example.com/thumb_100x100.jpg",
            "https://cdn.shopee.com/image_50x50.png",
        ]
        
        for url in small_urls:
            assert not is_high_quality_image(url), f"Should reject small: {url}"


class TestFilterCarouselImages:
    """Testes para filtro de imagens do carrossel"""
    
    def test_filters_mixed_urls(self):
        """Filtra corretamente URLs mistas"""
        urls = [
            "https://cf.shopee.com.br/file/product123.jpg",  # válido
            "https://cdn.shopee.com/logo.png",  # logo
            "https://example.com/product_large.jpg",  # válido
            "https://cdn.shopee.com/icon_heart.png",  # ícone
        ]
        
        filtered = filter_carousel_images(urls)
        
        # Deve ter apenas as imagens válidas
        assert len(filtered) == 2
    
    def test_removes_duplicates(self):
        """Remove URLs duplicadas"""
        urls = [
            "https://example.com/product.jpg",
            "https://example.com/product.jpg",
            "https://example.com/PRODUCT.jpg",  # case diferente
        ]
        
        filtered = filter_carousel_images(urls)
        
        # Deve ter apenas 1 URL única
        assert len(filtered) == 1


class TestGetMainProductImage:
    """Testes para seleção de imagem principal"""
    
    def test_returns_first_valid_image(self):
        """Retorna primeira imagem válida"""
        urls = [
            "https://example.com/product1.jpg",
            "https://example.com/product2.jpg",
        ]
        
        main = get_main_product_image(urls)
        
        assert main is not None
        assert main == urls[0]
    
    def test_prefers_main_image_indicators(self):
        """Prefere imagens marcadas como principal"""
        urls = [
            "https://example.com/product_2.jpg",
            "https://example.com/product_main.jpg",  # indica principal
            "https://example.com/product_3.jpg",
        ]
        
        main = get_main_product_image(urls)
        
        # Deve preferir a que tem 'main'
        assert "main" in main
    
    def test_returns_none_for_empty_list(self):
        """Retorna None para lista vazia"""
        main = get_main_product_image([])
        
        assert main is None


class TestValidateImageUrl:
    """Testes para validação de URLs de imagem"""
    
    def test_valid_urls(self):
        """Aceita URLs válidas"""
        valid_urls = [
            "https://example.com/image.jpg",
            "http://cdn.shopee.com/file.png",
        ]
        
        for url in valid_urls:
            assert validate_image_url(url), f"Should be valid: {url}"
    
    def test_rejects_invalid_urls(self):
        """Rejeita URLs inválidas"""
        invalid_urls = [
            "",
            "not-a-url",
            "ftp://example.com/file.jpg",
            "/relative/path.jpg",
            "https://example.com/img<script>.jpg",
        ]
        
        for url in invalid_urls:
            assert not validate_image_url(url), f"Should be invalid: {url}"


class TestExtractImagesFromShopeeData:
    """Testes para extração de imagens de dados do produto"""
    
    def test_extracts_from_image_field(self):
        """Extrai do campo 'image'"""
        product_data = {
            "image": "https://example.com/product.jpg"
        }
        
        images = extract_images_from_shopee_data(product_data)
        
        assert len(images) >= 1
    
    def test_extracts_from_images_list(self):
        """Extrai de lista de imagens"""
        product_data = {
            "images": [
                "https://example.com/product1.jpg",
                "https://example.com/product2.jpg",
            ]
        }
        
        images = extract_images_from_shopee_data(product_data)
        
        assert len(images) == 2
    
    def test_extracts_from_imagens_adicionais(self):
        """Extrai do campo brasileiro 'imagens_adicionais'"""
        product_data = {
            "imagem_url": "https://example.com/main.jpg",
            "imagens_adicionais": [
                "https://example.com/extra1.jpg",
                "https://example.com/extra2.jpg",
            ]
        }
        
        images = extract_images_from_shopee_data(product_data)
        
        assert len(images) >= 1
    
    def test_handles_empty_data(self):
        """Trata dados vazios"""
        images = extract_images_from_shopee_data({})
        
        assert images == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
