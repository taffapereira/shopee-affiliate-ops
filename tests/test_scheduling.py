"""
Testes para módulo de agendamento
"""
import pytest
from datetime import datetime, time
from zoneinfo import ZoneInfo

from src.scheduling.scheduler import PostScheduler, get_post_slots


class TestPostScheduler:
    """Testes para o agendador de postagens"""
    
    @pytest.fixture
    def scheduler(self):
        """Cria instância do scheduler para testes"""
        return PostScheduler(timezone="America/Sao_Paulo")
    
    def test_get_current_time(self, scheduler):
        """Retorna hora atual no timezone correto"""
        current = scheduler.get_current_time()
        
        assert current is not None
        assert current.tzinfo is not None
        assert "Sao_Paulo" in str(current.tzinfo)
    
    def test_get_next_post_time_returns_datetime(self, scheduler):
        """Retorna próximo horário de postagem"""
        next_time = scheduler.get_next_post_time("grupo")
        
        # Grupo sempre tem horários configurados
        assert next_time is not None
        assert isinstance(next_time, datetime)
    
    def test_get_next_post_time_is_future(self, scheduler):
        """Próximo horário deve ser no futuro"""
        next_time = scheduler.get_next_post_time("grupo")
        current = scheduler.get_current_time()
        
        assert next_time > current
    
    def test_unknown_channel_returns_none(self, scheduler):
        """Canal desconhecido retorna None"""
        next_time = scheduler.get_next_post_time("canal_inexistente")
        
        assert next_time is None
    
    def test_get_todays_schedule(self, scheduler):
        """Retorna horários de hoje"""
        schedule = scheduler.get_todays_schedule("grupo")
        
        assert len(schedule) > 0
        
        # Todos devem ser datetime de hoje
        today = scheduler.get_current_time().date()
        for dt in schedule:
            assert dt.date() == today
    
    def test_get_remaining_posts_today(self, scheduler):
        """Retorna apenas horários futuros de hoje"""
        remaining = scheduler.get_remaining_posts_today("grupo")
        current = scheduler.get_current_time()
        
        for dt in remaining:
            assert dt > current
    
    def test_get_status(self, scheduler):
        """Retorna status do scheduler"""
        status = scheduler.get_status()
        
        assert "running" in status
        assert "current_time" in status
        assert "timezone" in status
        assert "channels" in status


class TestGetPostSlots:
    """Testes para função get_post_slots"""
    
    def test_returns_slots_for_channel(self):
        """Retorna slots para um canal"""
        slots = get_post_slots("grupo")
        
        assert len(slots) > 0
        
        for slot in slots:
            assert "horario" in slot
            assert "datetime" in slot
            assert "status" in slot
            assert "canal" in slot
    
    def test_slot_has_correct_status(self):
        """Slots tem status correto (passed/upcoming)"""
        slots = get_post_slots("grupo")
        
        # Deve ter pelo menos um slot
        assert len(slots) > 0
        
        # Cada slot deve ter status válido
        for slot in slots:
            assert slot["status"] in ["passed", "upcoming"]
    
    def test_unknown_channel_returns_empty(self):
        """Canal desconhecido retorna lista vazia"""
        slots = get_post_slots("canal_inexistente")
        
        assert slots == []


class TestSchedulerIntegration:
    """Testes de integração do scheduler"""
    
    def test_schedule_and_cancel_job(self):
        """Agenda e cancela job"""
        scheduler = PostScheduler()
        
        def dummy_callback():
            pass
        
        # Agenda
        result = scheduler.schedule_daily_posts("grupo", dummy_callback)
        assert result > 0
        
        # Verifica que foi agendado
        assert len(scheduler.scheduled_jobs.get("grupo", [])) > 0
        
        # Cancela
        cancelled = scheduler.cancel_channel_jobs("grupo")
        assert cancelled > 0
        
        # Verifica que foi cancelado
        assert len(scheduler.scheduled_jobs.get("grupo", [])) == 0
    
    def test_cancel_all_jobs(self):
        """Cancela todos os jobs"""
        scheduler = PostScheduler()
        
        def dummy_callback():
            pass
        
        # Agenda em múltiplos canais
        scheduler.schedule_daily_posts("grupo", dummy_callback)
        scheduler.schedule_daily_posts("tiktok", dummy_callback)
        
        # Cancela todos
        total = scheduler.cancel_all_jobs()
        
        assert total > 0
        
        # Verifica que todos foram cancelados
        for channel_jobs in scheduler.scheduled_jobs.values():
            assert len(channel_jobs) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
