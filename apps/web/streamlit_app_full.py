import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json
import asyncio
import threading
import psutil
import GPUtil

# Импорт наших модулей
from autonomous_agent import AutonomousAgent
from core.goal_module import GoalPriority

# Конфигурация страницы
st.set_page_config(
    page_title="🤖 AIbox - Автономный Агент с Самосознанием",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Кастомные стили
st.markdown("""
<style>
.user-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 15px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.agent-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 15px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.thinking-process {
    background-color: #f0f8ff;
    border-left: 4px solid #4a90e2;
    padding: 10px;
    margin: 5px 0;
    border-radius: 5px;
    font-style: italic;
}

.metric-card {
    background: linear-gradient(45deg, #f3f4f6, #ffffff);
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.status-active { color: #10b981; font-weight: bold; }
.status-inactive { color: #ef4444; font-weight: bold; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Инициализация состояния
if 'agent' not in st.session_state:
    st.session_state.agent = None
    st.session_state.conversation_history = []
    st.session_state.agent_running = False
    st.session_state.auto_update = False
    st.session_state.background_task = None

def get_system_resources():
    """Получить информацию о системных ресурсах"""
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # RAM
        memory = psutil.virtual_memory()
        ram_used = memory.used / (1024**3)  # GB
        ram_total = memory.total / (1024**3)  # GB
        ram_percent = memory.percent
        
        # GPU
        gpus = GPUtil.getGPUs()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                'name': gpu.name,
                'memory_used': gpu.memoryUsed,
                'memory_total': gpu.memoryTotal,
                'memory_percent': (gpu.memoryUsed / gpu.memoryTotal) * 100,
                'temperature': gpu.temperature,
                'load': gpu.load * 100
            })
        
        return {
            'cpu_percent': cpu_percent,
            'ram_used': ram_used,
            'ram_total': ram_total,
            'ram_percent': ram_percent,
            'gpus': gpu_info
        }
    except Exception as e:
        st.error(f"Ошибка получения ресурсов: {e}")
        return None

def start_agent():
    """Запустить агента"""
    try:
        if st.session_state.agent is None:
            with st.spinner("🤖 Инициализация AIbox агента..."):
                st.session_state.agent = AutonomousAgent("AIbox Agent", "agent_data")
                st.session_state.agent.initialize_modules()
                st.session_state.agent.initialize_agent()
                st.session_state.agent_running = True
                st.success("✅ Агент успешно запущен!")
        else:
            st.warning("⚠️ Агент уже запущен")
    except Exception as e:
        st.error(f"❌ Ошибка запуска агента: {e}")

def stop_agent():
    """Остановить агента"""
    try:
        if st.session_state.agent:
            st.session_state.agent.stop()
            st.session_state.agent = None
            st.session_state.agent_running = False
            st.success("🛑 Агент остановлен")
        else:
            st.warning("⚠️ Агент не запущен")
    except Exception as e:
        st.error(f"❌ Ошибка остановки агента: {e}")

def get_agent_status():
    """Получить статус агента"""
    if st.session_state.agent:
        try:
            return st.session_state.agent.get_status_report()
        except Exception as e:
            st.error(f"Ошибка получения статуса: {e}")
            return {}
    return {}

def show_overview(agent_status):
    """Показать обзор системы"""
    st.header("📊 Обзор Системы")
    
    # Системные ресурсы
    resources = get_system_resources()
    if resources:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("CPU", f"{resources['cpu_percent']:.1f}%")
        
        with col2:
            st.metric("RAM", f"{resources['ram_used']:.1f}GB / {resources['ram_total']:.1f}GB", f"{resources['ram_percent']:.1f}%")
        
        with col3:
            if resources['gpus']:
                gpu = resources['gpus'][0]  # Первая GPU
                st.metric("GPU VRAM", f"{gpu['memory_used']}MB / {gpu['memory_total']}MB", f"{gpu['memory_percent']:.1f}%")
            else:
                st.metric("GPU", "Не обнаружена")
    
    # Статус агента
    if agent_status:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cycles = agent_status.get('consciousness_cycles', 0)
            st.metric("🧠 Циклы Сознания", cycles)
        
        with col2:
            goals = agent_status.get('goals_count', 0)
            st.metric("🎯 Активные Цели", goals)
        
        with col3:
            memories = agent_status.get('memory_stats', {}).get('total_episodes', 0)
            st.metric("💾 Эпизоды в Памяти", memories)
        
        with col4:
            thoughts = agent_status.get('active_thoughts', 0)
            st.metric("🌳 Активные Мысли", thoughts)
    
    # Модули
    st.subheader("🔧 Статус Модулей")
    if agent_status and 'modules_status' in agent_status:
        modules = agent_status['modules_status']
        cols = st.columns(4)
        
        module_names = list(modules.keys())
        for i, (col, module_name) in enumerate(zip(cols, module_names)):
            with col:
                status = modules[module_name]
                if status:
                    st.success(f"✅ {module_name}")
                else:
                    st.error(f"❌ {module_name}")

def show_chat():
    """Показать чат с агентом"""
    st.header("💬 Чат с Агентом")
    
    # Поле ввода
    user_input = st.text_area("Введите сообщение:", height=100, key="user_input")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📤 Отправить", type="primary"):
            if user_input and st.session_state.agent:
                with st.spinner("🤖 Агент думает..."):
                    try:
                        # Асинхронный вызов
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        response = loop.run_until_complete(
                            st.session_state.agent.process_input(user_input)
                        )
                        loop.close()
                        
                        # Добавить в историю
                        st.session_state.conversation_history.append({
                            'user': user_input,
                            'agent': response,
                            'timestamp': datetime.now()
                        })
                        
                        st.success("✅ Ответ получен!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Ошибка: {e}")
            else:
                st.warning("⚠️ Введите сообщение и убедитесь, что агент запущен")
    
    with col2:
        if st.button("🔄 Очистить чат"):
            st.session_state.conversation_history = []
            st.rerun()
    
    # История чата
    st.subheader("📜 История чата")
    for i, msg in enumerate(st.session_state.conversation_history):
        with st.container():
            st.markdown(f"**👤 Вы ({msg['timestamp'].strftime('%H:%M:%S')}):**")
            st.markdown(f'<div class="user-message">{msg["user"]}</div>', unsafe_allow_html=True)
            
            st.markdown(f"**🤖 Агент ({msg['timestamp'].strftime('%H:%M:%S')}):**")
            st.markdown(f'<div class="agent-message">{msg["agent"]}</div>', unsafe_allow_html=True)
            st.divider()

def show_ollama_status():
    """Показать статус Ollama"""
    st.header("🔧 Статус Ollama")
    
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            st.success("✅ Ollama работает")
            
            # Парсинг списка моделей
            lines = result.stdout.strip().split('\n')[1:]  # Пропустить заголовок
            models = []
            
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        models.append({
                            'name': parts[0],
                            'id': parts[1],
                            'size': parts[2],
                            'modified': ' '.join(parts[3:]) if len(parts) > 3 else ''
                        })
            
            # Таблица моделей
            if models:
                df = pd.DataFrame(models)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("⚠️ Модели не найдены")
        else:
            st.error("❌ Ollama не отвечает")
            
    except Exception as e:
        st.error(f"❌ Ошибка проверки Ollama: {e}")

def show_memory_status(agent_status):
    """Показать статус памяти"""
    st.header("💾 Статус Памяти")
    
    if st.session_state.agent and hasattr(st.session_state.agent, 'memory'):
        memory = st.session_state.agent.memory
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Статистика")
            try:
                episodes = memory.get_recent_episodes(1000)  # Получить все эпизоды
                st.metric("Всего эпизодов", len(episodes))
                
                if episodes:
                    # Типы эпизодов
                    types = {}
                    for episode in episodes:
                        ep_type = episode.get('type', 'unknown')
                        types[ep_type] = types.get(ep_type, 0) + 1
                    
                    # График типов
                    if types:
                        fig = px.pie(values=list(types.values()), names=list(types.keys()), 
                                   title="Распределение типов эпизодов")
                        st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Ошибка получения статистики: {e}")
        
        with col2:
            st.subheader("🔍 Поиск в памяти")
            search_query = st.text_input("Введите запрос для поиска:")
            
            if search_query and st.button("🔍 Найти"):
                try:
                    results = memory.retrieve_similar(search_query, 5)
                    if results:
                        st.success(f"Найдено {len(results)} результатов:")
                        for i, result in enumerate(results):
                            with st.expander(f"Результат {i+1}"):
                                st.write(f"**Содержание:** {result['content']}")
                                st.write(f"**Тип:** {result.get('type', 'unknown')}")
                                st.write(f"**Дата:** {result.get('created_at', 'unknown')}")
                    else:
                        st.warning("Ничего не найдено")
                except Exception as e:
                    st.error(f"Ошибка поиска: {e}")

def show_consciousness_analysis(agent_status):
    """Показать анализ сознания"""
    st.header("🧠 Анализ Сознания")
    
    if st.session_state.agent:
        try:
            # Получить диагностику сознания
            diagnostic = st.session_state.agent.get_consciousness_diagnostic()
            
            if diagnostic:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Метрики Сознания")
                    
                    # Радарная диаграмма
                    metrics = ['self_recognition', 'metacognitive_awareness', 'temporal_continuity', 'agency_sense']
                    values = [diagnostic.get(metric, 0) for metric in metrics]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=metrics,
                        fill='toself',
                        name='Сознание'
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                        showlegend=False,
                        title="Радар Сознания"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("📈 Детальные метрики")
                    for metric, value in diagnostic.items():
                        if isinstance(value, (int, float)):
                            st.metric(metric.replace('_', ' ').title(), f"{value:.2f}")
            
        except Exception as e:
            st.error(f"Ошибка анализа сознания: {e}")

def show_goals_motivation(agent_status):
    """Показать цели и мотивацию"""
    st.header("🎯 Цели и Мотивация")
    
    if st.session_state.agent and hasattr(st.session_state.agent, 'goals'):
        goals = st.session_state.agent.goals
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Активные Цели")
            try:
                active_goals = goals.get_active_goals()
                
                for goal in active_goals:
                    with st.expander(f"🎯 {goal.description}"):
                        st.write(f"**Приоритет:** {goal.priority.value}")
                        st.write(f"**Прогресс:** {goal.progress:.1f}%")
                        st.write(f"**Статус:** {'Активна' if goal.active else 'Неактивна'}")
                        
                        # Прогресс бар
                        st.progress(goal.progress / 100)
                        
            except Exception as e:
                st.error(f"Ошибка получения целей: {e}")
        
        with col2:
            st.subheader("📊 Статистика Целей")
            try:
                total_goals = len(goals.goals)
                active_count = len([g for g in goals.goals.values() if g.active])
                completed_count = len([g for g in goals.goals.values() if g.progress >= 100])
                
                st.metric("Всего целей", total_goals)
                st.metric("Активных", active_count)
                st.metric("Завершенных", completed_count)
                
                # График прогресса
                if active_goals:
                    goal_names = [g.description[:20] + "..." if len(g.description) > 20 else g.description for g in active_goals]
                    progress_values = [g.progress for g in active_goals]
                    
                    fig = px.bar(x=goal_names, y=progress_values, 
                               title="Прогресс по целям",
                               labels={'x': 'Цели', 'y': 'Прогресс (%)'})
                    st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Ошибка статистики целей: {e}")

def show_world_model(agent_status):
    """Показать модель мира"""
    st.header("🌍 Модель Мира")
    
    if st.session_state.agent and hasattr(st.session_state.agent, 'world_model'):
        world_model = st.session_state.agent.world_model
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Концепции")
            try:
                if hasattr(world_model, 'concepts') and world_model.concepts:
                    concepts_df = pd.DataFrame([
                        {
                            'Концепция': concept,
                            'Уверенность': details.get('confidence', 0),
                            'Частота': details.get('frequency', 0)
                        }
                        for concept, details in world_model.concepts.items()
                    ])
                    
                    if not concepts_df.empty:
                        st.dataframe(concepts_df, use_container_width=True)
                    else:
                        st.info("Концепции не найдены")
                else:
                    st.info("Концепции не загружены")
                    
            except Exception as e:
                st.error(f"Ошибка получения концепций: {e}")
        
        with col2:
            st.subheader("🔗 Отношения")
            try:
                if hasattr(world_model, 'relationships') and world_model.relationships:
                    relationships_df = pd.DataFrame([
                        {
                            'От': rel.get('from', ''),
                            'К': rel.get('to', ''),
                            'Тип': rel.get('type', ''),
                            'Сила': rel.get('strength', 0)
                        }
                        for rel in world_model.relationships
                    ])
                    
                    if not relationships_df.empty:
                        st.dataframe(relationships_df, use_container_width=True)
                    else:
                        st.info("Отношения не найдены")
                else:
                    st.info("Отношения не загружены")
                    
            except Exception as e:
                st.error(f"Ошибка получения отношений: {e}")

def show_thought_tree(agent_status):
    """Показать дерево мыслей"""
    st.header("🌳 Дерево Мыслей")
    
    if st.session_state.agent and hasattr(st.session_state.agent, 'thought_tree'):
        thought_tree = st.session_state.agent.thought_tree
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌱 Активные Мысли")
            try:
                active_thoughts = [t for t in thought_tree.thoughts.values() if hasattr(t, 'status') and t.status.value == "active"]
                
                for thought in active_thoughts[:5]:  # Показать первые 5
                    with st.expander(f"💭 {thought.content[:50]}..."):
                        st.write(f"**Содержание:** {thought.content}")
                        st.write(f"**Тип:** {thought.thought_type.value}")
                        st.write(f"**Уверенность:** {thought.confidence:.2f}")
                        st.write(f"**Статус:** {thought.status.value}")
                        
            except Exception as e:
                st.error(f"Ошибка получения мыслей: {e}")
        
        with col2:
            st.subheader("📊 Статистика Мыслей")
            try:
                total_thoughts = len(thought_tree.thoughts)
                active_count = len([t for t in thought_tree.thoughts.values() if hasattr(t, 'status') and t.status.value == "active"])
                completed_count = len([t for t in thought_tree.thoughts.values() if hasattr(t, 'status') and t.status.value == "completed"])
                
                st.metric("Всего мыслей", total_thoughts)
                st.metric("Активных", active_count)
                st.metric("Завершенных", completed_count)
                
                # График типов мыслей
                if thought_tree.thoughts:
                    thought_types = {}
                    for thought in thought_tree.thoughts.values():
                        thought_type = thought.thought_type.value
                        thought_types[thought_type] = thought_types.get(thought_type, 0) + 1
                    
                    if thought_types:
                        fig = px.pie(values=list(thought_types.values()), names=list(thought_types.keys()), 
                                   title="Распределение типов мыслей")
                        st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Ошибка статистики мыслей: {e}")

def show_self_log(agent_status):
    """Показать самоанализ"""
    st.header("🧠 Самоанализ")
    
    if st.session_state.agent and hasattr(st.session_state.agent, 'self_model'):
        self_model = st.session_state.agent.self_model
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Рефлексия")
            try:
                if hasattr(self_model, 'reflection_history') and self_model.reflection_history:
                    for reflection in self_model.reflection_history[-5:]:  # Последние 5
                        with st.expander(f"📅 {reflection.get('timestamp', 'Неизвестно')}"):
                            st.write(f"**Тема:** {reflection.get('topic', 'Неизвестно')}")
                            st.write(f"**Содержание:** {reflection.get('content', 'Нет данных')}")
                            st.write(f"**Уверенность:** {reflection.get('confidence', 0):.2f}")
                else:
                    st.info("История рефлексии пуста")
                    
            except Exception as e:
                st.error(f"Ошибка получения рефлексии: {e}")
        
        with col2:
            st.subheader("📊 Метапознание")
            try:
                if hasattr(self_model, 'metacognitive_insights') and self_model.metacognitive_insights:
                    for insight in self_model.metacognitive_insights[-5:]:  # Последние 5
                        with st.expander(f"💡 {insight.get('type', 'Инсайт')}"):
                            st.write(f"**Описание:** {insight.get('description', 'Нет данных')}")
                            st.write(f"**Важность:** {insight.get('importance', 0):.2f}")
                            st.write(f"**Дата:** {insight.get('timestamp', 'Неизвестно')}")
                else:
                    st.info("Метапознавательные инсайты не найдены")
                    
            except Exception as e:
                st.error(f"Ошибка получения метапознания: {e}")

# Основной интерфейс
def main():
    st.title("🤖 AIbox - Автономный Агент с Самосознанием")
    st.markdown("---")
    
    # Боковая панель
    with st.sidebar:
        st.header("🎛️ Управление")
        
        # Кнопки управления
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Запустить", type="primary"):
                start_agent()
        
        with col2:
            if st.button("🛑 Остановить"):
                stop_agent()
        
        # Статус
        st.subheader("📊 Статус")
        if st.session_state.agent_running:
            st.success("✅ Агент работает")
        else:
            st.error("❌ Агент остановлен")
        
        # Автообновление
        st.subheader("🔄 Автообновление")
        auto_update = st.checkbox("Автоматическое обновление", value=st.session_state.auto_update)
        if auto_update != st.session_state.auto_update:
            st.session_state.auto_update = auto_update
            st.rerun()
        
        # Информация о системе
        st.subheader("💻 Система")
        resources = get_system_resources()
        if resources:
            st.write(f"CPU: {resources['cpu_percent']:.1f}%")
            st.write(f"RAM: {resources['ram_percent']:.1f}%")
            if resources['gpus']:
                gpu = resources['gpus'][0]
                st.write(f"GPU: {gpu['memory_percent']:.1f}%")
    
    # Основные вкладки
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Обзор", "💬 Чат", "🔧 Ollama", "💾 Память", "🧠 Сознание", "🎯 Цели", "🌍 Мир", "🌳 Мысли"
    ])
    
    # Получить статус агента
    agent_status = get_agent_status()
    
    with tab1:
        show_overview(agent_status)
    
    with tab2:
        show_chat()
    
    with tab3:
        show_ollama_status()
    
    with tab4:
        show_memory_status(agent_status)
    
    with tab5:
        show_consciousness_analysis(agent_status)
    
    with tab6:
        show_goals_motivation(agent_status)
    
    with tab7:
        show_world_model(agent_status)
    
    with tab8:
        show_thought_tree(agent_status)
    
    # Автообновление
    if st.session_state.auto_update:
        time.sleep(2)
        st.rerun()

if __name__ == "__main__":
    main() 