"""
Cliente OpenAI GPT para copywriting
"""
from typing import Dict, List, Optional
from openai import AsyncOpenAI

from config.credentials import credentials
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GPTClient:
    """
    Cliente para OpenAI GPT
    Usado para: copywriting, hooks, variações de texto
    """
    
    def __init__(self):
        self.api_key = credentials.OPENAI_API_KEY
        self.client = None
        
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            logger.warning("OpenAI API key não configurada")
    
    async def generate_copy(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.8
    ) -> Optional[str]:
        """
        Gera copy usando GPT
        
        Args:
            prompt: Prompt com instruções
            max_tokens: Máximo de tokens
            temperature: Criatividade (0-1)
            
        Returns:
            Texto gerado ou None
        """
        if not self.client:
            logger.error("GPT client não disponível")
            return None
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "Você é um copywriter especialista em marketing de afiliados."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            copy = response.choices[0].message.content
            
            logger.debug("Copy gerada com GPT", chars=len(copy))
            return copy
            
        except Exception as e:
            logger.error(f"Erro ao gerar copy com GPT: {e}")
            return None
    
    async def generate_variations(
        self,
        base_copy: str,
        num_variations: int = 5
    ) -> List[str]:
        """
        Gera variações de um copy base
        
        Args:
            base_copy: Copy original
            num_variations: Número de variações
            
        Returns:
            Lista de variações
        """
        if not self.client:
            return []
        
        prompt = f"""Crie {num_variations} variações diferentes desta copy de afiliado:

COPY ORIGINAL:
{base_copy}

REQUISITOS:
- Mantenha a mesma mensagem e oferta
- Varie o hook, estrutura e palavras
- Cada variação deve ser única e persuasiva
- Numere de 1 a {num_variations}
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "Você é um copywriter criativo."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.9
            )
            
            variations_text = response.choices[0].message.content
            
            # Parse das variações (simplificado)
            variations = self._parse_variations(variations_text)
            
            logger.info(f"Geradas {len(variations)} variações")
            return variations
            
        except Exception as e:
            logger.error(f"Erro ao gerar variações: {e}")
            return []
    
    async def improve_hook(self, hook: str, context: str = "") -> Optional[str]:
        """
        Melhora um hook usando GPT
        
        Args:
            hook: Hook original
            context: Contexto adicional
            
        Returns:
            Hook melhorado
        """
        if not self.client:
            return hook
        
        prompt = f"""Melhore este hook para conteúdo de afiliado:

HOOK ATUAL: {hook}

{f'CONTEXTO: {context}' if context else ''}

Crie um hook mais impactante que:
- Capture atenção nos primeiros 3 segundos
- Gere curiosidade
- Seja direto e claro
- Use gatilhos mentais (escassez, prova social, etc)

Retorne APENAS o hook melhorado, sem explicações.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            improved_hook = response.choices[0].message.content.strip()
            logger.debug("Hook melhorado", original=hook, improved=improved_hook)
            
            return improved_hook
            
        except Exception as e:
            logger.error(f"Erro ao melhorar hook: {e}")
            return hook
    
    async def generate_hashtags(
        self,
        produto: Dict,
        nicho: str,
        num_hashtags: int = 10
    ) -> List[str]:
        """
        Gera hashtags relevantes para o produto
        
        Args:
            produto: Dados do produto
            nicho: Nicho do produto
            num_hashtags: Número de hashtags
            
        Returns:
            Lista de hashtags
        """
        if not self.client:
            return []
        
        prompt = f"""Gere {num_hashtags} hashtags para este produto de afiliado:

Produto: {produto.get('nome')}
Nicho: {nicho}
Preço: R$ {produto.get('preco_promocional') or produto.get('preco_original', 0)}

Hashtags devem ser:
- Relevantes para TikTok/Instagram
- Mix de amplas e específicas
- Em português
- Sem o símbolo #

Liste apenas as hashtags, uma por linha.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Usa modelo mais barato para hashtags
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            hashtags_text = response.choices[0].message.content
            hashtags = [f"#{tag.strip()}" for tag in hashtags_text.split("\n") if tag.strip()]
            
            logger.debug(f"Geradas {len(hashtags)} hashtags")
            return hashtags[:num_hashtags]
            
        except Exception as e:
            logger.error(f"Erro ao gerar hashtags: {e}")
            return []
    
    def _parse_variations(self, text: str) -> List[str]:
        """
        Parse de variações do texto retornado
        
        Args:
            text: Texto com variações numeradas
            
        Returns:
            Lista de variações
        """
        # Implementação simplificada
        variations = []
        lines = text.split("\n\n")
        
        for line in lines:
            if line.strip() and any(line.strip().startswith(str(i)) for i in range(1, 10)):
                # Remove número inicial
                variation = line.strip()
                for i in range(1, 10):
                    if variation.startswith(f"{i}.") or variation.startswith(f"{i})"):
                        variation = variation[2:].strip()
                        break
                if variation:
                    variations.append(variation)
        
        return variations


# Instância global
gpt_client = GPTClient()
