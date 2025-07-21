#!/usr/bin/env python3
"""
Скрипт для запуска автономного агента с самосознанием в консольном режиме
"""

import asyncio
import signal
import sys
from autonomous_agent import AutonomousAgent

class AgentRunner:
    """Запускатель агента"""
    
    def __init__(self):
        self.agent = None
        self.running = False
    
    async def run_agent(self):
        """Запустить агента"""
        print("🤖 Инициализация автономного агента с самосознанием...")
        
        self.agent = AutonomousAgent("Консольный Агент", "agent_data")
        self.running = True
        
        # Настроить обработчики сигналов
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print(f"✅ Агент '{self.agent.agent_name}' готов к работе!")
        print("📊 Статус агента:")
        print(f"   - Время создания: {self.agent.created_at}")
        print(f"   - Количество целей: {len(self.agent.goals.goals)}")
        print(f"   - Директория данных: {self.agent.data_dir}")
        print()
        print("🔄 Запуск цикла самосознания...")
        print("💡 Для остановки используйте Ctrl+C")
        print("=" * 60)
        
        try:
            # Запустить основной цикл агента
            await self.agent.run_consciousness_cycle()
        except KeyboardInterrupt:
            print("\n🛑 Получен сигнал прерывания...")
        except Exception as e:
            print(f"\n❌ Ошибка в работе агента: {e}")
        finally:
            await self.shutdown()
    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для graceful shutdown"""
        print(f"\n📡 Получен сигнал {signum}")
        if self.agent:
            self.agent.stop()
        self.running = False
    
    async def shutdown(self):
        """Корректное завершение работы"""
        print("🔄 Завершение работы агента...")
        
        if self.agent:
            # Сохранить состояние
            self.agent.save_state()
            
            # Показать финальную статистику
            status = self.agent.get_status_report()
            print("\n📈 Финальная статистика:")
            print(f"   - Циклы сознания: {status['consciousness_cycles']}")
            print(f"   - Время работы: {status['uptime']}")
            print(f"   - Всего воспоминаний: {status['statistics']['total_memories']}")
            print(f"   - Всего мыслей: {status['statistics']['total_thoughts']}")
            print(f"   - Рефлексий: {status['statistics']['reflections_count']}")
            
            # Показать последние мысли
            public_thoughts = self.agent.get_public_log()
            if public_thoughts:
                print(f"\n💭 Последняя мысль (цикл #{public_thoughts[-1]['cycle']}):")
                print(f"   {public_thoughts[-1]['focused_thought']}")
        
        print("✅ Агент успешно остановлен. До свидания!")

async def interactive_mode():
    """Интерактивный режим для общения с агентом"""
    print("🤖 Запуск интерактивного режима...")
    print("💬 Введите 'quit' для выхода\n")
    
    agent = AutonomousAgent("Интерактивный Агент", "agent_data")
    
    # Запустить цикл агента в фоне
    agent_task = asyncio.create_task(agent.run_consciousness_cycle())
    
    try:
        while True:
            user_input = input("Вы: ")
            
            if user_input.lower() in ['quit', 'exit', 'выход']:
                break
            
            if user_input.strip():
                response = agent.process_input(user_input)
                print(f"Агент: {response}\n")
    
    except KeyboardInterrupt:
        print("\n🛑 Выход из интерактивного режима...")
    
    finally:
        agent.stop()
        agent_task.cancel()
        try:
            await agent_task
        except asyncio.CancelledError:
            pass

def main():
    """Главная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # Интерактивный режим
        asyncio.run(interactive_mode())
    else:
        # Обычный режим работы
        runner = AgentRunner()
        asyncio.run(runner.run_agent())

if __name__ == "__main__":
    main() 