"""
Cliente Google Gemini para roteiros de vídeo e análise de imagens
"""
from typing import Dict, Optional, List
import google.generativeai as genai

from config.credentials import credentials
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiClient:
    """
    Cliente para Google Gemini
    Usado para: roteiros de vídeo, análise de imagens de produtos
    """
    
    def __init__(self):
        self.api_key = credentials.GOOGLE_API_KEY
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.vision_model = genai.GenerativeModel('gemini-pro-vision')
        else:
            logger.warning("Google API key não configurada")
            self.model = None
            self.vision_model = None
    
    async def generate_video_script(
        self,
        prompt: str,
        duracao_segundos: int = 30
    ) -> Optional[Dict]:
        """
        Gera roteiro de vídeo
        
        Args:
            prompt: Prompt com contexto do produto e persona
            duracao_segundos: Duração do vídeo
            
        Returns:
            Dict com roteiro estruturado
        """
        if not self.model:
            logger.error("Gemini não disponível")
            return None
        
        full_prompt = f"""{prompt}

Crie um roteiro detalhado de vídeo de {duracao_segundos} segundos.

FORMATO DE SAÍDA:
Estruture como:
[0-3s] HOOK: [descrição do que acontece]
[4-10s] DESENVOLVIMENTO: [descrição]
[11-25s] APRESENTAÇÃO: [descrição]
[26-30s] CTA: [descrição]

Inclua também:
- Narração/falas sugeridas
- Descrição visual de cada cena
- Transições
"""
        
        try:
            response = self.model.generate_content(full_prompt)
            
            roteiro = {
                "roteiro_completo": response.text,
                "duracao_segundos": duracao_segundos,
                "cenas": self._parse_scenes(response.text),
                "sucesso": True
            }
            
            logger.info(f"Roteiro gerado com {len(roteiro['cenas'])} cenas")
            return roteiro
            
        except Exception as e:
            logger.error(f"Erro ao gerar roteiro: {e}")
            return None
    
    async def analyze_product_image(self, image_url: str, produto: Dict) -> Optional[Dict]:
        """
        Analisa imagem do produto e sugere ângulos de marketing
        
        Args:
            image_url: URL da imagem
            produto: Dados do produto
            
        Returns:
            Dict com análise da imagem
        """
        if not self.vision_model:
            logger.error("Gemini Vision não disponível")
            return None
        
        prompt = f"""Analise esta imagem de produto:

Nome: {produto.get('nome')}
Categoria: {produto.get('nicho')}

Forneça:
1. Descrição detalhada do que vê na imagem
2. Qualidade percebida (1-10)
3. Principais features visuais
4. Ângulos de marketing baseados na aparência
5. Sugestões de como apresentar em vídeo
"""
        
        try:
            # Em produção, faria download da imagem e enviaria
            # Por ora, apenas simulação
            response = self.model.generate_content(prompt)
            
            return {
                "analise": response.text,
                "produto_id": produto.get('id'),
                "sucesso": True
            }
            
        except Exception as e:
            logger.error(f"Erro ao analisar imagem: {e}")
            return None
    
    async def generate_narration_script(
        self,
        roteiro: str,
        persona: str,
        tom: str
    ) -> Optional[str]:
        """
        Gera script de narração a partir de roteiro
        
        Args:
            roteiro: Roteiro do vídeo
            persona: Nome da persona
            tom: Tom de voz desejado
            
        Returns:
            Script de narração
        """
        if not self.model:
            return None
        
        prompt = f"""Com base neste roteiro de vídeo:

{roteiro}

Crie um script de NARRAÇÃO/FALA para {persona}.

Tom de voz: {tom}

REQUISITOS:
- Apenas as falas, sem descrições de cenas
- Natural e conversacional
- Adequado para TTS (Text-to-Speech)
- Pausas indicadas com [pausa]
- Ênfases indicadas com MAIÚSCULAS
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            logger.info("Script de narração gerado")
            return response.text
            
        except Exception as e:
            logger.error(f"Erro ao gerar narração: {e}")
            return None
    
    def _parse_scenes(self, roteiro: str) -> List[Dict]:
        """
        Parse de cenas do roteiro
        
        Args:
            roteiro: Texto do roteiro
            
        Returns:
            Lista de cenas estruturadas
        """
        cenas = []
        lines = roteiro.split("\n")
        
        for line in lines:
            line = line.strip()
            if "[" in line and "]" in line:
                # Extrai timing e conteúdo
                try:
                    timing_part = line[line.find("[")+1:line.find("]")]
                    content = line[line.find("]")+1:].strip()
                    
                    cenas.append({
                        "timing": timing_part,
                        "conteudo": content
                    })
                except:
                    pass
        
        return cenas


# Instância global
gemini_client = GeminiClient()
