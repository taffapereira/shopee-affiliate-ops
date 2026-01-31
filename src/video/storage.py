"""
Storage de vídeos no Cloudflare R2
"""
import boto3
from typing import Optional
from pathlib import Path

from config.credentials import credentials
from src.utils.logger import get_logger

logger = get_logger(__name__)


class R2Storage:
    """
    Cliente para Cloudflare R2 (compatível com S3)
    """
    
    def __init__(self):
        self.account_id = credentials.R2_ACCOUNT_ID
        self.access_key = credentials.R2_ACCESS_KEY_ID
        self.secret_key = credentials.R2_SECRET_ACCESS_KEY
        self.bucket_name = credentials.R2_BUCKET_NAME
        
        self.client = None
        
        if all([self.account_id, self.access_key, self.secret_key]):
            endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"
            
            self.client = boto3.client(
                's3',
                endpoint_url=endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name='auto'
            )
            logger.info("R2 Storage conectado")
        else:
            logger.warning("Credenciais R2 não configuradas")
    
    def upload_video(
        self,
        local_path: str,
        remote_key: str,
        metadata: dict = None
    ) -> Optional[str]:
        """
        Faz upload de vídeo para R2
        
        Args:
            local_path: Caminho local do vídeo
            remote_key: Chave/caminho no R2
            metadata: Metadata adicional
            
        Returns:
            URL público do vídeo ou None
        """
        if not self.client:
            logger.error("R2 client não disponível")
            return None
        
        try:
            extra_args = {}
            if metadata:
                extra_args['Metadata'] = metadata
            
            # Upload
            self.client.upload_file(
                local_path,
                self.bucket_name,
                remote_key,
                ExtraArgs=extra_args
            )
            
            # Gera URL público
            url = f"https://{self.bucket_name}.r2.dev/{remote_key}"
            
            logger.info("Vídeo enviado para R2", key=remote_key, url=url)
            return url
            
        except Exception as e:
            logger.error(f"Erro ao fazer upload para R2: {e}")
            return None
    
    def get_video_url(self, remote_key: str) -> str:
        """
        Retorna URL público de um vídeo
        
        Args:
            remote_key: Chave do vídeo no R2
            
        Returns:
            URL público
        """
        return f"https://{self.bucket_name}.r2.dev/{remote_key}"
    
    def delete_video(self, remote_key: str) -> bool:
        """
        Deleta vídeo do R2
        
        Args:
            remote_key: Chave do vídeo
            
        Returns:
            True se deletado com sucesso
        """
        if not self.client:
            return False
        
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=remote_key
            )
            logger.info("Vídeo deletado", key=remote_key)
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deletar vídeo: {e}")
            return False
    
    def list_videos(self, prefix: str = "") -> list:
        """
        Lista vídeos no bucket
        
        Args:
            prefix: Prefixo/pasta para filtrar
            
        Returns:
            Lista de chaves de vídeos
        """
        if not self.client:
            return []
        
        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            videos = [obj['Key'] for obj in response.get('Contents', [])]
            logger.info(f"Listados {len(videos)} vídeos")
            
            return videos
            
        except Exception as e:
            logger.error(f"Erro ao listar vídeos: {e}")
            return []


# Instância global
r2_storage = R2Storage()
