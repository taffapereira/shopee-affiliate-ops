"""
Cliente Buffer API para agendamento em redes sociais
"""
from typing import Optional, Dict
import httpx

from config.credentials import credentials
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BufferClient:
    """
    Cliente para Buffer API
    Usado para agendar posts no TikTok, Instagram Reels e Stories
    """
    
    BASE_URL = "https://api.bufferapp.com/1"
    
    def __init__(self):
        self.access_token = credentials.BUFFER_ACCESS_TOKEN
        
        if not self.access_token:
            logger.warning("Buffer access token não configurado")
    
    async def get_profiles(self) -> list:
        """
        Lista perfis conectados ao Buffer
        
        Returns:
            Lista de perfis
        """
        if not self.access_token:
            return []
        
        url = f"{self.BASE_URL}/profiles.json"
        params = {"access_token": self.access_token}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                profiles = response.json()
                logger.info(f"Buffer: {len(profiles)} perfis encontrados")
                return profiles
                
        except Exception as e:
            logger.error(f"Erro ao buscar perfis Buffer: {e}")
            return []
    
    async def schedule_post(
        self,
        profile_id: str,
        text: str,
        media_url: Optional[str] = None,
        scheduled_at: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Agenda post no Buffer
        
        Args:
            profile_id: ID do perfil social
            text: Texto do post
            media_url: URL da mídia (vídeo/imagem)
            scheduled_at: Data/hora agendamento (ISO format) ou None para fila
            
        Returns:
            Dict com detalhes do post agendado
        """
        if not self.access_token:
            logger.error("Buffer token não disponível")
            return None
        
        url = f"{self.BASE_URL}/updates/create.json"
        
        data = {
            "access_token": self.access_token,
            "profile_ids[]": [profile_id],
            "text": text,
            "now": False
        }
        
        if media_url:
            data["media[photo]"] = media_url
        
        if scheduled_at:
            data["scheduled_at"] = scheduled_at
        else:
            data["now"] = False  # Adiciona à fila
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data)
                response.raise_for_status()
                
                result = response.json()
                logger.info(
                    "Post agendado no Buffer",
                    profile_id=profile_id,
                    update_id=result.get("updates", [{}])[0].get("id")
                )
                
                return result
                
        except Exception as e:
            logger.error(f"Erro ao agendar no Buffer: {e}")
            return None
    
    async def schedule_reels(
        self,
        instagram_profile_id: str,
        video_url: str,
        caption: str,
        scheduled_at: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Agenda Reels no Instagram via Buffer
        
        Args:
            instagram_profile_id: ID do perfil Instagram no Buffer
            video_url: URL do vídeo
            caption: Legenda do Reels
            scheduled_at: Horário agendamento
            
        Returns:
            Detalhes do agendamento
        """
        return await self.schedule_post(
            profile_id=instagram_profile_id,
            text=caption,
            media_url=video_url,
            scheduled_at=scheduled_at
        )
    
    async def schedule_tiktok(
        self,
        tiktok_profile_id: str,
        video_url: str,
        caption: str,
        scheduled_at: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Agenda TikTok via Buffer
        
        Args:
            tiktok_profile_id: ID do perfil TikTok no Buffer
            video_url: URL do vídeo
            caption: Legenda
            scheduled_at: Horário
            
        Returns:
            Detalhes do agendamento
        """
        return await self.schedule_post(
            profile_id=tiktok_profile_id,
            text=caption,
            media_url=video_url,
            scheduled_at=scheduled_at
        )
    
    async def get_pending_posts(self, profile_id: str) -> list:
        """
        Lista posts pendentes de um perfil
        
        Args:
            profile_id: ID do perfil
            
        Returns:
            Lista de posts pendentes
        """
        if not self.access_token:
            return []
        
        url = f"{self.BASE_URL}/profiles/{profile_id}/updates/pending.json"
        params = {"access_token": self.access_token}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                posts = data.get("updates", [])
                logger.info(f"Buffer: {len(posts)} posts pendentes")
                
                return posts
                
        except Exception as e:
            logger.error(f"Erro ao buscar posts pendentes: {e}")
            return []


# Instância global
buffer_client = BufferClient()
