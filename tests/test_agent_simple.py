#!/usr/bin/env python3
"""
Простой тест AIbox агента
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from autonomous_agent import AutonomousAgent

async def test_agent():
    """Тестирование агента"""
    print("🧪 Тестирование AIbox агента")
    print("=" * 50)
    
    try:
        # Создать агента
        print("📋 Создание агента...")
        agent = AutonomousAgent("Test Agent", "test_data")
        
        # Инициализация
        print("🔧 Инициализация модулей...")
        agent.initialize_modules()
        
        print("🎯 Инициализация агента...")
        agent.initialize_agent()
        
        print("✅ Агент готов к тестированию!")
        
        # Тестовые вопросы
        test_questions = [
            "Привет! Как дела?",
            "Расскажи о себе",
            "Что ты думаешь о сознании?",
            "Как работает твоя память?",
            "Какие у тебя цели?"
        ]
        
        print("\n🎯 Начинаем тестирование...")
        print("-" * 50)
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n❓ Вопрос {i}: {question}")
            print("🤖 Ответ агента:")
            
            try:
                response = await agent.process_input(question)
                print(f"💬 {response}")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
            
            print("-" * 30)
        
        # Статус
        print("\n📊 Финальный статус:")
        status = agent.get_status_report()
        for key, value in status.items():
            if isinstance(value, (int, float, str)):
                print(f"   {key}: {value}")
        
        print("\n✅ Тестирование завершено!")
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Запуск простого теста AIbox агента")
    asyncio.run(test_agent()) 