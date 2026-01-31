"""
Constantes do sistema - Nichos, Canais, Formatos, etc.
"""

# Nichos suportados
NICHOS = {
    "casa": {
        "nome": "Casa & Cozinha",
        "persona": "Cléo Cozinha Prática",
        "categoria_shopee": ["Home & Living", "Kitchen & Dining"],
        "palavras_chave": ["casa", "cozinha", "decoração", "organização"]
    },
    "tech": {
        "nome": "Tech & Wearables",
        "persona": "Léo Tech Acessível",
        "categoria_shopee": ["Electronics", "Mobiles & Gadgets"],
        "palavras_chave": ["fone", "smartwatch", "carregador", "cabo", "tech"]
    },
    "pet": {
        "nome": "Mundo Pet",
        "persona": "Pri e os Peludinhos",
        "categoria_shopee": ["Pet Care"],
        "palavras_chave": ["pet", "cachorro", "gato", "ração", "brinquedo"]
    },
    "cosmeticos": {
        "nome": "Cosméticos",
        "persona": "Tati Beleza Real",
        "categoria_shopee": ["Beauty & Personal Care"],
        "palavras_chave": ["makeup", "skincare", "cabelo", "cosmético"]
    }
}

# Canais de publicação
CANAIS = {
    "tiktok": {
        "nome": "TikTok",
        "posts_por_dia": 4,
        "formato": "video",
        "duracao_max": 60,
        "prioridade": 1
    },
    "reels": {
        "nome": "Instagram Reels",
        "posts_por_dia": 3,
        "formato": "video",
        "duracao_max": 90,
        "prioridade": 2
    },
    "stories": {
        "nome": "Instagram Stories",
        "posts_por_dia": 6,
        "formato": "imagem_video",
        "duracao_max": 15,
        "prioridade": 3
    },
    "grupo": {
        "nome": "Grupo Telegram",
        "posts_por_dia": 10,
        "formato": "texto",
        "prioridade": 4
    }
}

# Formatos de conteúdo
FORMATOS = {
    "video15s": "Vídeo de 15 segundos",
    "video30s": "Vídeo de 30 segundos",
    "video60s": "Vídeo de 60 segundos",
    "texto": "Texto puro",
    "stories": "Stories (imagem + texto)",
    "carrossel": "Carrossel de imagens"
}

# Tipos de campanha
CAMPANHAS = {
    "oferta_dia": "Oferta do Dia",
    "top_comissao": "Top Comissão",
    "achado": "Achado do Dia",
    "flash": "Oferta Flash"
}

# SubId structure para rastreamento
# subId1 = canal (tiktok|reels|stories|grupo)
# subId2 = nicho (casa|tech|pet|cosmeticos)
# subId3 = formato (video15s|video30s|texto|stories|carrossel)
# subId4 = campanha (oferta_dia|top_comissao|achado|flash)
# subId5 = data (AAAAMMDD)

# Emojis por nicho
EMOJIS_NICHO = {
    "casa": ["🏠", "🍳", "🧹", "🛋️", "✨"],
    "tech": ["📱", "⌚", "🎧", "💻", "⚡"],
    "pet": ["🐶", "🐱", "🐾", "❤️", "🦴"],
    "cosmeticos": ["💄", "💅", "✨", "🌸", "💆‍♀️"]
}

# Horários de publicação (timezone: America/Sao_Paulo)
HORARIOS_PUBLICACAO = {
    "tiktok": ["08:00", "12:00", "18:00", "20:00"],
    "reels": ["09:00", "14:00", "19:00"],
    "stories": ["07:00", "10:00", "13:00", "16:00", "19:00", "21:00"],
    "grupo": ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "19:00", "20:00", "21:00", "22:00"]
}

# Pesos para o algoritmo de ranking
PESO_COMISSAO = 0.35
PESO_PRECO = 0.25
PESO_RATING = 0.20
PESO_VENDAS = 0.15
PESO_DESCONTO = 0.05

# Limites de API
SHOPEE_API_RATE_LIMIT = 100  # chamadas por minuto
PRODUTOS_POR_COLETA = 50
TOP_N_PRODUTOS = 10

# Compliance
DISCLAIMER_AFILIADO = "🔗 Link de afiliado"
DISCLAIMER_PRECO_SUJEITO = "⚠️ Preço sujeito a alteração"
