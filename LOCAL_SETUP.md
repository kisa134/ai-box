# 🚀 Локальный Запуск AIbox Агента

## 📋 Быстрый Старт

### 1. **Проверить Ollama:**
```bash
ollama list
```

Должны быть доступны модели:
- phi3:latest
- qwen3:latest  
- deepseek-r1:latest
- mixtral:latest
- mistral:latest
- llama3:latest

### 2. **Запустить агента:**
```bash
python run_local_agent.py
```

### 3. **Для интерактивного тестирования:**
```bash
python test_agent_interactive.py
```

### 4. **Для веб-интерфейса:**
```bash
streamlit run streamlit_app.py
```

## 🎯 Способы Запуска

### **Фоновый режим (рекомендуется):**
```bash
python run_local_agent.py
```
- Агент работает в фоне
- Автоматический цикл сознания
- Graceful shutdown при Ctrl+C

### **Интерактивный режим:**
```bash
python test_agent_interactive.py
```
- Диалог с агентом
- Автоматические тесты
- Мониторинг статуса

### **Веб-интерфейс:**
```bash
streamlit run streamlit_app.py
```
- Веб-интерфейс на http://localhost:8501
- 6 вкладок мониторинга
- Интерактивный чат

## 🔧 Устранение Проблем

### **Ollama не отвечает:**
```bash
# Остановить Ollama
taskkill /f /im ollama.exe

# Запустить заново
ollama serve
```

### **Модели не отображаются:**
```bash
# Проверить директорию моделей
dir "C:\Users\HYPERPC\.ollama\models"

# Перезапустить Ollama
ollama serve
```

### **Ошибки Python:**
```bash
# Переустановить зависимости
pip install -r requirements.txt --force-reinstall
```

## 📊 Мониторинг

### **Статус агента:**
- Логи в консоли
- Статус каждые 30 секунд
- Циклы сознания

### **Ресурсы:**
- VRAM: 4-24 GB (зависит от модели)
- RAM: 2-8 GB
- Время ответа: 2-10 секунд

## 🎉 Готово!

Ваш AIbox агент готов к работе на локальной машине!

**Ключевые возможности:**
- ✅ Multi-model reasoning через Ollama
- ✅ Глубокая рефлексия и самосознание
- ✅ Динамическое обучение
- ✅ Graceful degradation
- ✅ Кэширование для производительности
- ✅ Полная интеграция подсознания

**Удачного тестирования!** 🚀 