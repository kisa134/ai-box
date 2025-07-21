"""
Система кэширования для Ollama
"""

import hashlib
import json
import time
import threading
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class CacheEntry:
    """Запись в кэше"""
    content: str
    model_used: str
    processing_time: float
    tokens_used: int
    confidence: float
    timestamp: datetime
    ttl: int = 3600  # Время жизни в секундах

class OllamaCache:
    """Кэш для результатов Ollama"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self._cleanup_thread = None
        self._running = False
    
    def _generate_key(self, prompt: str, model: str, context: Dict[str, Any] = None) -> str:
        """Генерировать ключ кэша"""
        cache_data = {
            "prompt": prompt,
            "model": model,
            "context": context or {}
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def get(self, prompt: str, model: str, context: Dict[str, Any] = None) -> Optional[CacheEntry]:
        """Получить результат из кэша"""
        key = self._generate_key(prompt, model, context)
        
        with self._lock:
            if key in self.cache:
                entry = self.cache[key]
                if not self._is_expired(entry):
                    return entry
                else:
                    del self.cache[key]
        
        return None
    
    def set(self, prompt: str, model: str, content: str, processing_time: float, 
            tokens_used: int, confidence: float, context: Dict[str, Any] = None, ttl: int = None):
        """Сохранить результат в кэш"""
        key = self._generate_key(prompt, model, context)
        
        with self._lock:
            # Проверить размер кэша
            if len(self.cache) >= self.max_size:
                self._evict_oldest()
            
            entry = CacheEntry(
                content=content,
                model_used=model,
                processing_time=processing_time,
                tokens_used=tokens_used,
                confidence=confidence,
                timestamp=datetime.now(),
                ttl=ttl or self.default_ttl
            )
            
            self.cache[key] = entry
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Проверить, истек ли срок действия записи"""
        return (datetime.now() - entry.timestamp).seconds > entry.ttl
    
    def _evict_oldest(self):
        """Удалить самую старую запись"""
        if not self.cache:
            return
        
        oldest_key = min(self.cache.keys(), 
                        key=lambda k: self.cache[k].timestamp)
        del self.cache[oldest_key]
    
    def cleanup_expired(self):
        """Очистить истекшие записи"""
        with self._lock:
            expired_keys = [
                key for key, entry in self.cache.items()
                if self._is_expired(entry)
            ]
            for key in expired_keys:
                del self.cache[key]
    
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
                time.sleep(300)  # Очистка каждые 5 минут
                self.cleanup_expired()
            except Exception as e:
                print(f"Ошибка в cleanup worker: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику кэша"""
        with self._lock:
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "hit_rate": self._calculate_hit_rate(),
                "oldest_entry": min((entry.timestamp for entry in self.cache.values()), 
                                  default=datetime.now()),
                "newest_entry": max((entry.timestamp for entry in self.cache.values()), 
                                  default=datetime.now())
            }
    
    def _calculate_hit_rate(self) -> float:
        """Рассчитать hit rate кэша"""
        # Это упрощенная версия, в реальности нужно отслеживать hits/misses
        return 0.0  # Placeholder

# Глобальный экземпляр
ollama_cache = OllamaCache() 