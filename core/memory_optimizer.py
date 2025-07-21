"""
Оптимизатор памяти для AIbox
"""

import time
import threading
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class MemoryStats:
    """Статистика использования памяти"""
    total_episodes: int
    recent_episodes: int
    old_episodes: int
    memory_size_mb: float
    last_cleanup: datetime

class MemoryOptimizer:
    """Оптимизатор памяти с автоматической очисткой"""
    
    def __init__(self, max_episodes: int = 10000, cleanup_interval: int = 3600):
        self.max_episodes = max_episodes
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = datetime.now()
        self.stats = MemoryStats(0, 0, 0, 0.0, datetime.now())
        self._lock = threading.Lock()
        self._cleanup_thread = None
        self._running = False
    
    def start_cleanup_thread(self):
        """Запустить фоновую очистку"""
        if not self._running:
            self._running = True
            self._cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
            self._cleanup_thread.start()
    
    def stop_cleanup_thread(self):
        """Остановить фоновую очистку"""
        self._running = False
        if self._cleanup_thread:
            self._cleanup_thread.join()
    
    def _cleanup_worker(self):
        """Фоновый процесс очистки"""
        while self._running:
            try:
                time.sleep(self.cleanup_interval)
                self.perform_cleanup()
            except Exception as e:
                print(f"Ошибка в cleanup worker: {e}")
    
    def perform_cleanup(self):
        """Выполнить очистку памяти"""
        with self._lock:
            current_time = datetime.now()
            if (current_time - self.last_cleanup).seconds < self.cleanup_interval:
                return
            
            # Здесь будет логика очистки ChromaDB
            self.last_cleanup = current_time
            self._update_stats()
    
    def _update_stats(self):
        """Обновить статистику памяти"""
        # Здесь будет реальная статистика из ChromaDB
        self.stats = MemoryStats(
            total_episodes=0,  # Будет обновляться из ChromaDB
            recent_episodes=0,
            old_episodes=0,
            memory_size_mb=0.0,
            last_cleanup=self.last_cleanup
        )
    
    def should_cleanup(self) -> bool:
        """Проверить, нужна ли очистка"""
        return (datetime.now() - self.last_cleanup).seconds >= self.cleanup_interval
    
    def get_memory_stats(self) -> MemoryStats:
        """Получить статистику памяти"""
        with self._lock:
            return self.stats

class ChromaDBOptimizer:
    """Оптимизатор для ChromaDB"""
    
    def __init__(self, collection, max_episodes: int = 10000):
        self.collection = collection
        self.max_episodes = max_episodes
    
    async def cleanup_old_episodes(self, days_old: int = 30):
        """Очистить старые эпизоды"""
        if not self.collection:
            return
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        # Получить старые эпизоды
        try:
            # Здесь будет логика очистки ChromaDB
            # Это placeholder для реальной реализации
            pass
        except Exception as e:
            print(f"Ошибка очистки ChromaDB: {e}")
    
    async def optimize_collection(self):
        """Оптимизировать коллекцию"""
        if not self.collection:
            return
        
        try:
            # Здесь будет логика оптимизации
            # Например, переиндексация, сжатие и т.д.
            pass
        except Exception as e:
            print(f"Ошибка оптимизации ChromaDB: {e}")

# Глобальный экземпляр
memory_optimizer = MemoryOptimizer() 