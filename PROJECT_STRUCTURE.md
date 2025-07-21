# 📁 Структура Проекта AIbox

## 🎯 **Реорганизация завершена!**

Проект теперь имеет четкую и логичную структуру, где каждый файл находится в правильном месте.

---

## 📂 **Новая Структура:**

### **🤖 Основные компоненты:**
- **`autonomous_agent.py`** - Главный агент с самосознанием
- **`core/`** - 8 когнитивных модулей агента
- **`requirements.txt`** - Основные зависимости

### **🖥️ Приложения (`apps/`):**
- **`desktop/`** - Десктопные приложения
  - `desktop_app.py` - Полноценное GUI приложение
- **`web/`** - Веб-интерфейсы
  - `streamlit_app_full.py` - Полный веб-интерфейс
  - `streamlit_app_simple.py` - Упрощенный интерфейс
  - `streamlit_app.py` - Основной веб-интерфейс
  - `streamlit_app_updated.py` - Обновленный интерфейс
- **`background/`** - Фоновые процессы
  - `run_agent_forever.py` - Постоянная работа агента
  - `run_agent_persistent.py` - Персистентный режим
  - `run_local_agent.py` - Локальный запуск
  - `run_agent_background.py` - Фоновый режим
  - `start_agent.py` - Быстрый старт

### **🔧 Инструменты (`tools/`):**
- `check_gpu.py` - Проверка GPU и CUDA

### **🧪 Тесты (`tests/`):**
- `test_agent_simple.py` - Быстрый тест агента
- `test_agent.py` - Основной тест
- `test_agent_interactive.py` - Интерактивный тест
- `test_chat_interface.py` - Тест чата
- `test_consciousness.py` - Тест сознания
- `test_llm.py` - Тест LLM
- `test_ollama_integration.py` - Тест Ollama
- `simple_ollama_test.py` - Простой тест Ollama
- `demo_ollama_agent.py` - Демо агента
- `quick_test.py` - Быстрый тест

### **📚 Документация (`docs/`):**
- **`guides/`** - Руководства пользователя
  - `FIRST_TESTING_GUIDE.md` - Первое тестирование
  - `DESKTOP_APP_GUIDE.md` - Десктопное приложение
  - `FINAL_WORKING_GUIDE.md` - Рабочая инструкция
  - `FINAL_SETUP_GUIDE.md` - Настройка
  - `LAUNCH_INSTRUCTIONS.md` - Инструкции запуска
  - `LOCAL_SETUP.md` - Локальная настройка
  - `QUICKSTART.md` - Быстрый старт
  - `INSTALL.md` - Установка
  - `CHAT_GUIDE.md` - Руководство по чату
- **`technical/`** - Техническая документация
  - `TECHNICAL_STANDARDS.md` - Технические стандарты
  - `OLLAMA_SETUP.md` - Настройка Ollama
  - `OLLAMA_INTEGRATION_REPORT.md` - Отчет интеграции
  - `TESTING_RESULTS.md` - Результаты тестирования
- **`roadmaps/`** - Планы развития
  - `IMPROVEMENT_RECOMMENDATIONS.md` - Рекомендации
  - `EXPERT_ROADMAP.md` - Экспертный план
  - `NEXT_IMPROVEMENTS_PLAN.md` - План улучшений
  - `PROJECT_OVERVIEW.md` - Обзор проекта
  - `FIRST_DIALOGUES.md` - Первые диалоги

### **⚙️ Конфигурация (`config/`):**
- `config.py` - Основная конфигурация
- `ollama_config.yaml` - Конфигурация Ollama
- `env_example.txt` - Пример переменных окружения
- `requirements_desktop.txt` - Зависимости десктопа

### **📊 Данные (`data/`):**
- `test_reasoning_logs.jsonl` - Логи рассуждений

### **🗂️ Автоматически создаваемые папки:**
- **`agent_data/`** - Данные агента
- **`test_data/`** - Тестовые данные
- **`.venv/`** - Виртуальное окружение

---

## 🚀 **Быстрый доступ:**

### **Основные команды:**
```bash
# Быстрый тест
python tests/test_agent_simple.py

# Десктопное приложение
python apps/desktop/desktop_app.py

# Веб-интерфейс
streamlit run apps/web/streamlit_app_full.py

# Постоянная работа
python apps/background/run_agent_forever.py

# Проверка GPU
python tools/check_gpu.py
```

### **Документация:**
- **Первое тестирование:** `docs/guides/FIRST_TESTING_GUIDE.md`
- **Десктопное приложение:** `docs/guides/DESKTOP_APP_GUIDE.md`
- **Технические стандарты:** `docs/technical/TECHNICAL_STANDARDS.md`

---

## ✅ **Преимущества новой структуры:**

### **🎯 Организация:**
- ✅ Логичное разделение по типам файлов
- ✅ Легкий поиск нужных компонентов
- ✅ Четкая документация
- ✅ Простое навигация

### **🔧 Разработка:**
- ✅ Изолированные тесты
- ✅ Отдельные конфигурации
- ✅ Модульная архитектура
- ✅ Простое добавление новых компонентов

### **📚 Документация:**
- ✅ Структурированные руководства
- ✅ Техническая документация
- ✅ Планы развития
- ✅ Быстрый доступ к информации

### **🚀 Использование:**
- ✅ Понятные пути к файлам
- ✅ Простые команды запуска
- ✅ Четкие инструкции
- ✅ Минимальная путаница

---

## 🎉 **Результат:**

**Проект теперь имеет профессиональную структуру, где:**
- Каждый файл находится в правильном месте
- Легко найти нужные компоненты
- Простое навигация по проекту
- Четкая документация
- Готовность к масштабированию

**AIbox готов к использованию с чистой и организованной структурой!** 🚀✨ 