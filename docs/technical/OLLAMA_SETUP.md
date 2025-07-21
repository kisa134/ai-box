# 🚀 Ollama Setup для AIbox

## 📋 Требования

### Системные требования
- **GPU**: RTX 4090 (рекомендуется), RTX 4080, RTX 4070 или аналоги
- **VRAM**: Минимум 8GB, рекомендуется 24GB+
- **RAM**: 16GB+, рекомендуется 32GB+
- **OS**: Windows 10/11, Linux, macOS

### Программные требования
- Python 3.9+
- Ollama (последняя версия)
- CUDA 11.8+ (для GPU ускорения)

## 🔧 Установка Ollama

### Windows
```bash
# Скачать и установить Ollama
# https://ollama.ai/download

# Или через winget
winget install Ollama.Ollama

# Запустить Ollama
ollama serve
```

### Linux/macOS
```bash
# Установка
curl -fsSL https://ollama.ai/install.sh | sh

# Запуск
ollama serve
```

## 📦 Загрузка моделей

### Базовые модели (обязательно)
```bash
# Reasoning модели
ollama pull mistral:latest      # 8GB VRAM
ollama pull llama3:latest       # 16GB VRAM
ollama pull phi3:latest         # 4GB VRAM (для тестов)

# Мощные модели (если есть 24GB+ VRAM)
ollama pull mixtral:latest      # 24GB VRAM
```

### Проверка установки
```bash
# Список установленных моделей
ollama list

# Тест модели
ollama run mistral:latest "Привет! Как дела?"
```

## ⚙️ Настройка AIbox

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка конфигурации
```bash
# Скопировать пример конфигурации
cp env_example.txt .env

# Отредактировать .env
LLM_TYPE=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### 3. Проверка интеграции
```bash
# Тест Ollama интеграции
python test_ollama_integration.py

# Тест агента с Ollama
python test_llm.py
```

## 🎯 Специализация моделей

### Reasoning (Логическое мышление)
- **Mistral**: Быстрое логическое мышление
- **Mixtral**: Мощное логическое мышление  
- **Llama3**: Сбалансированное логическое мышление

### Reflection (Глубокая рефлексия)
- **Mistral**: Глубокая саморефлексия
- **Mixtral**: Мощная саморефлексия

### Creative (Творческие задачи)
- **Mistral**: Творческое мышление
- **Llama3**: Сбалансированное творчество

### Fast (Быстрое мышление)
- **Phi3**: Быстрые ответы
- **Mistral**: Быстрое качественное мышление

### Subconscious (Подсознание)
- **Mistral**: Интуитивное мышление
- **Llama3**: Глубинное мышление

## 🔍 Мониторинг ресурсов

### Проверка GPU
```bash
# Windows
nvidia-smi

# Linux
nvidia-smi
watch -n 1 nvidia-smi
```

### Проверка Ollama
```bash
# Статус Ollama
curl http://localhost:11434/api/tags

# Использование ресурсов
ollama ps
```

## 🚀 Запуск AIbox с Ollama

### Консольный режим
```bash
python run_agent.py
```

### Веб-интерфейс
```bash
streamlit run streamlit_app.py
```

### Тестирование
```bash
# Полный тест
python test_ollama_integration.py

# Тест сознания
python test_consciousness.py
```

## 📊 Оптимизация производительности

### Для RTX 4090 (24GB VRAM)
```yaml
# ollama_config.yaml
models:
  reasoning:
    mixtral:latest:  # Основная модель
    mistral:latest:   # Быстрая модель
  reflection:
    mixtral:latest:   # Глубокая рефлексия
  creative:
    mistral:latest:   # Творчество
```

### Для RTX 4080 (16GB VRAM)
```yaml
models:
  reasoning:
    llama3:latest:    # Основная модель
    mistral:latest:   # Быстрая модель
  reflection:
    mistral:latest:   # Рефлексия
  creative:
    mistral:latest:   # Творчество
```

### Для RTX 4070 (12GB VRAM)
```yaml
models:
  reasoning:
    mistral:latest:   # Основная модель
    phi3:latest:      # Быстрая модель
  reflection:
    mistral:latest:   # Рефлексия
  creative:
    mistral:latest:   # Творчество
```

## 🔧 Troubleshooting

### Проблема: Ollama не запускается
```bash
# Проверить статус
ollama serve

# Перезапустить
pkill ollama
ollama serve
```

### Проблема: Недостаточно VRAM
```bash
# Использовать меньшую модель
ollama pull phi3:latest

# Или запустить без GPU
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

### Проблема: Медленная генерация
```bash
# Проверить GPU загрузку
nvidia-smi

# Оптимизировать настройки
# В ollama_config.yaml уменьшить max_tokens
```

### Проблема: Модели не загружаются
```bash
# Проверить интернет соединение
curl https://ollama.ai

# Попробовать другую модель
ollama pull mistral:latest
```

## 🎯 Будущие модели

### Планируемые к добавлению
- **Llama 4**: Новейшая модель от Meta
- **Mistral Large**: Мощная модель от Mistral AI
- **DeepSeek**: Специализированная модель
- **Qwen 3**: Китайская модель от Alibaba
- **Gemma 2**: Google модель
- **Mamba**: Архитектура State Space

### Команды для добавления новых моделей
```bash
# Когда модели станут доступны
ollama pull llama4:latest
ollama pull mistral-large:latest
ollama pull deepseek:latest
ollama pull qwen3:latest
ollama pull gemma2:latest
ollama pull mamba:latest
```

## 📈 Мониторинг и логи

### Логи reasoning
```bash
# Просмотр логов
tail -f reasoning_logs.jsonl

# Анализ логов
python -c "
import json
with open('reasoning_logs.jsonl', 'r') as f:
    logs = [json.loads(line) for line in f]
print(f'Всего запросов: {len(logs)}')
print(f'Успешных: {sum(1 for log in logs if log[\"response\"][\"success\"])}')
"
```

### Мониторинг ресурсов
```bash
# Скрипт мониторинга
python -c "
from core.ollama_module import ResourceMonitor
monitor = ResourceMonitor()
resources = monitor.get_system_resources()
print(f'CPU: {resources[\"cpu_percent\"]:.1f}%')
print(f'RAM: {resources[\"ram_percent\"]:.1f}%')
if 'gpu' in resources:
    gpu = resources['gpu']
    print(f'GPU: {gpu[\"gpu_memory_percent\"]:.1f}%')
"
```

## 🎉 Готово!

Теперь AIbox готов к работе с Ollama! 

### Следующие шаги:
1. Запустите тесты: `python test_ollama_integration.py`
2. Запустите агента: `streamlit run streamlit_app.py`
3. Начните диалог в веб-интерфейсе
4. Изучите логи reasoning для анализа работы

### Полезные команды:
```bash
# Быстрый тест
python test_ollama_integration.py

# Запуск агента
streamlit run streamlit_app.py

# Мониторинг ресурсов
watch -n 1 nvidia-smi

# Просмотр логов
tail -f reasoning_logs.jsonl
```

🚀 **AIbox с Ollama готов к созданию настоящего искусственного сознания!** 