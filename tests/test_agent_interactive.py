#!/usr/bin/env python3
"""
Интерактивный тест AIbox агента
"""

import asyncio
import time
from autonomous_agent import AutonomousAgent

class InteractiveAgentTester:
    """Интерактивный тестер агента"""
    
    def __init__(self):
        self.agent = None
        self.test_questions = [
            "Привет! Как дела?",
            "Что такое сознание?",
            "Как ты себя чувствуешь?",
            "Расскажи о своих возможностях",
            "Что ты думаешь об искусственном интеллекте?",
            "Как работает твоя память?",
            "Какие у тебя цели?",
            "Что такое самосознание?",
            "Как ты учишься?",
            "Расскажи о своем подсознании"
        ]
    
    async def initialize_agent(self):
        """Инициализация агента"""
        print("🚀 Инициализация AIbox агента...")
        
        try:
            self.agent = AutonomousAgent("Interactive Test Agent", "test_data")
            
            print("📋 Инициализация модулей...")
            self.agent.initialize_modules()
            
            print("🎯 Инициализация агента...")
            self.agent.initialize_agent()
            
            print("✅ Агент успешно инициализирован!")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка инициализации: {e}")
            return False
    
    async def run_automated_tests(self):
        """Запуск автоматических тестов"""
        print("\n🤖 Запуск автоматических тестов...")
        print("=" * 50)
        
        for i, question in enumerate(self.test_questions, 1):
            print(f"\n🎯 Тест {i}/{len(self.test_questions)}")
            print(f"❓ Вопрос: {question}")
            
            try:
                start_time = time.time()
                response = await self.agent.process_input(question)
                response_time = time.time() - start_time
                
                print(f"🤖 Ответ ({response_time:.2f}с):")
                print(f"   {response}")
                
                # Показать статус агента
                status = self.agent.get_status_report()
                print(f"📊 Статус: {status.get('consciousness_cycles', 0)} циклов сознания")
                
                await asyncio.sleep(2)  # Пауза между вопросами
                
            except Exception as e:
                print(f"❌ Ошибка при обработке вопроса: {e}")
    
    async def run_interactive_mode(self):
        """Интерактивный режим"""
        print("\n💬 Интерактивный режим")
        print("Введите 'quit' для выхода")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 Вы: ")
                
                if user_input.lower() in ['quit', 'exit', 'выход']:
                    print("👋 До свидания!")
                    break
                
                if not user_input.strip():
                    continue
                
                print("🤔 Агент думает...")
                start_time = time.time()
                
                response = await self.agent.process_input(user_input)
                response_time = time.time() - start_time
                
                print(f"🤖 AIbox ({response_time:.2f}с): {response}")
                
                # Показать дополнительную информацию
                if "сознание" in user_input.lower() or "самосознание" in user_input.lower():
                    status = self.agent.get_status_report()
                    print(f"📊 Циклов сознания: {status.get('consciousness_cycles', 0)}")
                
            except KeyboardInterrupt:
                print("\n👋 До свидания!")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    
    async def show_agent_status(self):
        """Показать статус агента"""
        print("\n📊 Статус агента:")
        print("=" * 30)
        
        status = self.agent.get_status_report()
        
        print(f"🧠 Циклов сознания: {status.get('consciousness_cycles', 0)}")
        print(f"🎯 Активных целей: {len(status.get('active_goals', []))}")
        print(f"💾 Эпизодов в памяти: {status.get('episodes_in_memory', 0)}")
        print(f"🌳 Активных мыслей: {status.get('active_thoughts', 0)}")
        
        # Информация о модулях
        print("\n📋 Статус модулей:")
        modules = ['memory', 'goals', 'inner_state', 'world_model', 'thought_tree', 'self_model', 'reasoning_orchestrator', 'subconscious']
        
        for module in modules:
            available = self.agent.is_module_available(module)
            status_icon = "✅" if available else "❌"
            print(f"   {status_icon} {module}: {'Доступен' if available else 'Недоступен'}")

async def main():
    """Основная функция"""
    tester = InteractiveAgentTester()
    
    print("🤖 AIbox Interactive Agent Tester")
    print("=" * 50)
    
    # Инициализация
    if not await tester.initialize_agent():
        print("❌ Не удалось инициализировать агента")
        return
    
    # Показать статус
    await tester.show_agent_status()
    
    # Выбор режима
    print("\n🎯 Выберите режим:")
    print("1. Автоматические тесты")
    print("2. Интерактивный режим")
    print("3. Оба режима")
    
    try:
        choice = input("Введите номер (1-3): ").strip()
        
        if choice == "1":
            await tester.run_automated_tests()
        elif choice == "2":
            await tester.run_interactive_mode()
        elif choice == "3":
            await tester.run_automated_tests()
            await tester.run_interactive_mode()
        else:
            print("❌ Неверный выбор")
            
    except KeyboardInterrupt:
        print("\n👋 Завершение работы...")

if __name__ == "__main__":
    asyncio.run(main()) 