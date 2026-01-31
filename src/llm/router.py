"""
Router de LLMs - Decide qual LLM usar para cada tarefa
"""
from typing import Dict, Optional
from enum import Enum

from src.llm.deepseek_client import deepseek_client
from src.llm.gpt_client import gpt_client
from src.llm.gemini_client import gemini_client
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LLMTask(Enum):
    """Tipos de tarefas para LLMs"""
    RANKING = "ranking"
    ANALYSIS = "analysis"
    COPYWRITING = "copywriting"
    VARIATIONS = "variations"
    HASHTAGS = "hashtags"
    VIDEO_SCRIPT = "video_script"
    IMAGE_ANALYSIS = "image_analysis"
    NARRATION = "narration"


class LLMRouter:
    """
    Roteia requisições para o LLM apropriado baseado na tarefa
    
    Distribuição:
    - DeepSeek: Ranking, Análise de dados, Otimização
    - GPT: Copywriting, Hooks, Variações de texto
    - Gemini: Roteiros de vídeo, Análise de imagens
    """
    
    def __init__(self):
        self.deepseek = deepseek_client
        self.gpt = gpt_client
        self.gemini = gemini_client
    
    async def execute(self, task: LLMTask, **kwargs) -> Optional[Dict]:
        """
        Executa uma tarefa com o LLM apropriado
        
        Args:
            task: Tipo de tarefa
            **kwargs: Parâmetros específicos da tarefa
            
        Returns:
            Resultado da tarefa
        """
        if task == LLMTask.RANKING:
            return await self._handle_ranking(**kwargs)
        elif task == LLMTask.ANALYSIS:
            return await self._handle_analysis(**kwargs)
        elif task == LLMTask.COPYWRITING:
            return await self._handle_copywriting(**kwargs)
        elif task == LLMTask.VARIATIONS:
            return await self._handle_variations(**kwargs)
        elif task == LLMTask.HASHTAGS:
            return await self._handle_hashtags(**kwargs)
        elif task == LLMTask.VIDEO_SCRIPT:
            return await self._handle_video_script(**kwargs)
        elif task == LLMTask.IMAGE_ANALYSIS:
            return await self._handle_image_analysis(**kwargs)
        elif task == LLMTask.NARRATION:
            return await self._handle_narration(**kwargs)
        else:
            logger.error(f"Tarefa desconhecida: {task}")
            return None
    
    async def _handle_ranking(self, produtos: list, **kwargs) -> Optional[Dict]:
        """Ranking de produtos com DeepSeek"""
        ranked = await self.deepseek.rank_products(produtos)
        return {"produtos_ranqueados": ranked}
    
    async def _handle_analysis(self, produto: Dict, **kwargs) -> Optional[Dict]:
        """Análise de produto com DeepSeek"""
        return await self.deepseek.analyze_product(produto)
    
    async def _handle_copywriting(self, prompt: str, **kwargs) -> Optional[Dict]:
        """Copywriting com GPT"""
        copy = await self.gpt.generate_copy(prompt, **kwargs)
        return {"copy": copy}
    
    async def _handle_variations(self, base_copy: str, num: int = 5, **kwargs) -> Optional[Dict]:
        """Variações de copy com GPT"""
        variations = await self.gpt.generate_variations(base_copy, num)
        return {"variacoes": variations}
    
    async def _handle_hashtags(self, produto: Dict, nicho: str, **kwargs) -> Optional[Dict]:
        """Geração de hashtags com GPT"""
        hashtags = await self.gpt.generate_hashtags(produto, nicho, **kwargs)
        return {"hashtags": hashtags}
    
    async def _handle_video_script(self, prompt: str, duracao: int = 30, **kwargs) -> Optional[Dict]:
        """Roteiro de vídeo com Gemini"""
        return await self.gemini.generate_video_script(prompt, duracao)
    
    async def _handle_image_analysis(self, image_url: str, produto: Dict, **kwargs) -> Optional[Dict]:
        """Análise de imagem com Gemini"""
        return await self.gemini.analyze_product_image(image_url, produto)
    
    async def _handle_narration(self, roteiro: str, persona: str, tom: str, **kwargs) -> Optional[Dict]:
        """Script de narração com Gemini"""
        script = await self.gemini.generate_narration_script(roteiro, persona, tom)
        return {"narration_script": script}
    
    def get_available_llms(self) -> Dict[str, bool]:
        """
        Verifica quais LLMs estão disponíveis
        
        Returns:
            Dict com status de cada LLM
        """
        return {
            "deepseek": self.deepseek.api_key is not None,
            "gpt": self.gpt.client is not None,
            "gemini": self.gemini.model is not None
        }


# Instância global
llm_router = LLMRouter()
