"""
Testes para módulo de conteúdo
"""
import pytest
from src.content.generator import ContentGenerator
from src.content.personas import get_persona


def test_get_persona():
    """Testa obtenção de persona"""
    persona = get_persona("tech")
    
    assert persona is not None
    assert persona.nome == "Léo Tech Acessível"
    assert persona.nicho == "tech"


def test_generate_grupo_content():
    """Testa geração de conteúdo para grupo"""
    generator = ContentGenerator()
    
    produto = {
        "id": 1,
        "nome": "Fone Bluetooth Test",
        "preco_original": 100.0,
        "preco_promocional": 80.0,
        "desconto_percentual": 20.0,
        "nicho": "tech",
        "url_produto": "https://shopee.com.br/test",
        "imagem_url": "https://example.com/image.jpg"
    }
    
    conteudo = generator.generate_for_canal(
        canal="grupo",
        produto=produto
    )
    
    assert conteudo is not None
    assert conteudo["canal"] == "grupo"
    assert conteudo["nicho"] == "tech"
    assert "copy_texto" in conteudo


def test_generate_tiktok_content():
    """Testa geração de conteúdo para TikTok"""
    generator = ContentGenerator()
    
    produto = {
        "id": 1,
        "nome": "Fone Bluetooth Test",
        "preco_original": 100.0,
        "preco_promocional": 80.0,
        "nicho": "tech"
    }
    
    conteudo = generator.generate_for_canal(
        canal="tiktok",
        produto=produto
    )
    
    assert conteudo is not None
    assert conteudo["canal"] == "tiktok"
    assert "prompt_llm" in conteudo  # TikTok precisa de LLM
    assert conteudo["duracao_segundos"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
