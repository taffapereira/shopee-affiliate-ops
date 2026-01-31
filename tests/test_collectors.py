"""
Testes para módulo de coletores
"""
import pytest
from src.collectors.offer_parser import OfferParser


def test_parse_offer():
    """Testa parsing de oferta"""
    parser = OfferParser()
    
    raw_offer = {
        "item_id": "67890",
        "shop_id": "12345",
        "product_name": "Fone Bluetooth",
        "price_max": 10000000,  # R$ 100,00 (em centavos * 1000)
        "price_min": 8000000,   # R$ 80,00
        "commission_rate": 1000,  # 10%
        "item_rating": {"rating_star": 4.5, "rating_count": [50]},
        "item_sold": 100,
        "product_link": "https://shopee.com.br/test",
        "image": "https://example.com/image.jpg",
        "category_name": "Electronics"
    }
    
    produto = parser.parse_offer(raw_offer, "tech")
    
    assert produto is not None
    assert produto["shopee_id"] == "12345_67890"
    assert produto["nome"] == "Fone Bluetooth"
    assert produto["preco_original"] == 100.0
    assert produto["preco_promocional"] == 80.0
    assert produto["comissao_percentual"] == 10.0
    assert produto["nicho"] == "tech"


def test_validar_produto():
    """Testa validação de produto"""
    parser = OfferParser()
    
    # Produto válido
    produto_valido = {
        "preco_original": 100.0,
        "preco_promocional": 80.0,
        "comissao_percentual": 10.0,
        "rating": 4.5,
        "total_avaliacoes": 50,
        "imagem_url": "https://example.com/image.jpg"
    }
    
    is_valid, motivo = parser.validar_produto(produto_valido)
    assert is_valid is True
    
    # Produto com preço muito baixo
    produto_invalido = {
        "preco_original": 5.0,
        "comissao_percentual": 10.0,
        "rating": 4.5,
        "total_avaliacoes": 50,
        "imagem_url": "https://example.com/image.jpg"
    }
    
    is_valid, motivo = parser.validar_produto(produto_invalido)
    assert is_valid is False
    assert "Preço muito baixo" in motivo


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
