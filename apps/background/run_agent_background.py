#!/usr/bin/env python3
"""
Скрипт для запуска AIbox агента в фоновом режиме
"""

import asyncio
import time
import signal
import sys
from autonomous_agent import AutonomousAgent

class BackgroundAgentRunner:
    """Запуск агента в фоновом режиме"""
    
    def __init__(self, agent_name: str = "AIbox Agent"):
        self.agent = AutonomousAgent(agent_name, "agent_data")
        self.running = False
        
    async def start(self):
        """Запустить агента"""
        print("🚀 Запуск AIbox агента...")
        
        try:
            # Инициализация агента
            print("📋 Инициализация модулей...")
            self.agent.initialize_modules()
            
            print("🎯 Инициализация агента...")
            self.agent.initialize_agent()
            
            print("✅ Агент успешно инициализирован!")
            
            # Запуск цикла сознания
            self.running = True
            print("🧠 Запуск цикла сознания...")
            
            # Запустить цикл сознания в фоне
            consciousness_task = asyncio.create_task(
                self.agent.run_consciousness_cycle()
            )
            
            # Основной цикл работы
            while self.running:
                try:
                    # Проверить статус агента
                    status = self.agent.get_status_report()
                    print(f"📊 Статус: {status.get('consciousness_cycles', 0)} циклов сознания")
                    
                    await asyncio.sleep(30)  # Проверка каждые 30 секунд
                    
                except KeyboardInterrupt:
                    print("\n🛑 Получен сигнал остановки...")
                    break
                except Exception as e:
                    print(f"❌ Ошибка в основном цикле: {e}")
                    await asyncio.sleep(5)
            
            # Остановка агента
            print("🔄 Остановка агента...")
            self.agent.stop()
            consciousness_task.cancel()
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            sys.exit(1)
    
    def stop(self):
        """Остановить агента"""
        self.running = False
        print("🛑 Сигнал остановки отправлен")

async def main():
    """Основная функция"""
    runner = BackgroundAgentRunner("AIbox Background Agent")
    
    # Обработка сигналов для graceful shutdown
    def signal_handler(signum, frame):
        print(f"\n📡 Получен сигнал {signum}")
        runner.stop()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await runner.start()
    except KeyboardInterrupt:
        print("\n👋 Завершение работы...")
    finally:
        print("✅ Агент остановлен")

if __name__ == "__main__":
    print("🤖 AIbox Background Agent Runner")
    print("=" * 50)
    
    # Запуск
    asyncio.run(main()) 