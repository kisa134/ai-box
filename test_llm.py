#!/usr/bin/env python3
"""
Тест языковой модели для AIbox агента
"""

import os
from core.llm_module import LLMModule, OpenAILLM, LocalLLM
from config import Config

def test_llm_availability():
    """Тест доступности языковых моделей"""
    print("🧠 Тест доступности языковых моделей")
    print("=" * 50)
    
    # Тест OpenAI
    print("\n1. Тест OpenAI LLM:")
    openai_llm = OpenAILLM()
    if openai_llm.is_available():
        print("✅ OpenAI доступен")
        
        # Тест генерации
        response = openai_llm.generate_response("Привет! Как дела?")
        print(f"   Ответ: {response[:100]}...")
    else:
        print("❌ OpenAI недоступен (проверьте OPENAI_API_KEY)")
    
    # Тест локальной модели
    print("\n2. Тест локальной модели:")
    try:
        local_llm = LocalLLM()
        if local_llm.is_available():
            print("✅ Локальная модель доступна")
            
            # Тест генерации
            response = local_llm.generate_response("Привет! Как дела?")
            print(f"   Ответ: {response[:100]}...")
        else:
            print("❌ Локальная модель недоступна")
    except Exception as e:
        print(f"❌ Ошибка загрузки локальной модели: {e}")
    
    # Тест LLM модуля
    print("\n3. Тест LLM модуля:")
    llm_module = LLMModule(llm_type="openai")
    if llm_module.is_available():
        print("✅ LLM модуль работает с OpenAI")
    else:
        print("⚠️ LLM модуль использует fallback")
    
    llm_module_local = LLMModule(llm_type="local")
    if llm_module_local.is_available():
        print("✅ LLM модуль работает с локальной моделью")
    else:
        print("⚠️ LLM модуль использует fallback для локальной модели")

def test_agent_with_llm():
    """Тест агента с LLM"""
    print("\n🤖 Тест агента с LLM")
    print("=" * 50)
    
    from autonomous_agent import AutonomousAgent
    
    # Создаем агента
    print("🔄 Создание агента...")
    agent = AutonomousAgent("Тестовый Агент", "agent_data")
    
    # Тестируем диалог
    test_questions = [
        "Привет! Как тебя зовут?",
        "Расскажи о себе",
        "Что ты думаешь о сознании?",
        "Как ты принимаешь решения?",
        "Чем ты отличаешься от других систем?"
    ]
    
    print("\n💬 Тест диалога:")
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Вопрос: {question}")
        response = agent.process_input(question)
        print(f"   Ответ: {response[:200]}...")
        
        # Проверяем качество ответа
        if len(response) > 50 and not response.startswith("Извините"):
            print("   ✅ Качественный ответ")
        else:
            print("   ⚠️ Простой ответ (возможно, fallback)")

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование языковых моделей для AIbox")
    
    # Проверяем конфигурацию
    print("\n📋 Проверка конфигурации:")
    if Config.validate_config():
        print("✅ Конфигурация корректна")
    else:
        print("⚠️ Проблемы с конфигурацией")
    
    # Тестируем доступность LLM
    test_llm_availability()
    
    # Тестируем агента с LLM
    test_agent_with_llm()
    
    print("\n🎯 Тест завершен!")

if __name__ == "__main__":
    main() 