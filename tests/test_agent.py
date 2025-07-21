#!/usr/bin/env python3
"""
Простой тест для проверки работоспособности автономного агента
"""
import sys

def test_imports():
    """Тест импортов всех модулей"""
    print("🔄 Тестирование импортов...", flush=True)
    
    modules_to_test = [
        ("core.memory_module", "MemoryModule"),
        ("core.goal_module", "GoalModule"),
        ("core.inner_state_module", "InnerStateModule"),
        ("core.world_model_module", "WorldModelModule"),
        ("core.thought_tree_module", "ThoughtTreeModule"),
        ("core.self_model_module", "SelfModelModule"),
        ("autonomous_agent", "AutonomousAgent")
    ]
    
    results = {}
    
    for module_name, class_name in modules_to_test:
        print(f"   Импорт {module_name}...", end=" ", flush=True)
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print("✅ OK")
            results[module_name] = True
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            results[module_name] = False
    
    return results

def test_agent_creation():
    """Тест создания агента"""
    print("\n🔄 Тестирование создания агента...", flush=True)
    
    try:
        print("   Импорт AutonomousAgent...", end=" ", flush=True)
        from autonomous_agent import AutonomousAgent
        print("✅ OK")
        
        print("   Создание агента...", end=" ", flush=True)
        agent = AutonomousAgent("Тестовый Агент", "test_data")
        print("✅ Агент создан")
        
        print("   Тест обработки ввода...", end=" ", flush=True)
        response = agent.process_input("Привет!")
        print(f"✅ Ответ получен: {response[:50]}...")
        
        print("   Получение статуса...", end=" ", flush=True)
        status = agent.get_status_report()
        print(f"✅ Статус: {status['agent_name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_interface():
    """Тест веб-интерфейса"""
    print("\n🔄 Тестирование веб-интерфейса...", flush=True)
    
    try:
        print("   Импорт streamlit_app...", end=" ", flush=True)
        import streamlit_app
        print("✅ Streamlit приложение импортировано")
        return True
    except Exception as e:
        print(f"❌ Ошибка веб-интерфейса: {e}")
        return False

def main():
    """Запуск всех тестов"""
    print("🤖 Тестирование автономного агента с самосознанием")
    print("=" * 60)
    
    # Тест импортов
    import_results = test_imports()
    
    # Подсчет успешных импортов
    successful_imports = sum(import_results.values())
    total_imports = len(import_results)
    
    print(f"\n📊 Результаты импортов: {successful_imports}/{total_imports} успешно")
    
    # Тесты работоспособности
    agent_ok = False
    web_ok = False
    
    if import_results.get("autonomous_agent", False):
        agent_ok = test_agent_creation()
    else:
        print("\n⚠️  Пропуск теста агента - ошибки импорта")
    
    web_ok = test_web_interface()
    
    print("\n" + "=" * 60)
    print("📊 Итоговые результаты:")
    print(f"   Импорты: {successful_imports}/{total_imports}")
    print(f"   Агент: {'✅ OK' if agent_ok else '❌ FAIL'}")
    print(f"   Веб-интерфейс: {'✅ OK' if web_ok else '❌ FAIL'}")
    
    if agent_ok and web_ok:
        print("\n🎉 Все тесты пройдены! Агент готов к работе.")
        print("\nДля запуска:")
        print("   Консоль: python run_agent.py")
        print("   Веб: streamlit run streamlit_app.py")
    else:
        print("\n⚠️  Обнаружены проблемы. Проверьте зависимости:")
        print("   pip install -r requirements.txt")
        
        if not agent_ok:
            print("\nВозможные проблемы:")
            print("   - Отсутствуют зависимости (chromadb, sentence-transformers)")
            print("   - Проблемы с TensorFlow/PyTorch")
            print("   - Недостаточно памяти для загрузки моделей")

if __name__ == "__main__":
    main() 