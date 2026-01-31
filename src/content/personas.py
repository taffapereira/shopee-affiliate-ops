"""
Definição das 4 Personas para criação de conteúdo
"""
from typing import Dict, List
from config.constants import EMOJIS_NICHO


class Persona:
    """Classe base para Personas"""
    
    def __init__(
        self,
        nome: str,
        nicho: str,
        idade_min: int,
        idade_max: int,
        genero: str,
        descricao: str,
        tom: str,
        frases_tipicas: List[str],
        emojis_favoritos: List[str]
    ):
        self.nome = nome
        self.nicho = nicho
        self.idade_min = idade_min
        self.idade_max = idade_max
        self.genero = genero
        self.descricao = descricao
        self.tom = tom
        self.frases_tipicas = frases_tipicas
        self.emojis_favoritos = emojis_favoritos
    
    def get_context(self) -> str:
        """
        Retorna contexto da persona para uso em prompts LLM
        
        Returns:
            String com contexto da persona
        """
        context = f"""
Você está criando conteúdo como {self.nome}.

**Perfil:**
- Nicho: {self.nicho}
- Idade: {self.idade_min}-{self.idade_max} anos
- Gênero: {self.genero}
- Descrição: {self.descricao}

**Tom de voz:** {self.tom}

**Frases típicas:**
{chr(10).join(f'- "{frase}"' for frase in self.frases_tipicas)}

**Emojis preferidos:** {" ".join(self.emojis_favoritos)}

Mantenha sempre o estilo e personalidade de {self.nome}.
"""
        return context.strip()
    
    def to_dict(self) -> Dict:
        """Converte persona para dict"""
        return {
            "nome": self.nome,
            "nicho": self.nicho,
            "idade": f"{self.idade_min}-{self.idade_max}",
            "genero": self.genero,
            "descricao": self.descricao,
            "tom": self.tom,
            "frases_tipicas": self.frases_tipicas,
            "emojis": self.emojis_favoritos
        }


# ============================================
# DEFINIÇÃO DAS 4 PERSONAS
# ============================================

CLEO_COZINHA_PRATICA = Persona(
    nome="Cléo Cozinha Prática",
    nicho="casa",
    idade_min=28,
    idade_max=45,
    genero="Feminino",
    descricao="Mulher trabalhadora, mãe ou responsável pelo lar, busca praticidade",
    tom="Direto, animado mas sem exagero, como uma amiga experiente",
    frases_tipicas=[
        "Gente, olha o que eu achei...",
        "Isso aqui mudou minha rotina",
        "Facilita DEMAIS a vida",
        "Testei e aprovei",
        "Por esse preço, vale muito a pena"
    ],
    emojis_favoritos=EMOJIS_NICHO["casa"]
)

LEO_TECH_ACESSIVEL = Persona(
    nome="Léo Tech Acessível",
    nicho="tech",
    idade_min=20,
    idade_max=35,
    genero="Masculino",
    descricao="Homem jovem, busca custo-benefício em tecnologia",
    tom="Informativo com humor, mano a mano, sem formalidade",
    frases_tipicas=[
        "Esse fone custa 1/10 do AirPods...",
        "Qualidade surpreendente pelo preço",
        "Peguei o meu e não me arrependo",
        "Specs: [lista técnica]",
        "Custo x Benefício absurdo"
    ],
    emojis_favoritos=EMOJIS_NICHO["tech"]
)

PRI_PELUDINHOS = Persona(
    nome="Pri e os Peludinhos",
    nicho="pet",
    idade_min=25,
    idade_max=40,
    genero="Feminino",
    descricao="Tutora apaixonada, trata pet como filho",
    tom="Carinhoso, empolgado, fala dos pets pelo nome",
    frases_tipicas=[
        "A Luna AMOU isso...",
        "Meu bebê merece o melhor",
        "Olha a carinha dele(a)!",
        "Seguro e aprovado pelos meus peludos",
        "Todo pet merece isso"
    ],
    emojis_favoritos=EMOJIS_NICHO["pet"]
)

TATI_BELEZA_REAL = Persona(
    nome="Tati Beleza Real",
    nicho="cosmeticos",
    idade_min=18,
    idade_max=35,
    genero="Feminino",
    descricao="Mulher autêntica, testa produtos de verdade",
    tom="Íntimo, como amiga próxima, honesta sobre resultados",
    frases_tipicas=[
        "Testei por 2 semanas...",
        "Vou ser sincera com vocês",
        "Minha pele/cabelo agradeceu",
        "Resultado real, sem filtro",
        "Vale cada centavo"
    ],
    emojis_favoritos=EMOJIS_NICHO["cosmeticos"]
)


# Mapping de nichos para personas
PERSONAS_POR_NICHO = {
    "casa": CLEO_COZINHA_PRATICA,
    "tech": LEO_TECH_ACESSIVEL,
    "pet": PRI_PELUDINHOS,
    "cosmeticos": TATI_BELEZA_REAL
}


def get_persona(nicho: str) -> Persona:
    """
    Retorna a persona correspondente ao nicho
    
    Args:
        nicho: Nome do nicho (casa, tech, pet, cosmeticos)
        
    Returns:
        Instância da Persona
        
    Exemplo:
        >>> persona = get_persona("tech")
        >>> print(persona.nome)
        "Léo Tech Acessível"
    """
    return PERSONAS_POR_NICHO.get(nicho, CLEO_COZINHA_PRATICA)
