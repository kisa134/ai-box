#!/usr/bin/env python3
"""
Тест интеграции с Ollama для AIbox
"""

import asyncio
import os
import sys
from typing import Dict, Any

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.ollama_module import (
    OllamaClient, 
    ReasoningOrchestrator, 
    ModelType, 
    ReasoningRequest,
    ResourceMonitor,
    ExplainabilityLogger
)
from core.subconscious_module import SubconsciousModule

async def test_ollama_connection():
    """Тест подключения к Ollama"""
    print("🔌 Тест подключения к Ollama")
    print("=" * 50)
    
    client = OllamaClient()
    
    try:
        await client.initialize()
        
        if client.available_models:
            print(f"✅ Подключение успешно! Доступные модели: {list(client.available_models.keys())}")
            
            # Тест генерации
            test_prompt = "Привет! Как дела?"
            result = await client.generate_response(
                prompt=test_prompt,
                model_name=list(client.available_models.keys())[0]
            )
            
            if result["success"]:
                print(f"✅ Генерация успешна!")
                print(f"   Модель: {result['model']}")
                print(f"   Время: {result['processing_time']:.2f}с")
                print(f"   Ответ: {result['content'][:100]}...")
            else:
                print(f"❌ Ошибка генерации: {result['content']}")
        else:
            print("⚠️ Ollama доступен, но модели не обнаружены")
            print("   Убедитесь, что модели загружены: ollama pull mistral:latest")
            
    except Exception as e:
        print(f"❌ Ошибка подключения к Ollama: {e}")
        print("   Убедитесь, что Ollama запущен: ollama serve")

async def test_reasoning_orchestrator():
    """Тест оркестратора reasoning"""
    print("\n🧠 Тест Reasoning Orchestrator")
    print("=" * 50)
    
    orchestrator = ReasoningOrchestrator()
    
    try:
        await orchestrator.initialize()
        
        # Тест различных типов reasoning
        test_requests = [
            ReasoningRequest(
                prompt="Что такое сознание?",
                model_type=ModelType.REASONING,
                context={"emotional_state": "curious"}
            ),
            ReasoningRequest(
                prompt="Как я себя чувствую?",
                model_type=ModelType.REFLECTION,
                context={"current_goal": "самопознание"}
            ),
            ReasoningRequest(
                prompt="Создай историю о роботе",
                model_type=ModelType.CREATIVE,
                context={"emotional_state": "excited"}
            )
        ]
        
        for i, request in enumerate(test_requests, 1):
            print(f"\n{i}. Тест {request.model_type.value}:")
            print(f"   Промпт: {request.prompt}")
            
            request_id = await orchestrator.submit_reasoning_request(request)
            response = await orchestrator.get_reasoning_response(request_id)
            
            if response:
                print(f"   ✅ Ответ получен")
                print(f"   Модель: {response.model_used}")
                print(f"   Уверенность: {response.confidence:.2f}")
                print(f"   Время: {response.processing_time:.2f}с")
                print(f"   Ответ: {response.content[:150]}...")
                
                if response.reasoning_chain:
                    print(f"   Цепочка рассуждений: {len(response.reasoning_chain)} шагов")
            else:
                print(f"   ❌ Ответ не получен")
                
    except Exception as e:
        print(f"❌ Ошибка тестирования оркестратора: {e}")

async def test_subconscious_module():
    """Тест модуля подсознания"""
    print("\n🌙 Тест модуля подсознания")
    print("=" * 50)
    
    orchestrator = ReasoningOrchestrator()
    subconscious = SubconsciousModule("Тестовый Агент")
    
    try:
        await subconscious.initialize(orchestrator)
        
        # Тест обработки сознательных мыслей
        test_thoughts = [
            ("Я думаю о природе сознания", "analysis"),
            ("Мне интересно, как работает мышление", "reflection"),
            ("Хочу создать что-то новое", "creative"),
            ("Вспоминаю важный опыт", "memory")
        ]
        
        for content, thought_type in test_thoughts:
            print(f"\n💭 Обработка мысли: {content}")
            await subconscious.process_conscious_thought(content, thought_type)
        
        # Получить состояние подсознания
        state = subconscious.get_subconscious_state()
        print(f"\n📊 Состояние подсознания:")
        print(f"   Активных мыслей: {state['active_thoughts']}")
        print(f"   Интуиций: {state['intuitions_generated']}")
        print(f"   Паттернов: {state['patterns_discovered']}")
        print(f"   Эмоциональных инсайтов: {state['emotional_insights']}")
        
        if state['recent_intuitions']:
            print(f"   Последние интуиции: {len(state['recent_intuitions'])}")
            
    except Exception as e:
        print(f"❌ Ошибка тестирования подсознания: {e}")

async def test_resource_monitoring():
    """Тест мониторинга ресурсов"""
    print("\n💻 Тест мониторинга ресурсов")
    print("=" * 50)
    
    monitor = ResourceMonitor()
    
    try:
        resources = monitor.get_system_resources()
        
        print(f"📊 Системные ресурсы:")
        print(f"   CPU: {resources.get('cpu_percent', 0):.1f}%")
        print(f"   RAM: {resources.get('ram_percent', 0):.1f}%")
        print(f"   RAM доступно: {resources.get('ram_available_gb', 0):.1f} GB")
        
        gpu_info = resources.get('gpu', {})
        if gpu_info:
            print(f"   GPU: {gpu_info.get('gpu_name', 'Unknown')}")
            print(f"   GPU загрузка: {gpu_info.get('gpu_load', 0):.1f}%")
            print(f"   GPU память: {gpu_info.get('gpu_memory_percent', 0):.1f}%")
            print(f"   GPU память доступно: {gpu_info.get('gpu_memory_available', 0):.1f} GB")
            
            # Тест проверки возможности загрузки модели
            can_load_mistral = monitor.can_load_model(8)  # 8GB для Mistral
            can_load_mixtral = monitor.can_load_model(24)  # 24GB для Mixtral
            
            print(f"   Может загрузить Mistral: {'✅' if can_load_mistral else '❌'}")
            print(f"   Может загрузить Mixtral: {'✅' if can_load_mixtral else '❌'}")
        else:
            print("   GPU: Не обнаружена")
            
    except Exception as e:
        print(f"❌ Ошибка мониторинга ресурсов: {e}")

async def test_explainability_logging():
    """Тест логирования explainability"""
    print("\n📝 Тест логирования explainability")
    print("=" * 50)
    
    logger = ExplainabilityLogger("test_reasoning_logs.jsonl")
    
    try:
        # Создать тестовый запрос и ответ
        from core.ollama_module import ReasoningResponse
        
        test_request = ReasoningRequest(
            prompt="Тестовый запрос",
            model_type=ModelType.REASONING
        )
        
        test_response = ReasoningResponse(
            content="Тестовый ответ",
            model_used="test_model",
            reasoning_chain=["Шаг 1", "Шаг 2"],
            confidence=0.8,
            processing_time=1.5,
            vram_used=0.5,
            explanation={"test": "data"}
        )
        
        # Залогировать
        logger.log_reasoning_request(test_request, test_response)
        print("✅ Запрос залогирован")
        
        # Получить логи
        logs = logger.get_recent_logs(10)
        print(f"✅ Получено {len(logs)} логов")
        
        if logs:
            latest_log = logs[-1]
            print(f"   Последний лог: {latest_log['timestamp']}")
            
    except Exception as e:
        print(f"❌ Ошибка логирования: {e}")

async def test_model_switching():
    """Тест переключения моделей"""
    print("\n🔄 Тест переключения моделей")
    print("=" * 50)
    
    orchestrator = ReasoningOrchestrator()
    
    try:
        await orchestrator.initialize()
        
        # Тест различных типов запросов
        test_scenarios = [
            {
                "name": "Быстрое мышление",
                "request": ReasoningRequest(
                    prompt="Краткий ответ на вопрос",
                    model_type=ModelType.FAST,
                    priority=9
                )
            },
            {
                "name": "Глубокая рефлексия",
                "request": ReasoningRequest(
                    prompt="Глубокая саморефлексия",
                    model_type=ModelType.REFLECTION,
                    priority=8
                )
            },
            {
                "name": "Творческая задача",
                "request": ReasoningRequest(
                    prompt="Создай оригинальную идею",
                    model_type=ModelType.CREATIVE,
                    priority=7
                )
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n🎯 {scenario['name']}:")
            
            request_id = await orchestrator.submit_reasoning_request(scenario['request'])
            response = await orchestrator.get_reasoning_response(request_id)
            
            if response:
                print(f"   ✅ Модель: {response.model_used}")
                print(f"   Время: {response.processing_time:.2f}с")
                print(f"   Уверенность: {response.confidence:.2f}")
            else:
                print(f"   ❌ Ответ не получен")
                
    except Exception as e:
        print(f"❌ Ошибка тестирования переключения моделей: {e}")

async def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование интеграции с Ollama для AIbox")
    print("=" * 60)
    
    # Проверка доступности Ollama
    print("\n📋 Проверка окружения:")
    print(f"   Ollama URL: http://localhost:11434")
    print(f"   Текущая директория: {os.getcwd()}")
    
    # Запуск тестов
    await test_ollama_connection()
    await test_resource_monitoring()
    await test_reasoning_orchestrator()
    await test_subconscious_module()
    await test_explainability_logging()
    await test_model_switching()
    
    print("\n🎯 Тестирование завершено!")
    print("\n📋 Рекомендации:")
    print("1. Убедитесь, что Ollama запущен: ollama serve")
    print("2. Загрузите модели: ollama pull mistral:latest")
    print("3. Проверьте доступность GPU для больших моделей")
    print("4. Настройте переменные окружения в .env")

if __name__ == "__main__":
    asyncio.run(main()) 