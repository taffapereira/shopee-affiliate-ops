"""
Cliente DeepSeek para análise e ranking de produtos
"""
from typing import Dict, List, Optional
import httpx

from config.credentials import credentials
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DeepSeekClient:
    """
    Cliente para API DeepSeek
    Usado para: análise de produtos, ranking, otimização
    """
    
    def __init__(self):
        self.api_key = credentials.DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1"
        
        if not self.api_key:
            logger.warning("DeepSeek API key não configurada")
    
    async def analyze_product(self, produto: Dict) -> Dict:
        """
        Analisa um produto e sugere estratégias
        
        Args:
            produto: Dados do produto
            
        Returns:
            Dict com análise e sugestões
        """
        if not self.api_key:
            return {"error": "API key não configurada"}
        
        prompt = self._build_analysis_prompt(produto)
        
        try:
            response = await self._call_api(prompt)
            
            return {
                "analise": response.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "produto_id": produto.get("id"),
                "sucesso": True
            }
        except Exception as e:
            logger.error(f"Erro ao analisar produto: {e}")
            return {"error": str(e), "sucesso": False}
    
    async def rank_products(self, produtos: List[Dict]) -> List[Dict]:
        """
        Ranqueia produtos usando análise de IA
        
        Args:
            produtos: Lista de produtos
            
        Returns:
            Produtos ranqueados com scores
        """
        if not self.api_key:
            logger.warning("DeepSeek não disponível, usando ranking básico")
            return produtos
        
        prompt = self._build_ranking_prompt(produtos)
        
        try:
            response = await self._call_api(prompt)
            analysis = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Parse da resposta e atualiza scores
            ranked_products = self._parse_ranking_response(analysis, produtos)
            
            logger.info("Produtos ranqueados com DeepSeek", total=len(ranked_products))
            return ranked_products
            
        except Exception as e:
            logger.error(f"Erro ao ranquear com DeepSeek: {e}")
            return produtos
    
    async def optimize_performance(self, analytics_data: Dict) -> Dict:
        """
        Analisa dados de performance e sugere otimizações
        
        Args:
            analytics_data: Dados de analytics
            
        Returns:
            Dict com sugestões de otimização
        """
        if not self.api_key:
            return {"error": "API key não configurada"}
        
        prompt = f"""Analise os seguintes dados de performance de afiliado Shopee e sugira otimizações:

{analytics_data}

Forneça insights sobre:
1. Quais canais estão performando melhor
2. Quais nichos devem receber mais foco
3. Produtos com melhor taxa de conversão
4. Sugestões de melhoria
"""
        
        try:
            response = await self._call_api(prompt)
            
            return {
                "otimizacoes": response.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "sucesso": True
            }
        except Exception as e:
            logger.error(f"Erro ao otimizar: {e}")
            return {"error": str(e), "sucesso": False}
    
    async def _call_api(self, prompt: str, max_tokens: int = 1000) -> Dict:
        """
        Chama a API DeepSeek
        
        Args:
            prompt: Prompt para o modelo
            max_tokens: Máximo de tokens na resposta
            
        Returns:
            Resposta da API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    def _build_analysis_prompt(self, produto: Dict) -> str:
        """Constrói prompt de análise de produto"""
        return f"""Analise este produto de afiliado Shopee:

Nome: {produto.get('nome')}
Preço: R$ {produto.get('preco_promocional') or produto.get('preco_original', 0)}
Comissão: {produto.get('comissao_percentual', 0)}%
Rating: {produto.get('rating', 0)}⭐
Vendas: {produto.get('total_vendas', 0)}
Nicho: {produto.get('nicho')}

Forneça:
1. Potencial de conversão (0-100)
2. Principais pontos de venda
3. Ângulo de marketing recomendado
4. Público-alvo ideal
"""
    
    def _build_ranking_prompt(self, produtos: List[Dict]) -> str:
        """Constrói prompt de ranking"""
        produtos_resumo = "\n".join([
            f"{i+1}. {p.get('nome')} - R${p.get('preco_promocional', 0):.2f} - {p.get('comissao_percentual', 0)}% comissão"
            for i, p in enumerate(produtos[:20])  # Limita a 20 produtos
        ])
        
        return f"""Ranqueie estes produtos de afiliado por potencial de conversão e lucratividade:

{produtos_resumo}

Para cada produto, atribua um score de 0-100 e explique o motivo.
Formato: produto_numero|score|motivo
"""
    
    def _parse_ranking_response(self, response: str, produtos: List[Dict]) -> List[Dict]:
        """
        Parse da resposta de ranking
        
        Args:
            response: Resposta do LLM
            produtos: Produtos originais
            
        Returns:
            Produtos com scores atualizados
        """
        # Implementação simplificada - retorna produtos originais
        # Em produção, faria parse real da resposta
        return produtos


# Instância global
deepseek_client = DeepSeekClient()
