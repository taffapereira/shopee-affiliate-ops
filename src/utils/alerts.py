"""
Sistema de alertas via Telegram para monitoramento
"""
import asyncio
from typing import Optional
from datetime import datetime

from telegram import Bot
from telegram.error import TelegramError

from config.credentials import credentials
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TelegramAlerter:
    """Envia alertas via Telegram para canal de monitoramento"""
    
    def __init__(self):
        self.bot_token = credentials.TELEGRAM_BOT_TOKEN
        self.alert_channel_id = credentials.TELEGRAM_ALERT_CHANNEL_ID
        self.bot: Optional[Bot] = None
        
        if self.bot_token:
            self.bot = Bot(token=self.bot_token)
    
    async def send_alert(
        self,
        message: str,
        level: str = "INFO",
        context: Optional[dict] = None
    ) -> bool:
        """
        Envia um alerta para o canal do Telegram
        
        Args:
            message: Mensagem do alerta
            level: Nível do alerta (INFO, WARNING, ERROR, CRITICAL)
            context: Contexto adicional (dict)
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.bot or not self.alert_channel_id:
            logger.warning("Telegram alerter não configurado")
            return False
        
        try:
            # Emoji baseado no nível
            emoji_map = {
                "INFO": "ℹ️",
                "WARNING": "⚠️",
                "ERROR": "❌",
                "CRITICAL": "🚨"
            }
            emoji = emoji_map.get(level, "📢")
            
            # Formata mensagem
            formatted_message = f"{emoji} *{level}*\n\n{message}"
            
            # Adiciona contexto se existir
            if context:
                formatted_message += "\n\n*Contexto:*\n"
                for key, value in context.items():
                    formatted_message += f"• {key}: {value}\n"
            
            # Adiciona timestamp
            formatted_message += f"\n⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            
            # Envia mensagem
            await self.bot.send_message(
                chat_id=self.alert_channel_id,
                text=formatted_message,
                parse_mode="Markdown"
            )
            
            logger.info("Alerta enviado via Telegram", level=level, message=message)
            return True
            
        except TelegramError as e:
            logger.error(f"Erro ao enviar alerta Telegram: {e}")
            return False
    
    def send_alert_sync(
        self,
        message: str,
        level: str = "INFO",
        context: Optional[dict] = None
    ) -> bool:
        """
        Versão síncrona de send_alert (usa asyncio.run)
        
        Args:
            message: Mensagem do alerta
            level: Nível do alerta
            context: Contexto adicional
            
        Returns:
            True se enviado com sucesso
        """
        try:
            return asyncio.run(self.send_alert(message, level, context))
        except Exception as e:
            logger.error(f"Erro ao enviar alerta sync: {e}")
            return False
    
    async def send_daily_summary(self, summary_data: dict) -> bool:
        """
        Envia resumo diário de operações
        
        Args:
            summary_data: Dados do resumo (produtos coletados, posts criados, etc)
            
        Returns:
            True se enviado com sucesso
        """
        message = "📊 *Resumo Diário - Shopee Affiliate Ops*\n\n"
        
        message += f"🛍️ Produtos coletados: {summary_data.get('produtos_coletados', 0)}\n"
        message += f"⭐ Produtos ranqueados: {summary_data.get('produtos_ranqueados', 0)}\n"
        message += f"✍️ Conteúdos gerados: {summary_data.get('conteudos_gerados', 0)}\n"
        message += f"📱 Posts publicados: {summary_data.get('posts_publicados', 0)}\n"
        message += f"💰 Comissão estimada: R$ {summary_data.get('comissao_estimada', 0):.2f}\n"
        
        return await self.send_alert(message, level="INFO")
    
    async def send_error_alert(self, error: Exception, context: str) -> bool:
        """
        Envia alerta de erro crítico
        
        Args:
            error: Exceção capturada
            context: Contexto onde o erro ocorreu
            
        Returns:
            True se enviado com sucesso
        """
        message = f"Erro no módulo: *{context}*\n\n"
        message += f"Tipo: `{type(error).__name__}`\n"
        message += f"Mensagem: {str(error)}"
        
        return await self.send_alert(message, level="ERROR")


# Instância global
alerter = TelegramAlerter()


def send_alert(message: str, level: str = "INFO", context: Optional[dict] = None) -> bool:
    """
    Função helper para enviar alertas (síncrona)
    
    Args:
        message: Mensagem do alerta
        level: Nível do alerta
        context: Contexto adicional
        
    Returns:
        True se enviado com sucesso
        
    Exemplo:
        >>> send_alert("Coleta finalizada", level="INFO", context={"produtos": 50})
    """
    return alerter.send_alert_sync(message, level, context)
