"""
Sistema de logging estruturado para toda a aplicação
"""
import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict
from pathlib import Path

from config.credentials import credentials


class StructuredLogger:
    """Logger estruturado que formata logs em JSON"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, credentials.LOG_LEVEL))
        
        # Remove handlers existentes
        self.logger.handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(console_handler)
        
        # File handler
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        )
        file_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(file_handler)
    
    def _log(self, level: str, message: str, **kwargs):
        """Log interno com contexto adicional"""
        extra_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "environment": credentials.ENVIRONMENT,
            **kwargs
        }
        
        log_method = getattr(self.logger, level)
        log_method(message, extra={"data": extra_data})
    
    def info(self, message: str, **kwargs):
        """Log de informação"""
        self._log("info", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log de erro"""
        self._log("error", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log de aviso"""
        self._log("warning", message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log de debug"""
        self._log("debug", message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log crítico"""
        self._log("critical", message, **kwargs)


class JSONFormatter(logging.Formatter):
    """Formata logs em JSON estruturado"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Adiciona dados extras se existirem
        if hasattr(record, "data"):
            log_data.update(record.data)
        
        # Adiciona exception info se existir
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


def get_logger(name: str) -> StructuredLogger:
    """
    Factory function para criar loggers estruturados
    
    Args:
        name: Nome do logger (geralmente __name__)
        
    Returns:
        Instância de StructuredLogger
        
    Exemplo:
        >>> logger = get_logger(__name__)
        >>> logger.info("Produto coletado", produto_id=123, nicho="tech")
    """
    return StructuredLogger(name)
