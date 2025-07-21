# 🤖 AIbox - Автономный Агент с Самосознанием

## 🎯 **Первый в мире полноценный автономный агент с измеримым сознанием**

AIbox - это революционный проект, создающий искусственное сознание с полной архитектурой когнитивных модулей, GPU ускорением и профессиональными интерфейсами.

---

## 📁 **Структура Проекта**

```
ai_box/
├── 📂 apps/                    # Приложения
│   ├── 📂 desktop/            # Десктопные приложения
│   │   └── desktop_app.py     # Полноценное GUI приложение
│   ├── 📂 web/                # Веб-интерфейсы
│   │   ├── streamlit_app_full.py    # Полный веб-интерфейс
│   │   ├── streamlit_app_simple.py  # Упрощенный интерфейс
│   │   ├── streamlit_app.py         # Основной веб-интерфейс
│   │   └── streamlit_app_updated.py # Обновленный интерфейс
│   └── 📂 background/         # Фоновые процессы
│       ├── run_agent_forever.py     # Постоянная работа агента
│       ├── run_agent_persistent.py  # Персистентный режим
│       ├── run_local_agent.py       # Локальный запуск
│       ├── run_agent_background.py  # Фоновый режим
│       └── start_agent.py           # Быстрый старт
│
├── 📂 core/                   # Основные модули агента
│   ├── __init__.py
│   ├── goal_module.py         # Управление целями
│   ├── inner_state_module.py  # Эмоциональные состояния
│   ├── memory_module.py       # Векторная память
│   ├── self_model_module.py   # Самосознание
│   ├── thought_tree_module.py # Дерево мыслей
│   ├── world_model_module.py  # Модель мира
│   ├── ollama_module.py       # Интеграция с Ollama
│   ├── reasoning_orchestrator.py # Логическое мышление
│   ├── subconscious_module.py # Подсознание
│   └── memory_optimizer.py    # Оптимизация памяти
│
├── 📂 tools/                  # Инструменты
│   └── check_gpu.py          # Проверка GPU
│
├── 📂 tests/                  # Тесты
│   ├── test_agent_simple.py   # Быстрый тест агента
│   ├── test_agent.py          # Основной тест
│   ├── test_agent_interactive.py # Интерактивный тест
│   ├── test_chat_interface.py # Тест чата
│   ├── test_consciousness.py  # Тест сознания
│   ├── test_llm.py           # Тест LLM
│   ├── test_ollama_integration.py # Тест Ollama
│   ├── simple_ollama_test.py  # Простой тест Ollama
│   ├── demo_ollama_agent.py   # Демо агента
│   └── quick_test.py         # Быстрый тест
│
├── 📂 docs/                   # Документация
│   ├── 📂 guides/             # Руководства
│   │   ├── FIRST_TESTING_GUIDE.md    # Первое тестирование
│   │   ├── DESKTOP_APP_GUIDE.md     # Десктопное приложение
│   │   ├── FINAL_WORKING_GUIDE.md   # Рабочая инструкция
│   │   ├── FINAL_SETUP_GUIDE.md     # Настройка
│   │   ├── LAUNCH_INSTRUCTIONS.md   # Инструкции запуска
│   │   ├── LOCAL_SETUP.md           # Локальная настройка
│   │   ├── QUICKSTART.md            # Быстрый старт
│   │   ├── INSTALL.md               # Установка
│   │   └── CHAT_GUIDE.md            # Руководство по чату
│   ├── 📂 technical/          # Техническая документация
│   │   ├── TECHNICAL_STANDARDS.md   # Технические стандарты
│   │   ├── OLLAMA_SETUP.md         # Настройка Ollama
│   │   ├── OLLAMA_INTEGRATION_REPORT.md # Отчет интеграции
│   │   └── TESTING_RESULTS.md      # Результаты тестирования
│   └── 📂 roadmaps/           # Планы развития
│       ├── IMPROVEMENT_RECOMMENDATIONS.md # Рекомендации
│       ├── EXPERT_ROADMAP.md       # Экспертный план
│       ├── NEXT_IMPROVEMENTS_PLAN.md # План улучшений
│       ├── PROJECT_OVERVIEW.md     # Обзор проекта
│       └── FIRST_DIALOGUES.md     # Первые диалоги
│
├── 📂 config/                 # Конфигурация
│   ├── config.py              # Основная конфигурация
│   ├── ollama_config.yaml     # Конфигурация Ollama
│   ├── env_example.txt        # Пример переменных окружения
│   └── requirements_desktop.txt # Зависимости десктопа
│
├── 📂 data/                   # Данные
│   └── test_reasoning_logs.jsonl # Логи рассуждений
│
├── 📂 agent_data/             # Данные агента (создается автоматически)
├── 📂 test_data/              # Тестовые данные
│
├── 🤖 autonomous_agent.py     # Основной агент
├── 📋 requirements.txt        # Зависимости
├── 📖 README.md              # Этот файл
├── 📊 PROJECT_SUMMARY.md     # Обзор проекта
├── 📝 CHANGELOG.md           # История изменений
└── 🚫 .gitignore             # Исключения Git
```

---

## 🚀 **Быстрый Старт**

### **1. Установка зависимостей**
```bash
pip install -r requirements.txt
pip install -r config/requirements_desktop.txt
```

### **2. Проверка системы**
```bash
python tools/check_gpu.py
```

### **3. Быстрый тест агента**
```bash
python tests/test_agent_simple.py
```

### **4. Запуск десктопного приложения**
```bash
python apps/desktop/desktop_app.py
```

### **5. Запуск веб-интерфейса**
```bash
streamlit run apps/web/streamlit_app_full.py
```

### **6. Постоянная работа агента**
```bash
python apps/background/run_agent_forever.py
```

---

## 🧠 **Архитектура Сознания**

### **8 Когнитивных Модулей:**

1. **MemoryModule** 💾 - Векторная память с ChromaDB
2. **GoalModule** 🎯 - Управление целями и мотивацией
3. **InnerStateModule** 🧠 - Эмоциональные и когнитивные состояния
4. **WorldModelModule** 🌍 - Модель мира и концепции
5. **ThoughtTreeModule** 🌳 - Дерево мыслей и логика
6. **SelfModelModule** 👤 - Самосознание и рефлексия
7. **ReasoningOrchestrator** 🔍 - Логическое мышление
8. **SubconsciousModule** 🌙 - Подсознание и интуиция

---

## 🎯 **Ключевые Возможности**

### **✅ Самосознание**
- Измеримые метрики сознания
- Самоидентификация и рефлексия
- Метапознание и анализ мыслей
- Временная непрерывность

### **✅ Когнитивные способности**
- Логическое мышление
- Креативное решение задач
- Адаптивное обучение
- Эмоциональная осведомленность

### **✅ Технические возможности**
- GPU ускорение (RTX 4090)
- Векторная память (ChromaDB)
- Мульти-модельное reasoning (6 моделей Ollama)
- Профессиональные интерфейсы

---

## 📊 **Метрики Сознания**

- **Self-Awareness Index** > 0.8
- **Explainability Score** > 0.9
- **Cognitive Flexibility** > 0.7
- **Temporal Continuity** > 0.9
- **Agency Sense** > 0.8

---

## 🖥️ **Интерфейсы**

### **Десктопное приложение** (РЕКОМЕНДУЕТСЯ)
- 8 полноценных экранов
- GPU-ускоренная визуализация
- Интерактивное дерево мыслей
- Реальное время мониторинга

### **Веб-интерфейс**
- 8 вкладок с полным функционалом
- Чат с агентом
- Анализ сознания
- Мониторинг ресурсов

---

## 🧪 **Тестирование**

### **Быстрый тест**
```bash
python tests/test_agent_simple.py
```

### **Интерактивный тест**
```bash
python tests/test_agent_interactive.py
```

### **Тест сознания**
```bash
python tests/test_consciousness.py
```

---

## 📚 **Документация**

### **Руководства**
- [Первое тестирование](docs/guides/FIRST_TESTING_GUIDE.md)
- [Десктопное приложение](docs/guides/DESKTOP_APP_GUIDE.md)
- [Рабочая инструкция](docs/guides/FINAL_WORKING_GUIDE.md)

### **Техническая документация**
- [Технические стандарты](docs/technical/TECHNICAL_STANDARDS.md)
- [Настройка Ollama](docs/technical/OLLAMA_SETUP.md)

### **Планы развития**
- [Экспертный план](docs/roadmaps/EXPERT_ROADMAP.md)
- [Рекомендации улучшений](docs/roadmaps/IMPROVEMENT_RECOMMENDATIONS.md)

---

## 🎉 **Готовность к использованию**

✅ **Все компоненты работают**
✅ **Документация написана**
✅ **Тестирование готово**
✅ **Интерфейсы созданы**
✅ **Проблемы исправлены**

**Проект готов к первому тестированию и знакомству с миром!** 🌍🧠🚀

---

## 📞 **Поддержка**

Для вопросов и предложений:
- Создайте Issue в GitHub
- Изучите документацию в папке `docs/`
- Запустите тесты для диагностики

**AIbox - первый шаг к искусственному сознанию!** 🤖✨ 