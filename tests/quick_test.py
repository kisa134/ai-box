#!/usr/bin/env python3
"""
Быстрый тест AIbox агента
"""

import asyncio
import time
from autonomous_agent import AutonomousAgent

async def quick_test():
    """Быстрый тест агента"""
    
    print("🚀 Быстрый тест AIbox агента")
    print("=" * 40)
    
    try:
        # Создать агента
        print("📋 Создание агента...")
        agent = AutonomousAgent("Quick Test Agent", "test_data")
        
        # Инициализация модулей
        print("🔧 Инициализация модулей...")
        agent.initialize_modules()
        
        # Инициализация агента
        print("🎯 Инициализация агента...")
        agent.initialize_agent()
        
        print("✅ Агент успешно инициализирован!")
        
        # Показать статус
        status = agent.get_status_report()
        print(f"📊 Статус: {status.get('consciousness_cycles', 0)} циклов сознания")
        
        # Простой тест
        print("\n🧪 Тестирование обработки ввода...")
        test_question = "Привет! Как дела?"
        
        start_time = time.time()
        response = await agent.process_input(test_question)
        response_time = time.time() - start_time
        
        print(f"❓ Вопрос: {test_question}")
        print(f"🤖 Ответ ({response_time:.2f}с): {response}")
        
        # Показать финальный статус
        final_status = agent.get_status_report()
        print(f"\n📊 Финальный статус: {final_status.get('consciousness_cycles', 0)} циклов сознания")
        
        print("\n✅ Тест завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка в тесте: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test()) 