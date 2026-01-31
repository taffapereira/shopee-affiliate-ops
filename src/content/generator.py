"""
Orquestrador de geração de conteúdo
"""
from typing import Dict, List, Optional
from src.content.personas import get_persona
from src.content.templates.tiktok import get_tiktok_template, get_all_tiktok_templates
from src.content.templates.grupo import get_grupo_template, GRUPO_TEMPLATES
from src.content.templates.reels import get_reels_template
from src.content.templates.stories import get_stories_template
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ContentGenerator:
    """
    Orquestrador de geração de conteúdo para todos os canais
    """
    
    def __init__(self):
        self.logger = logger
    
    def generate_for_canal(
        self,
        canal: str,
        produto: Dict,
        template_nome: Optional[str] = None,
        variacao: int = 1
    ) -> Dict:
        """
        Gera conteúdo para um canal específico
        
        Args:
            canal: Nome do canal (tiktok, reels, stories, grupo)
            produto: Dados do produto
            template_nome: Nome do template específico (opcional)
            variacao: Número da variação (1-5)
            
        Returns:
            Dict com conteúdo gerado
        """
        nicho = produto.get('nicho')
        persona = get_persona(nicho)
        
        if canal == 'tiktok':
            return self._generate_tiktok(produto, persona, template_nome, variacao)
        elif canal == 'reels':
            return self._generate_reels(produto, persona, template_nome, variacao)
        elif canal == 'stories':
            return self._generate_stories(produto, persona, template_nome, variacao)
        elif canal == 'grupo':
            return self._generate_grupo(produto, persona, template_nome, variacao)
        else:
            logger.error(f"Canal desconhecido: {canal}")
            return {}
    
    def _generate_tiktok(
        self,
        produto: Dict,
        persona,
        template_nome: Optional[str],
        variacao: int
    ) -> Dict:
        """Gera conteúdo para TikTok"""
        # Se não especificou template, usa um dos 5
        if not template_nome:
            templates = get_all_tiktok_templates()
            template = templates[variacao % len(templates)]
        else:
            template = get_tiktok_template(template_nome)
        
        # Gera prompt para LLM
        prompt = template.get_prompt(produto, persona.get_context())
        
        return {
            "canal": "tiktok",
            "template": template.nome,
            "formato": f"video{template.duracao}s",
            "persona": persona.nome,
            "prompt_llm": prompt,
            "duracao_segundos": template.duracao,
            "variacao_numero": variacao,
            "produto_id": produto.get('id'),
            "nicho": produto.get('nicho')
        }
    
    def _generate_reels(
        self,
        produto: Dict,
        persona,
        template_nome: Optional[str],
        variacao: int
    ) -> Dict:
        """Gera conteúdo para Reels (similar ao TikTok)"""
        if not template_nome:
            template = get_reels_template("problema_solucao")
        else:
            template = get_reels_template(template_nome)
        
        prompt = template.get_prompt(produto, persona.get_context())
        
        return {
            "canal": "reels",
            "template": template.nome,
            "formato": "video60s",
            "persona": persona.nome,
            "prompt_llm": prompt,
            "duracao_segundos": 60,
            "variacao_numero": variacao,
            "produto_id": produto.get('id'),
            "nicho": produto.get('nicho')
        }
    
    def _generate_stories(
        self,
        produto: Dict,
        persona,
        template_nome: Optional[str],
        variacao: int
    ) -> Dict:
        """Gera conteúdo para Stories"""
        if not template_nome:
            template = get_stories_template("produto_desconto")
        else:
            template = get_stories_template(template_nome)
        
        # Stories gera diretamente (não precisa LLM)
        link = produto.get('url_produto', '#')
        conteudo = template.generate(produto, link)
        
        return {
            "canal": "stories",
            "template": template.nome,
            "formato": "stories",
            "persona": persona.nome,
            "conteudo_gerado": conteudo,
            "duracao_segundos": conteudo.get('duracao', 15),
            "variacao_numero": variacao,
            "produto_id": produto.get('id'),
            "nicho": produto.get('nicho')
        }
    
    def _generate_grupo(
        self,
        produto: Dict,
        persona,
        template_nome: Optional[str],
        variacao: int
    ) -> Dict:
        """Gera conteúdo para Grupo Telegram"""
        if not template_nome:
            # Rotaciona entre os 5 templates
            template_names = list(GRUPO_TEMPLATES.keys())
            template = get_grupo_template(template_names[variacao % len(template_names)])
        else:
            template = get_grupo_template(template_nome)
        
        # Grupo gera diretamente
        link = produto.get('url_produto', '#')
        mensagem = template.generate(produto, link)
        
        return {
            "canal": "grupo",
            "template": template.nome,
            "formato": "texto",
            "persona": persona.nome,
            "copy_texto": mensagem,
            "variacao_numero": variacao,
            "produto_id": produto.get('id'),
            "nicho": produto.get('nicho')
        }
    
    def generate_variacoes(
        self,
        canal: str,
        produto: Dict,
        num_variacoes: int = 5
    ) -> List[Dict]:
        """
        Gera múltiplas variações de conteúdo
        
        Args:
            canal: Canal de publicação
            produto: Dados do produto
            num_variacoes: Número de variações a gerar
            
        Returns:
            Lista de conteúdos gerados
        """
        variacoes = []
        
        for i in range(1, num_variacoes + 1):
            try:
                conteudo = self.generate_for_canal(
                    canal=canal,
                    produto=produto,
                    variacao=i
                )
                variacoes.append(conteudo)
                
                logger.debug(
                    "Variação gerada",
                    canal=canal,
                    variacao=i,
                    template=conteudo.get('template')
                )
            except Exception as e:
                logger.error(
                    f"Erro ao gerar variação {i}",
                    canal=canal,
                    error=str(e)
                )
        
        logger.info(
            "Variações geradas",
            canal=canal,
            total=len(variacoes),
            produto_id=produto.get('id')
        )
        
        return variacoes
