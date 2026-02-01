"""
Sistema de agendamento de publicações
Gerencia horários de postagem para diferentes canais
"""
from datetime import datetime, time, timedelta
from typing import List, Dict, Optional, Callable
from zoneinfo import ZoneInfo
import schedule
import threading

from config.constants import HORARIOS_PUBLICACAO
from config.credentials import credentials
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PostScheduler:
    """
    Agendador de publicações para diferentes canais
    
    Gerencia horários de postagem baseado na configuração em constants.py
    """
    
    def __init__(self, timezone: str = None):
        """
        Inicializa o agendador
        
        Args:
            timezone: Timezone para os horários (default: America/Sao_Paulo)
        """
        self.timezone = ZoneInfo(timezone or credentials.TIMEZONE)
        self.scheduled_jobs: Dict[str, List] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
    
    def get_current_time(self) -> datetime:
        """
        Retorna a hora atual no timezone configurado
        
        Returns:
            datetime no timezone configurado
        """
        return datetime.now(self.timezone)
    
    def get_next_post_time(self, canal: str) -> Optional[datetime]:
        """
        Calcula o próximo horário de postagem para um canal
        
        Args:
            canal: Nome do canal (tiktok, reels, stories, grupo)
            
        Returns:
            datetime do próximo horário ou None se canal não configurado
        """
        horarios = HORARIOS_PUBLICACAO.get(canal, [])
        
        if not horarios:
            logger.warning(f"Nenhum horário configurado para canal: {canal}")
            return None
        
        now = self.get_current_time()
        today = now.date()
        
        # Converte horários string para time objects e ordena
        times = sorted([
            time.fromisoformat(h) for h in horarios
        ])
        
        # Procura próximo horário hoje
        for t in times:
            next_dt = datetime.combine(today, t, tzinfo=self.timezone)
            if next_dt > now:
                return next_dt
        
        # Se não há mais horários hoje, pega o primeiro de amanhã
        tomorrow = today + timedelta(days=1)
        first_time = times[0]
        return datetime.combine(tomorrow, first_time, tzinfo=self.timezone)
    
    def get_todays_schedule(self, canal: str) -> List[datetime]:
        """
        Retorna todos os horários de postagem de hoje para um canal
        
        Args:
            canal: Nome do canal
            
        Returns:
            Lista de datetimes para hoje
        """
        horarios = HORARIOS_PUBLICACAO.get(canal, [])
        today = self.get_current_time().date()
        
        return [
            datetime.combine(today, time.fromisoformat(h), tzinfo=self.timezone)
            for h in horarios
        ]
    
    def get_remaining_posts_today(self, canal: str) -> List[datetime]:
        """
        Retorna horários de postagem restantes para hoje
        
        Args:
            canal: Nome do canal
            
        Returns:
            Lista de datetimes restantes hoje
        """
        now = self.get_current_time()
        todays = self.get_todays_schedule(canal)
        
        return [dt for dt in todays if dt > now]
    
    def schedule_post(
        self,
        canal: str,
        callback: Callable,
        *args,
        **kwargs
    ) -> bool:
        """
        Agenda uma postagem para o próximo horário disponível
        
        Args:
            canal: Nome do canal
            callback: Função a ser executada
            *args, **kwargs: Argumentos para o callback
            
        Returns:
            True se agendado com sucesso
        """
        next_time = self.get_next_post_time(canal)
        
        if not next_time:
            return False
        
        # Converte para string de horário para o schedule
        time_str = next_time.strftime('%H:%M')
        
        job = schedule.every().day.at(time_str).do(callback, *args, **kwargs)
        
        if canal not in self.scheduled_jobs:
            self.scheduled_jobs[canal] = []
        self.scheduled_jobs[canal].append(job)
        
        logger.info(
            "Postagem agendada",
            canal=canal,
            horario=time_str,
            data=next_time.strftime('%Y-%m-%d')
        )
        
        return True
    
    def schedule_daily_posts(
        self,
        canal: str,
        callback: Callable,
        *args,
        **kwargs
    ) -> int:
        """
        Agenda postagens para todos os horários do dia de um canal
        
        Args:
            canal: Nome do canal
            callback: Função a ser executada
            *args, **kwargs: Argumentos para o callback
            
        Returns:
            Número de postagens agendadas
        """
        horarios = HORARIOS_PUBLICACAO.get(canal, [])
        count = 0
        
        if canal not in self.scheduled_jobs:
            self.scheduled_jobs[canal] = []
        
        for horario in horarios:
            job = schedule.every().day.at(horario).do(callback, *args, **kwargs)
            self.scheduled_jobs[canal].append(job)
            count += 1
            
            logger.info(
                "Postagem diária agendada",
                canal=canal,
                horario=horario
            )
        
        return count
    
    def cancel_channel_jobs(self, canal: str) -> int:
        """
        Cancela todos os jobs de um canal
        
        Args:
            canal: Nome do canal
            
        Returns:
            Número de jobs cancelados
        """
        jobs = self.scheduled_jobs.get(canal, [])
        count = len(jobs)
        
        for job in jobs:
            schedule.cancel_job(job)
        
        self.scheduled_jobs[canal] = []
        
        logger.info(f"Cancelados {count} jobs do canal {canal}")
        return count
    
    def cancel_all_jobs(self) -> int:
        """
        Cancela todos os jobs agendados
        
        Returns:
            Número total de jobs cancelados
        """
        total = 0
        for canal in list(self.scheduled_jobs.keys()):
            total += self.cancel_channel_jobs(canal)
        
        return total
    
    def _run_scheduler(self):
        """Loop interno do scheduler"""
        while self._running:
            schedule.run_pending()
            # Dorme 30 segundos entre checks
            import time as time_module
            time_module.sleep(30)
    
    def start(self, blocking: bool = False):
        """
        Inicia o scheduler
        
        Args:
            blocking: Se True, bloqueia a thread atual
        """
        self._running = True
        
        if blocking:
            logger.info("Iniciando scheduler (modo bloqueante)")
            self._run_scheduler()
        else:
            logger.info("Iniciando scheduler (modo background)")
            self._thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self._thread.start()
    
    def stop(self):
        """Para o scheduler"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Scheduler parado")
    
    def get_status(self) -> Dict:
        """
        Retorna status do scheduler
        
        Returns:
            Dict com informações de status
        """
        now = self.get_current_time()
        
        status = {
            "running": self._running,
            "current_time": now.isoformat(),
            "timezone": str(self.timezone),
            "channels": {}
        }
        
        for canal in HORARIOS_PUBLICACAO.keys():
            next_post = self.get_next_post_time(canal)
            remaining = self.get_remaining_posts_today(canal)
            
            status["channels"][canal] = {
                "next_post": next_post.isoformat() if next_post else None,
                "remaining_today": len(remaining),
                "scheduled_jobs": len(self.scheduled_jobs.get(canal, []))
            }
        
        return status


def get_post_slots(canal: str, date: datetime = None) -> List[Dict]:
    """
    Retorna slots de postagem para um canal em uma data específica
    
    Args:
        canal: Nome do canal
        date: Data (default: hoje)
        
    Returns:
        Lista de slots com horário e status
    """
    scheduler = PostScheduler()
    
    if date is None:
        date = scheduler.get_current_time()
    
    horarios = HORARIOS_PUBLICACAO.get(canal, [])
    slots = []
    
    now = scheduler.get_current_time()
    
    for horario in horarios:
        slot_time = datetime.combine(
            date.date(),
            time.fromisoformat(horario),
            tzinfo=scheduler.timezone
        )
        
        slots.append({
            "horario": horario,
            "datetime": slot_time.isoformat(),
            "status": "passed" if slot_time < now else "upcoming",
            "canal": canal
        })
    
    return slots


# Instância global do scheduler
post_scheduler = PostScheduler()
