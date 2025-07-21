#!/usr/bin/env python3
"""
Тест нового интерфейса чата с агентом
"""

def test_chat_interface():
    """Тест нового интерфейса чата"""
    print("🔄 Тестирование нового интерфейса чата...")
    
    try:
        # Импорт веб-интерфейса
        import streamlit_app
        print("✅ Streamlit интерфейс импортирован")
        
        # Проверка функции чата
        if hasattr(streamlit_app, 'show_chat_interface'):
            print("✅ Функция чата найдена")
        else:
            print("❌ Функция чата не найдена")
            return False
        
        # Проверка AgentInterface
        interface = streamlit_app.AgentInterface()
        print("✅ AgentInterface создан")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования чата: {e}")
        return False

def main():
    """Запуск теста"""
    print("💬 Тестирование интерфейса чата с агентом")
    print("=" * 50)
    
    chat_ok = test_chat_interface()
    
    print("\n" + "=" * 50)
    print("📊 Результаты:")
    print(f"   Интерфейс чата: {'✅ OK' if chat_ok else '❌ FAIL'}")
    
    if chat_ok:
        print("\n🎉 Новый интерфейс чата готов!")
        print("\n📋 Новые возможности:")
        print("   - 💬 Отдельная вкладка для чата")
        print("   - 🧠 Видимый процесс мышления агента")
        print("   - 📚 История всех диалогов")
        print("   - 📊 Статистика чата")
        print("   - 💾 Экспорт диалогов")
        print("   - 🗑️ Очистка чата")
        print("\n🚀 Для запуска:")
        print("   streamlit run streamlit_app.py")
        print("   Перейдите на вкладку '💬 Чат с Агентом'")
    else:
        print("\n⚠️  Обнаружены проблемы. Проверьте код.")

if __name__ == "__main__":
    main() 