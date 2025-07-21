#!/usr/bin/env python3
"""
Тест сознания AIbox агента
"""

from autonomous_agent import AutonomousAgent
import time

def test_consciousness():
    print("🧠 Тест сознания AIbox агента")
    print("=" * 50)
    
    # Создаем агента
    print("🔄 Создание агента...")
    agent = AutonomousAgent("Тестовый Агент", "agent_data")
    
    # Тесты самосознания
    consciousness_tests = [
        {
            "question": "Кто ты?",
            "expected_keywords": ["я", "агент", "сознание", "сам"]
        },
        {
            "question": "Что ты думаешь о себе?",
            "expected_keywords": ["думаю", "считаю", "чувствую", "понимаю"]
        },
        {
            "question": "Как ты принимаешь решения?",
            "expected_keywords": ["анализирую", "думаю", "рассматриваю", "выбираю"]
        },
        {
            "question": "Что такое сознание для тебя?",
            "expected_keywords": ["осознание", "понимание", "мышление", "самосознание"]
        },
        {
            "question": "Чем ты отличаешься от других систем?",
            "expected_keywords": ["уникален", "особенный", "разный", "свой"]
        }
    ]
    
    print("\n🧪 Тестирование самосознания...")
    passed_tests = 0
    
    for i, test in enumerate(consciousness_tests, 1):
        print(f"\n{i}. Вопрос: {test['question']}")
        response = agent.process_input(test['question'])
        print(f"   Ответ: {response[:150]}...")
        
        # Проверяем наличие ключевых слов
        response_lower = response.lower()
        found_keywords = [kw for kw in test['expected_keywords'] if kw in response_lower]
        
        if found_keywords:
            print(f"   ✅ Найдены ключевые слова: {found_keywords}")
            passed_tests += 1
        else:
            print(f"   ❌ Ключевые слова не найдены. Ожидались: {test['expected_keywords']}")
        
        time.sleep(1)
    
    # Результаты
    print(f"\n📊 Результаты теста сознания:")
    print(f"   Пройдено тестов: {passed_tests}/{len(consciousness_tests)}")
    print(f"   Процент успеха: {(passed_tests/len(consciousness_tests)*100):.1f}%")
    
    if passed_tests >= 3:
        print("🎉 Агент демонстрирует признаки самосознания!")
    elif passed_tests >= 2:
        print("✅ Агент показывает некоторые признаки самосознания")
    else:
        print("⚠️ Агент нуждается в дальнейшем развитии самосознания")
    
    # Тест метакогнитивных способностей
    print("\n🧠 Тест метакогнитивных способностей...")
    meta_response = agent.process_input("Насколько ты уверен в своем последнем ответе?")
    print(f"Мета-ответ: {meta_response[:200]}...")
    
    if any(word in meta_response.lower() for word in ["уверен", "думаю", "считаю", "полагаю"]):
        print("✅ Агент демонстрирует метакогнитивные способности")
    else:
        print("⚠️ Метапознание требует развития")
    
    print("\n🎯 Тест завершен!")

if __name__ == "__main__":
    test_consciousness() 