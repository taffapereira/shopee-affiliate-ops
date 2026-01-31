"""
Text-to-Speech com Nanobana (ou alternativas)
"""
from typing import Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)


class NanobanaTTS:
    """
    Text-to-Speech usando Nanobana ou alternativas
    
    Nanobana é um modelo TTS. Se não estiver disponível,
    podemos usar alternativas como:
    - Google Text-to-Speech
    - Amazon Polly
    - ElevenLabs
    """
    
    def __init__(self):
        self.tts_provider = "google"  # Fallback para Google TTS
        logger.info(f"TTS Provider: {self.tts_provider}")
    
    async def generate_audio(
        self,
        text: str,
        voice: str = "pt-BR-Wavenet-A",
        speed: float = 1.0
    ) -> Optional[str]:
        """
        Gera áudio a partir de texto
        
        Args:
            text: Texto para converter em fala
            voice: Voz a usar (depende do provider)
            speed: Velocidade da fala (0.5 - 2.0)
            
        Returns:
            Caminho do arquivo de áudio gerado
        """
        if self.tts_provider == "google":
            return await self._google_tts(text, voice, speed)
        else:
            logger.error(f"Provider {self.tts_provider} não implementado")
            return None
    
    async def _google_tts(
        self,
        text: str,
        voice: str,
        speed: float
    ) -> Optional[str]:
        """
        Gera áudio usando Google Text-to-Speech
        
        Args:
            text: Texto para fala
            voice: Voz Google
            speed: Velocidade
            
        Returns:
            Caminho do arquivo
        """
        try:
            from google.cloud import texttospeech
            import os
            
            client = texttospeech.TextToSpeechClient()
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice_params = texttospeech.VoiceSelectionParams(
                language_code="pt-BR",
                name=voice
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speed
            )
            
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config
            )
            
            # Salva áudio
            output_path = f"/tmp/tts_{hash(text)}.mp3"
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            
            logger.info("Áudio gerado", path=output_path, chars=len(text))
            return output_path
            
        except ImportError:
            logger.warning("Google TTS não disponível - instale google-cloud-texttospeech")
            return None
        except Exception as e:
            logger.error(f"Erro ao gerar TTS: {e}")
            return None
    
    def get_available_voices(self, language: str = "pt-BR") -> list:
        """
        Lista vozes disponíveis
        
        Args:
            language: Código do idioma
            
        Returns:
            Lista de vozes disponíveis
        """
        # Vozes Google TTS em PT-BR
        return [
            "pt-BR-Wavenet-A",  # Feminina
            "pt-BR-Wavenet-B",  # Masculina
            "pt-BR-Wavenet-C",  # Feminina
            "pt-BR-Standard-A", # Feminina
            "pt-BR-Standard-B", # Masculina
        ]


# Instância global
nanobana_tts = NanobanaTTS()
