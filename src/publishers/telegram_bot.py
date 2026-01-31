"""
Bot Telegram para publicação em grupos
"""
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError

from config.credentials import credentials
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TelegramPublisher:
    """
    Publisher para grupos Telegram
    """
    
    def __init__(self):
        self.bot_token = credentials.TELEGRAM_BOT_TOKEN
        self.bot: Optional[Bot] = None
        
        if self.bot_token:
            self.bot = Bot(token=self.bot_token)
        else:
            logger.warning("Telegram bot token não configurado")
    
    async def publish_to_group(
        self,
        group_id: str,
        message: str,
        image_url: Optional[str] = None,
        parse_mode: str = "Markdown"
    ) -> bool:
        """
        Publica mensagem em grupo Telegram
        
        Args:
            group_id: ID do grupo
            message: Mensagem a enviar
            image_url: URL da imagem (opcional)
            parse_mode: Modo de parse (Markdown ou HTML)
            
        Returns:
            True se publicado com sucesso
        """
        if not self.bot:
            logger.error("Telegram bot não disponível")
            return False
        
        try:
            if image_url:
                await self.bot.send_photo(
                    chat_id=group_id,
                    photo=image_url,
                    caption=message,
                    parse_mode=parse_mode
                )
            else:
                await self.bot.send_message(
                    chat_id=group_id,
                    text=message,
                    parse_mode=parse_mode,
                    disable_web_page_preview=False
                )
            
            logger.info("Mensagem publicada no Telegram", group_id=group_id)
            return True
            
        except TelegramError as e:
            logger.error(f"Erro ao publicar no Telegram: {e}")
            return False
    
    async def publish_to_nicho(
        self,
        nicho: str,
        message: str,
        image_url: Optional[str] = None
    ) -> bool:
        """
        Publica em grupo específico de um nicho
        
        Args:
            nicho: Nome do nicho (casa, tech, pet, cosmeticos)
            message: Mensagem
            image_url: URL da imagem
            
        Returns:
            True se publicado
        """
        group_id = credentials.get_telegram_group_id(nicho)
        
        if not group_id:
            logger.error(f"Grupo não configurado para nicho: {nicho}")
            return False
        
        return await self.publish_to_group(group_id, message, image_url)
    
    async def schedule_message(
        self,
        group_id: str,
        message: str,
        delay_seconds: int
    ) -> bool:
        """
        Agenda mensagem para publicação futura
        
        Args:
            group_id: ID do grupo
            message: Mensagem
            delay_seconds: Atraso em segundos
            
        Returns:
            True se agendado
        """
        # Em produção, usaria scheduler como APScheduler ou Celery
        logger.info(
            "Mensagem agendada",
            group_id=group_id,
            delay=delay_seconds
        )
        
        # Por ora, apenas log
        return True
    
    def get_group_info(self, group_id: str) -> Optional[dict]:
        """
        Obtém informações do grupo
        
        Args:
            group_id: ID do grupo
            
        Returns:
            Dict com informações ou None
        """
        if not self.bot:
            return None
        
        try:
            import asyncio
            chat = asyncio.run(self.bot.get_chat(group_id))
            
            return {
                "id": chat.id,
                "title": chat.title,
                "type": chat.type,
                "member_count": chat.get_member_count() if hasattr(chat, 'get_member_count') else None
            }
        except Exception as e:
            logger.error(f"Erro ao obter info do grupo: {e}")
            return None


# Instância global
telegram_publisher = TelegramPublisher()
