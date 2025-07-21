#!/usr/bin/env python3
"""
Запуск AIbox агента на локальной машине
"""

import asyncio
import signal
import sys
import os
from autonomous_agent import AutonomousAgent

class LocalAgentRunner:
    """Запуск агента на локальной машине"""
    
    def __init__(self):
        self.agent = None
        self.running = False
        
    async def start(self):
        """Запустить агента"""
        print("🤖 AIbox Local Agent")
        print("=" * 50)
        
        try:
            # Создать агента
            print("📋 Создание агента...")
            self.agent = AutonomousAgent("AIbox Local Agent", "agent_data")
            
            # Инициализация модулей
            print("🔧 Инициализация модулей...")
            self.agent.initialize_modules()
            
            # Инициализация агента
            print("🎯 Инициализация агента...")
            self.agent.initialize_agent()
            
            print("✅ Агент успешно инициализирован!")
            
            # Показать статус
            status = self.agent.get_status_report()
            print(f"📊 Статус: {status.get('consciousness_cycles', 0)} циклов сознания")
            
            # Запуск цикла сознания
            self.running = True
            print("🧠 Запуск цикла сознания...")
            print("💡 Агент работает. Нажмите Ctrl+C для остановки.")
            
            # Запустить цикл сознания
            consciousness_task = asyncio.create_task(
                self.agent.run_consciousness_cycle()
            )
            
            # Основной цикл мониторинга
            while self.running:
                try:
                    await asyncio.sleep(30)  # Проверка каждые 30 секунд
                    
                    # Показать статус
                    status = self.agent.get_status_report()
                    print(f"📊 Циклов сознания: {status.get('consciousness_cycles', 0)}")
                    
                except KeyboardInterrupt:
                    print("\n🛑 Получен сигнал остановки...")
                    break
                except Exception as e:
                    print(f"❌ Ошибка в основном цикле: {e}")
                    await asyncio.sleep(5)
            
            # Остановка
            print("🔄 Остановка агента...")
            self.agent.stop()
            consciousness_task.cancel()
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            import traceback
            traceback.print_exc()
    
    def stop(self):
        """Остановить агента"""
        self.running = False
        print("🛑 Сигнал остановки отправлен")

async def main():
    """Основная функция"""
    runner = LocalAgentRunner()
    
    # Обработка сигналов
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
    print("🚀 Запуск AIbox агента на локальной машине")
    print("=" * 60)
    
    # Проверить Ollama
    print("🔍 Проверка Ollama...")
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama доступен")
            print("📋 Доступные модели:")
            for line in result.stdout.strip().split('\n')[1:]:  # Пропустить заголовок
                if line.strip():
                    print(f"   {line.strip()}")
        else:
            print("❌ Ollama недоступен")
    except Exception as e:
        print(f"❌ Ошибка проверки Ollama: {e}")
    
    print("\n🎯 Запуск агента...")
    asyncio.run(main()) 