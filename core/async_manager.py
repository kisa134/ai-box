"""
Централизованный менеджер async операций для AIbox
"""

import asyncio
import threading
import concurrent.futures
from typing import Any, Callable, Coroutine
from contextlib import asynccontextmanager

class AsyncManager:
    """Централизованный менеджер async операций"""
    
    def __init__(self):
        self._loop = None
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self._lock = threading.Lock()
    
    def get_or_create_loop(self) -> asyncio.AbstractEventLoop:
        """Получить или создать event loop"""
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            if self._loop is None or self._loop.is_closed():
                with self._lock:
                    self._loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self._loop)
            return self._loop
    
    async def run_in_thread(self, func: Callable, *args, **kwargs) -> Any:
        """Запустить синхронную функцию в отдельном потоке"""
        loop = self.get_or_create_loop()
        return await loop.run_in_executor(self._executor, func, *args, **kwargs)
    
    async def run_coroutine_safe(self, coro: Coroutine) -> Any:
        """Безопасно запустить корутину"""
        try:
            loop = self.get_or_create_loop()
            return await coro
        except RuntimeError:
            # Если нет запущенного loop, создаем новый
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return await coro
            finally:
                loop.close()
    
    @asynccontextmanager
    async def managed_session(self):
        """Контекстный менеджер для aiohttp сессий"""
        import aiohttp
        session = aiohttp.ClientSession()
        try:
            yield session
        finally:
            await session.close()
    
    def shutdown(self):
        """Завершение работы менеджера"""
        if self._executor:
            self._executor.shutdown(wait=True)

# Глобальный экземпляр
async_manager = AsyncManager() 