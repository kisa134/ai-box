#!/usr/bin/env python3
"""
Простой запуск AIbox агента в фоновом режиме
"""

import asyncio
import signal
import sys
from autonomous_agent import AutonomousAgent

async def run_agent():
    """Запустить агента в фоновом режиме"""
    
    print("🤖 AIbox Agent - Background Mode")
    print("=" * 50)
    
    # Создать агента
    agent = AutonomousAgent("AIbox Background Agent", "agent_data")
    
    try:
        # Инициализация
        print("📋 Инициализация модулей...")
        agent.initialize_modules()
        
        print("🎯 Инициализация агента...")
        agent.initialize_agent()
        
        print("✅ Агент успешно инициализирован!")
        print("🧠 Запуск цикла сознания...")
        print("💡 Агент работает в фоне. Нажмите Ctrl+C для остановки.")
        
        # Запустить цикл сознания
        await agent.run_consciousness_cycle()
        
    except KeyboardInterrupt:
        print("\n🛑 Получен сигнал остановки...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        print("🔄 Остановка агента...")
        agent.stop()
        print("✅ Агент остановлен")

def signal_handler(signum, frame):
    """Обработчик сигналов"""
    print(f"\n📡 Получен сигнал {signum}")
    sys.exit(0)

if __name__ == "__main__":
    # Настройка обработчиков сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Запуск
    asyncio.run(run_agent()) 