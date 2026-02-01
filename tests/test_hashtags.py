"""
Testes para módulo de hashtags
"""
import pytest
from src.utils.hashtags import (
    normalize_text,
    extract_keywords,
    generate_hashtags,
    format_hashtags,
    generate_hashtags_string
)


class TestNormalizeText:
    """Testes para normalização de texto"""
    
    def test_remove_accents(self):
        """Remove acentos corretamente"""
        result = normalize_text("Pijama Americano para Amamentação")
        assert result == "pijama americano para amamentacao"
    
    def test_lowercase(self):
        """Converte para minúsculas"""
        result = normalize_text("FONE BLUETOOTH")
        assert result == "fone bluetooth"
    
    def test_remove_special_chars(self):
        """Remove caracteres especiais"""
        result = normalize_text("Kit 2-Pç. Produto!")
        assert "kit" in result
        assert "2" in result
        assert "-" not in result


class TestExtractKeywords:
    """Testes para extração de palavras-chave"""
    
    def test_filter_stopwords(self):
        """Filtra stopwords em português"""
        keywords = extract_keywords("Kit de Pijama para Amamentação")
        
        # Deve conter palavras relevantes
        assert "pijama" in keywords
        assert "amamentacao" in keywords
        
        # Não deve conter stopwords
        assert "de" not in keywords
        assert "para" not in keywords
    
    def test_filter_short_words(self):
        """Filtra palavras muito curtas"""
        keywords = extract_keywords("Um Fone de 2 Vias")
        
        assert "um" not in keywords
        assert "de" not in keywords
    
    def test_remove_duplicates(self):
        """Remove duplicatas mantendo ordem"""
        keywords = extract_keywords("Fone Bluetooth Fone Wireless")
        
        # Deve ter apenas uma ocorrência
        assert keywords.count("fone") == 1


class TestGenerateHashtags:
    """Testes para geração de hashtags"""
    
    def test_basic_generation(self):
        """Gera hashtags básicas"""
        hashtags = generate_hashtags("Fone Bluetooth Sem Fio")
        
        assert len(hashtags) > 0
        assert "fone" in hashtags
        assert "bluetooth" in hashtags
    
    def test_includes_nicho_tags(self):
        """Inclui hashtags do nicho"""
        hashtags = generate_hashtags("Fone Bluetooth", nicho="tech")
        
        # Deve incluir alguma tag do nicho tech
        tech_tags = ['tech', 'tecnologia', 'gadgets', 'eletronicos']
        assert any(tag in hashtags for tag in tech_tags)
    
    def test_includes_base_tags(self):
        """Inclui hashtags base (shopee, oferta)"""
        hashtags = generate_hashtags("Produto Teste", include_base=True)
        
        assert "shopee" in hashtags or "oferta" in hashtags
    
    def test_respects_max_limit(self):
        """Respeita limite máximo de hashtags"""
        hashtags = generate_hashtags(
            "Produto com Nome Muito Grande e Várias Palavras",
            nicho="casa",
            max_hashtags=5
        )
        
        assert len(hashtags) <= 5
    
    def test_without_base_tags(self):
        """Pode excluir hashtags base"""
        hashtags = generate_hashtags(
            "Produto Teste",
            include_base=False
        )
        
        # Não deve ter tags base
        assert "shopee" not in hashtags
        assert "oferta" not in hashtags
        assert "promocao" not in hashtags


class TestFormatHashtags:
    """Testes para formatação de hashtags"""
    
    def test_with_hash_symbol(self):
        """Adiciona # antes de cada hashtag"""
        result = format_hashtags(['shopee', 'oferta', 'tech'])
        
        assert result == "#shopee #oferta #tech"
    
    def test_without_hash_symbol(self):
        """Funciona sem o símbolo #"""
        result = format_hashtags(['shopee', 'oferta'], with_hash=False)
        
        assert result == "shopee oferta"
    
    def test_custom_separator(self):
        """Usa separador customizado"""
        result = format_hashtags(['a', 'b', 'c'], separator=', ')
        
        assert result == "#a, #b, #c"


class TestGenerateHashtagsString:
    """Testes para geração de string de hashtags"""
    
    def test_generates_formatted_string(self):
        """Gera string formatada corretamente"""
        result = generate_hashtags_string("Kit 2 Pijamas Americanos", nicho="casa")
        
        # Deve começar com #
        assert result.startswith("#")
        
        # Deve ter espaços entre hashtags
        assert " " in result
        
        # Deve ter hashtags relevantes
        assert "#pijamas" in result or "#americanos" in result
    
    def test_real_product_example(self):
        """Testa com exemplo real de produto"""
        result = generate_hashtags_string(
            "Fone de Ouvido Bluetooth TWS com Case",
            nicho="tech"
        )
        
        # Verifica hashtags esperadas
        assert "#fone" in result or "#bluetooth" in result or "#tws" in result
        
        # Deve ter hashtag de shopee/oferta
        assert "#shopee" in result or "#oferta" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
