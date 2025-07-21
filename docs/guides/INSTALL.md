# 📦 Инструкции по Установке

## 🚀 Быстрая Установка

### 1. Установка Python
Убедитесь, что у вас установлен Python 3.11 или выше:
```bash
python --version
```

### 2. Установка Зависимостей
```bash
pip install -r requirements.txt
```

### 3. Проверка Работоспособности
```bash
python test_agent.py
```

### 4. Запуск
```bash
# Консольный режим
python run_agent.py

# Веб-интерфейс
streamlit run streamlit_app.py

# Интерактивный режим
python run_agent.py --interactive
```

## 🔧 Устранение Проблем

### Ошибки с ChromaDB
Если возникают проблемы с ChromaDB:
```bash
pip install --upgrade chromadb
```

### Ошибки с SentenceTransformers
Для работы векторной памяти:
```bash
pip install sentence-transformers torch
```

### Ошибки с Streamlit
```bash
pip install --upgrade streamlit plotly
```

### Ошибки с NetworkX
```bash
pip install networkx matplotlib
```

## 🖥️ Для Windows

Если возникают проблемы с компиляцией:
```powershell
# Установка Visual Studio Build Tools
# Или использование conda
conda install chromadb sentence-transformers
```

## 🐧 Для Linux/Mac

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev build-essential

# macOS с Homebrew
brew install python

# Установка зависимостей
pip3 install -r requirements.txt
```

## 📋 Минимальные Требования

### Системные Требования
- **Python**: 3.11+
- **RAM**: 4GB (рекомендуется 8GB)
- **Диск**: 2GB свободного места
- **Интернет**: для загрузки моделей SentenceTransformers

### Версии Пакетов
- `streamlit >= 1.29.0`
- `chromadb >= 0.4.0`
- `sentence-transformers >= 2.2.0`
- `plotly >= 5.17.0`
- `networkx >= 3.2.0`

## 🔍 Диагностика

### Проверка Установки
```bash
python -c "import streamlit, chromadb, sentence_transformers; print('Все модули установлены')"
```

### Проверка GPU (опционально)
```bash
python -c "import torch; print(f'CUDA доступен: {torch.cuda.is_available()}')"
```

### Лог Ошибок
Если агент не запускается, проверьте:
1. `agent_data/agent.log` - основные логи
2. Консольный вывод при запуске
3. Версии Python и пакетов

## ⚠️ Известные Проблемы

### 1. Медленная Загрузка
При первом запуске SentenceTransformers загружает модели (~500MB).
Это нормально и происходит только один раз.

### 2. Предупреждения TensorFlow
Предупреждения TensorFlow можно игнорировать или отключить:
```bash
export TF_CPP_MIN_LOG_LEVEL=2
```

### 3. Проблемы с Портами
Если порт 8501 занят (Streamlit):
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 🐳 Docker (опционально)

Можно использовать Docker для изоляции окружения:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "run_agent.py"]
```

## 💡 Советы по Оптимизации

### Для Слабых Машин
1. Уменьшите интервал рефлексии в `autonomous_agent.py`:
   ```python
   self.reflection_interval = 600  # 10 минут вместо 5
   ```

2. Отключите сложные визуализации в веб-интерфейсе

3. Используйте более простую модель для векторизации:
   ```python
   self.encoder = SentenceTransformer('all-MiniLM-L12-v2')  # Меньше размер
   ```

### Для Мощных Машин
1. Увеличьте размер памяти
2. Используйте GPU для ускорения
3. Включите более частые рефлексии

## 📞 Поддержка

Если проблемы не решаются:
1. Проверьте версии всех зависимостей
2. Запустите `python test_agent.py` для диагностики
3. Посмотрите логи в `agent_data/agent.log`
4. Создайте issue в репозитории с полным текстом ошибки 