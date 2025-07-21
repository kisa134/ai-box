#!/usr/bin/env python3
"""
Демонстрация AIbox агента с Ollama
"""

import asyncio
import time
from autonomous_agent import AutonomousAgent

async def demo_ollama_agent():
    """Демонстрация агента с Ollama"""
    
    print("🚀 Демонстрация AIbox с Ollama")
    print("=" * 50)
    
    # Создать агента
    print("🔄 Создание агента...")
    agent = AutonomousAgent("Ollama Демо Агент", "demo_data")
    
    # Тестовые вопросы для демонстрации разных типов reasoning
    test_questions = [
        {
            "question": "Привет! Как дела?",
            "type": "fast",
            "description": "Быстрый ответ"
        },
        {
            "question": "Что такое сознание?",
            "type": "reasoning", 
            "description": "Логическое рассуждение"
        },
        {
            "question": "Как я себя чувствую?",
            "type": "reflection",
            "description": "Глубокая рефлексия"
        },
        {
            "question": "Создай историю о роботе с сознанием",
            "type": "creative",
            "description": "Творческая задача"
        },
        {
            "question": "Быстро объясни суть искусственного интеллекта",
            "type": "fast",
            "description": "Краткий ответ"
        }
    ]
    
    print(f"\n💬 Начинаем диалог с агентом...")
    print(f"📊 Доступные модели: {len(agent.reasoning_orchestrator.ollama_client.available_models)}")
    
    for i, test in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"🎯 Вопрос {i}: {test['description']}")
        print(f"💭 Тип: {test['type']}")
        print(f"❓ Вопрос: {test['question']}")
        print(f"{'='*60}")
        
        # Получить ответ
        start_time = time.time()
        response = agent.process_input(test['question'])
        response_time = time.time() - start_time
        
        print(f"🤖 Ответ ({response_time:.2f}с):")
        print(f"{response}")
        
        # Показать состояние подсознания
        if agent.is_module_available("subconscious"):
            subconscious_state = agent.subconscious.get_subconscious_state()
            print(f"\n🌙 Подсознание:")
            print(f"   Активных мыслей: {subconscious_state['active_thoughts']}")
            print(f"   Интуиций: {subconscious_state['intuitions_generated']}")
            print(f"   Паттернов: {subconscious_state['patterns_discovered']}")
        
        # Пауза между вопросами
        await asyncio.sleep(2)
    
    # Финальная статистика
    print(f"\n{'='*60}")
    print(f"📊 Финальная статистика:")
    
    if agent.is_module_available("subconscious"):
        final_state = agent.subconscious.get_subconscious_state()
        print(f"   Всего интуиций: {final_state['intuitions_generated']}")
        print(f"   Обнаружено паттернов: {final_state['patterns_discovered']}")
        print(f"   Эмоциональных инсайтов: {final_state['emotional_insights']}")
    
    # Статус агента
    status = agent.get_status_report()
    print(f"   Циклов сознания: {status.get('consciousness_cycles', 0)}")
    print(f"   Активных целей: {len(status.get('active_goals', []))}")
    print(f"   Эпизодов в памяти: {status.get('memory_episodes', 0)}")
    
    print(f"\n🎉 Демонстрация завершена!")
    print(f"🌐 Веб-интерфейс доступен по адресу: http://localhost:8501")

def main():
    """Основная функция"""
    print("🚀 Запуск демонстрации AIbox с Ollama")
    print("=" * 60)
    
    # Проверка Ollama
    print("🔍 Проверка Ollama...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama доступен! Моделей: {len(models)}")
            for model in models:
                print(f"   - {model['name']}")
        else:
            print("❌ Ollama недоступен")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения к Ollama: {e}")
        return
    
    # Запуск демонстрации
    asyncio.run(demo_ollama_agent())

if __name__ == "__main__":
    main() 