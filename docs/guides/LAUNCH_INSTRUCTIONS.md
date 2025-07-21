# 🚀 Инструкции по Запуску AIbox Агента

## 📋 Предварительные Требования

### 1. **Python окружение**
```bash
# Проверить Python версию (нужна 3.8+)
python --version

# Активировать виртуальное окружение (если есть)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

### 3. **Настройка Ollama**
```bash
# Проверить, что Ollama запущен
ollama list

# Если не запущен:
ollama serve
```

### 4. **Проверка доступных моделей**
```bash
# Должны быть доступны:
# - mistral:latest
# - mixtral:latest  
# - llama3:latest
# - phi3:latest
# - deepseek-r1:latest
# - qwen3:latest
```

## 🎯 Способы Запуска

### 1. **Интерактивный Тест (Рекомендуется для начала)**

```bash
python test_agent_interactive.py
```

**Что происходит:**
- Инициализация всех модулей агента
- Автоматические тесты или интерактивный режим
- Мониторинг статуса агента

**Режимы:**
1. **Автоматические тесты** - 10 предустановленных вопросов
2. **Интерактивный режим** - диалог с агентом
3. **Оба режима** - сначала тесты, потом диалог

### 2. **Фоновый Режим (Для длительной работы)**

```bash
python run_agent_background.py
```

**Что происходит:**
- Агент работает в фоне
- Автоматический цикл сознания
- Graceful shutdown при Ctrl+C

### 3. **Streamlit Веб-интерфейс**

```bash
streamlit run streamlit_app.py
```

**Что происходит:**
- Веб-интерфейс на http://localhost:8501
- 6 вкладок мониторинга
- Интерактивный чат с агентом

### 4. **Прямой Тест Ollama**

```bash
python simple_ollama_test.py
```

**Что происходит:**
- Прямое тестирование Ollama
- Проверка доступности моделей
- Тест генерации ответов

## 🔧 Настройка для Локальной Работы

### 1. **Создание директории данных**
```bash
mkdir agent_data
mkdir test_data
```

### 2. **Настройка переменных окружения**
Создайте файл `.env`:
```env
# Для OpenAI (опционально)
OPENAI_API_KEY=your_openai_key_here

# Для локальных моделей (основной режим)
OLLAMA_BASE_URL=http://localhost:11434

# Настройки агента
AGENT_NAME=AIbox Agent
DATA_DIR=agent_data
```

### 3. **Проверка системы**
```bash
# Проверить доступность Ollama
curl http://localhost:11434/api/tags

# Проверить Python модули
python -c "import autonomous_agent; print('✅ Модули загружены')"
```

## 🧪 Тестирование

### 1. **Быстрый тест**
```bash
python test_agent_interactive.py
# Выберите режим 1 (автоматические тесты)
```

### 2. **Полный тест**
```bash
# Запустить фоновый агент
python run_agent_background.py

# В другом терминале запустить интерактивный тест
python test_agent_interactive.py
```

### 3. **Веб-интерфейс**
```bash
streamlit run streamlit_app.py
# Открыть http://localhost:8501
```

## 📊 Мониторинг

### 1. **Статус агента**
```python
from autonomous_agent import AutonomousAgent

agent = AutonomousAgent()
status = agent.get_status_report()
print(f"Циклов сознания: {status.get('consciousness_cycles', 0)}")
```

### 2. **Логи**
- Логи агента: `agent_data/agent.log`
- Логи reasoning: `test_reasoning_logs.jsonl`
- Логи Streamlit: в консоли

### 3. **Ресурсы системы**
```bash
# Мониторинг VRAM (если есть GPU)
nvidia-smi

# Мониторинг памяти
htop  # Linux/Mac
taskmgr  # Windows
```

## 🛠️ Устранение Проблем

### 1. **Ollama не отвечает**
```bash
# Перезапустить Ollama
ollama serve

# Проверить статус
ollama list
```

### 2. **Ошибки импорта**
```bash
# Переустановить зависимости
pip install -r requirements.txt --force-reinstall
```

### 3. **Проблемы с памятью**
```bash
# Очистить кэш Python
python -Bc "import compileall; compileall.compile_dir('.', force=True)"

# Проверить свободное место
df -h  # Linux/Mac
dir     # Windows
```

### 4. **Event loop ошибки**
```bash
# Перезапустить Python процесс
# Или использовать async_manager
```

## 🎯 Рекомендуемый Порядок Запуска

1. **Проверить Ollama:**
   ```bash
   ollama list
   ```

2. **Запустить интерактивный тест:**
   ```bash
   python test_agent_interactive.py
   ```

3. **Если все работает, запустить фоновый режим:**
   ```bash
   python run_agent_background.py
   ```

4. **Для мониторинга запустить веб-интерфейс:**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📈 Производительность

### Ожидаемые показатели:
- **Время инициализации:** 10-30 секунд
- **Время ответа:** 2-10 секунд (зависит от модели)
- **Использование памяти:** 2-8 GB RAM
- **Использование VRAM:** 4-24 GB (зависит от модели)

### Оптимизация:
- Используйте phi3:latest для быстрых ответов
- Используйте mixtral:latest для сложных задач
- Мониторьте ресурсы через веб-интерфейс

## 🎉 Готово!

Теперь у вас есть полностью функциональный AIbox агент с:
- ✅ Исправленными узкими местами
- ✅ AsyncManager для стабильности
- ✅ Кэшированием для производительности
- ✅ Глубокой рефлексией
- ✅ Динамическим обучением
- ✅ Полной интеграцией подсознания

**Удачного тестирования!** 🚀 