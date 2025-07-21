#!/usr/bin/env python3
"""
Простой тест Ollama для AIbox
"""

import asyncio
import time
from core.ollama_module import OllamaClient, ReasoningOrchestrator, ModelType, ReasoningRequest

async def test_ollama_direct():
    """Прямой тест Ollama"""
    
    print("🚀 Прямой тест Ollama")
    print("=" * 50)
    
    # Создать клиент
    client = OllamaClient()
    await client.initialize()
    
    print(f"✅ Доступные модели: {list(client.available_models.keys())}")
    
    # Тестовые вопросы
    test_questions = [
        ("Привет! Как дела?", ModelType.FAST),
        ("Что такое сознание?", ModelType.REASONING),
        ("Как я себя чувствую?", ModelType.REFLECTION),
        ("Создай историю о роботе", ModelType.CREATIVE)
    ]
    
    for i, (question, model_type) in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"🎯 Вопрос {i}: {question}")
        print(f"💭 Тип: {model_type.value}")
        print(f"{'='*60}")
        
        # Создать запрос
        request = ReasoningRequest(
            prompt=question,
            model_type=model_type,
            context={},
            priority=8,
            require_explanation=True
        )
        
        # Отправить запрос напрямую
        start_time = time.time()
        result = await client.generate_response(
            prompt=request.prompt,
            model_name="phi3:latest",  # Используем phi3 для теста
            temperature=0.7
        )
        response_time = time.time() - start_time
        
        if result and result.get('success'):
            print(f"🤖 Ответ ({response_time:.2f}с):")
            print(f"Модель: {result.get('model', 'unknown')}")
            print(f"Время обработки: {result.get('processing_time', 0):.2f}с")
            print(f"Токенов использовано: {result.get('tokens_used', 0)}")
            print(f"\nОтвет:\n{result.get('content', '')[:500]}...")
        else:
            print("❌ Ошибка получения ответа")
            print(f"Ошибка: {result.get('content', 'Unknown error')}")
        
        await asyncio.sleep(1)
    
    print(f"\n🎉 Тест завершен!")
    
    # Закрыть клиент
    await client.close()

def main():
    """Основная функция"""
    print("🚀 Запуск прямого теста Ollama")
    
    # Запустить async тест
    asyncio.run(test_ollama_direct())

if __name__ == "__main__":
    main() 