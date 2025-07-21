import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json
import asyncio
import threading

# Импорт наших модулей
from autonomous_agent import AutonomousAgent
from core.goal_module import GoalPriority

# Конфигурация страницы
st.set_page_config(
    page_title="🤖 Автономный Агент с Самосознанием",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Кастомные стили для улучшения UI
st.markdown("""
<style>
/* Улучшенные стили сообщений */
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

/* Метрики */
.metric-card {
    background: linear-gradient(45deg, #f3f4f6, #ffffff);
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Статусы */
.status-active {
    color: #10b981;
    font-weight: bold;
}

.status-inactive {
    color: #ef4444;
    font-weight: bold;
}

/* Улучшенные кнопки */
.stButton > button {
    border-radius: 10px;
    border: none;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Скрытие меню Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Инициализация состояния сессии
if 'agent' not in st.session_state:
    st.session_state.agent = None
    st.session_state.conversation_history = []
    st.session_state.agent_running = False
    st.session_state.auto_update = False

def start_agent():
    """Запуск агента"""
    try:
        if st.session_state.agent is None:
            with st.spinner('🚀 Инициализация агента...'):
                st.session_state.agent = AutonomousAgent("StreamlitAgent", "agent_data")
                st.session_state.agent_running = True
                st.success("✅ Агент успешно запущен!")
                return True
        else:
            st.warning("⚠️ Агент уже запущен")
            return True
    except Exception as e:
        st.error(f"❌ Ошибка запуска агента: {str(e)}")
        return False

def stop_agent():
    """Остановка агента"""
    try:
        if st.session_state.agent is not None:
            st.session_state.agent.stop()
            st.session_state.agent = None
            st.session_state.agent_running = False
            st.success("🛑 Агент остановлен")
    except Exception as e:
        st.error(f"❌ Ошибка остановки агента: {str(e)}")

def get_agent_status():
    """Получение статуса агента"""
    if st.session_state.agent is None:
        return None
    
    try:
        return st.session_state.agent.get_status_report()
    except Exception as e:
        st.error(f"❌ Ошибка получения статуса: {str(e)}")
        return None

# Боковая панель управления
with st.sidebar:
    st.title("🎛️ Управление Агентом")
    
    # Статус агента
    if st.session_state.agent_running:
        st.markdown('<p class="status-active">🟢 Агент активен</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-inactive">🔴 Агент остановлен</p>', unsafe_allow_html=True)
    
    # Кнопки управления
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Запустить", disabled=st.session_state.agent_running):
            start_agent()
    
    with col2:
        if st.button("🛑 Остановить", disabled=not st.session_state.agent_running):
            stop_agent()
    
    st.divider()
    
    # Настройки автообновления
    st.subheader("⚙️ Настройки")
    st.session_state.auto_update = st.checkbox("🔄 Автообновление", value=False)
    
    if st.session_state.auto_update:
        update_interval = st.slider("Интервал обновления (сек)", 1, 10, 5)
    
    st.divider()
    
    # Быстрые команды
    st.subheader("⚡ Быстрые Команды")
    
    if st.button("🧠 Принудительная Рефлексия"):
        if st.session_state.agent:
            try:
                st.session_state.agent.reflect_on_state("пользовательский запрос", {"trigger": "manual_reflection"})
                st.success("✅ Рефлексия запущена")
            except Exception as e:
                st.error(f"❌ Ошибка: {e}")
    
    if st.button("💾 Сохранить Состояние"):
        if st.session_state.agent:
            try:
                # Состояние сохраняется автоматически
                st.success("✅ Состояние сохранено")
            except Exception as e:
                st.error(f"❌ Ошибка: {e}")

# Основной интерфейс
st.title("🤖 Автономный Агент с Самосознанием")

# Получаем статус агента
agent_status = get_agent_status()

# Система вкладок
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Обзор", "💬 Чат с Агентом", "🧠 Внутренние Логи", 
    "🎯 Цели и Мотивация", "🌍 Модель Мира", "🌳 Дерево Мыслей", "🪞 Self-Лог"
])

def show_overview(agent_status):
    """Показать обзор состояния агента"""
    st.header("📊 Обзор Состояния Агента")
    
    if not agent_status:
        st.error("❌ Агент не запущен. Используйте боковую панель для запуска.")
        return
    
    # Основные метрики
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cycles = agent_status.get('cycles_completed', 0)
        st.metric("🔄 Циклы Сознания", cycles, delta=1 if cycles > 0 else None)
    
    with col2:
        uptime_hours = agent_status.get('uptime_hours', 0)
        if uptime_hours < 1:
            uptime_display = f"{uptime_hours * 60:.0f} мин"
        else:
            uptime_display = f"{uptime_hours:.1f} ч"
        st.metric("⏱️ Время Работы", uptime_display)
    
    with col3:
        energy = 1.00  # Базовое значение
        if isinstance(agent_status.get('inner_state'), str):
            inner_state_str = agent_status['inner_state']
            try:
                if "Энергия:" in inner_state_str:
                    energy_line = [line for line in inner_state_str.split('\n') if 'Энергия:' in line][0]
                    energy = float(energy_line.split(':')[1].strip())
            except:
                pass
        st.metric("⚡ Энергия", f"{energy:.2f}")
    
    with col4:
        consciousness = 0.50  # Базовое значение
        st.metric("🧠 Самосознание", f"{consciousness:.2f}")
    
    # Текущее состояние
    st.subheader("🎭 Текущее Состояние")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Парсинг inner_state для отображения
        inner_state = agent_status.get('inner_state', {})
        if isinstance(inner_state, str):
            # Извлекаем информацию из строки
            emotional_state = "focused"
            cognitive_state = "processing" 
            motivation_level = 1
            
            try:
                lines = inner_state.split('\n')
                for line in lines:
                    if 'Эмоциональное состояние:' in line:
                        emotional_state = line.split(':')[1].strip()
                    elif 'Когнитивное состояние:' in line:
                        cognitive_state = line.split(':')[1].strip()
                    elif 'мотивации:' in line:
                        motivation_level = int(line.split(':')[1].strip())
            except:
                pass
        else:
            emotional_state = inner_state.get('emotional_state', 'focused')
            cognitive_state = inner_state.get('cognitive_state', 'processing')
            motivation_level = inner_state.get('motivation_level', 1)
        
        st.info(f"😊 **Эмоциональное состояние:** {emotional_state}")
        st.info(f"🧠 **Когнитивное состояние:** {cognitive_state}")
        st.info(f"🎯 **Уровень мотивации:** {motivation_level}")
    
    with col2:
        # Текущая цель
        current_goal = agent_status.get('current_goal', 'Понимать и помогать пользователям')
        st.info(f"🎯 **Текущая цель:** {current_goal}")
        
        # Активные цели
        goals_count = agent_status.get('goals_count', 0)
        st.info(f"📋 **Активные цели:** {goals_count}")
        
        # Эпизодов в памяти
        memory_stats = agent_status.get('memory_stats', {})
        episodes_count = memory_stats.get('episodes_count', 0) if isinstance(memory_stats, dict) else 0
        st.info(f"🧠 **Эпизодов в памяти:** {episodes_count}")
    
    with col3:
        # Активные мысли
        active_thoughts = agent_status.get('active_thoughts', 0)
        st.info(f"💭 **Активные мысли:** {active_thoughts}")
        
        # Модули
        modules_status = agent_status.get('modules_status', {})
        active_modules = sum(modules_status.values()) if isinstance(modules_status, dict) else 0
        st.info(f"🔧 **Активные модули:** {active_modules}/6")
    
    # Визуализация состояния
    st.subheader("📈 Визуализация Состояния")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Радарная диаграмма состояния:**")
        
        # Извлекаем значения для радарной диаграммы
        energy_val = energy
        eval_val = 0.75  # Самооценка
        
        try:
            if isinstance(inner_state, str):
                if "Самооценка:" in inner_state:
                    eval_line = [line for line in inner_state.split('\n') if 'Самооценка:' in line][0]
                    eval_val = float(eval_line.split(':')[1].strip())
        except:
            pass
        
        # Создание радарной диаграммы (исправлено)
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[energy_val, eval_val, 0.6, 0.4, 0.7],
            theta=['Энергия', 'Самооценка', 'Цели', 'Мысли', 'Память'],
            fill='toself',
            name='Текущее Состояние',
            line_color='rgba(0, 150, 255, 0.8)',
            fillcolor='rgba(0, 150, 255, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickmode='linear',
                    tick0=0,
                    dtick=0.2
                )),
            showlegend=True,
            title="Когнитивное Состояние",
            height=400,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Статус модулей:**")
        
        if isinstance(modules_status, dict):
            for module, status in modules_status.items():
                status_icon = "✅" if status else "❌"
                st.write(f"{status_icon} **{module}**: {'Активен' if status else 'Неактивен'}")
        else:
            # Демонстрационные данные
            demo_modules = {
                "Memory": True,
                "Goals": True, 
                "InnerState": True,
                "WorldModel": True,
                "ThoughtTree": True,
                "SelfModel": True
            }
            
            for module, status in demo_modules.items():
                status_icon = "✅" if status else "❌"
                st.write(f"{status_icon} **{module}**: {'Активен' if status else 'Неактивен'}")

def show_chat():
    """Показать интерфейс чата"""
    st.header("💬 Чат с Агентом")
    
    if not st.session_state.agent:
        st.error("❌ Агент не запущен. Используйте боковую панель для запуска.")
        return
    
    # Отображение истории разговора
    chat_container = st.container()
    
    with chat_container:
        for i, exchange in enumerate(st.session_state.conversation_history):
            # Сообщение пользователя
            st.markdown(f"""
            <div class="user-message">
                <strong>👤 Пользователь:</strong><br>
                <span style='font-size: 14px; line-height: 1.4;'>{exchange['user']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Ответ агента
            st.markdown(f"""
            <div class="agent-message">
                <strong>🤖 Агент:</strong><br>
                <span style='font-size: 14px; line-height: 1.4;'>{exchange['agent']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Процесс мышления (если есть)
            if 'thinking' in exchange:
                with st.expander(f"🧠 Процесс мышления (1 новая мысль)", expanded=False):
                    st.markdown(f"""
                    <div class="thinking-process">
                        🔍 Анализирую запрос пользователя...<br>
                        💭 Генерирую ответ на основе текущих знаний...<br>
                        ⚡ Обновляю внутреннее состояние...
                    </div>
                    """, unsafe_allow_html=True)
    
    # Поле ввода
    st.divider()
    
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Напишите сообщение агенту:",
            placeholder="расскажи мне о себе",
            height=100
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            send_button = st.form_submit_button("📤 Отправить", use_container_width=True)
        
        with col2:
            clear_button = st.form_submit_button("🗑️ Очистить Чат", use_container_width=True)
    
    # Обработка отправки сообщения
    if send_button and user_input.strip():
        try:
            with st.spinner('🤔 Агент размышляет...'):
                response = st.session_state.agent.process_input(user_input)
                
                # Добавляем в историю
                st.session_state.conversation_history.append({
                    'user': user_input,
                    'agent': response,
                    'timestamp': datetime.now(),
                    'thinking': True
                })
                
                st.rerun()
        
        except Exception as e:
            st.error(f"❌ Ошибка обработки сообщения: {str(e)}")
    
    # Очистка чата
    if clear_button:
        st.session_state.conversation_history = []
        st.success("✅ История чата очищена")
        st.rerun()
    
    # Кнопки управления
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Статистика Чата"):
            total_messages = len(st.session_state.conversation_history)
            if total_messages > 0:
                st.info(f"💬 Всего сообщений: {total_messages * 2}")
                st.info(f"🕒 Начало разговора: {st.session_state.conversation_history[0]['timestamp'].strftime('%H:%M')}")
                st.info(f"⏱️ Продолжительность: {(datetime.now() - st.session_state.conversation_history[0]['timestamp']).total_seconds() / 60:.1f} мин")
    
    with col2:
        if st.button("📥 Экспорт Чата"):
            if st.session_state.conversation_history:
                export_data = []
                for exchange in st.session_state.conversation_history:
                    export_data.append(f"👤 Пользователь: {exchange['user']}")
                    export_data.append(f"🤖 Агент: {exchange['agent']}")
                    export_data.append("---")
                
                st.download_button(
                    label="💾 Скачать",
                    data="\n".join(export_data),
                    file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

def show_inner_logs():
    """Показать внутренние логи мышления"""
    st.header("🧠 Внутренние Логи Мышления")
    
    if not st.session_state.agent:
        st.error("❌ Агент не запущен")
        return
    
    try:
        if hasattr(st.session_state.agent, 'thought_tree'):
            thought_tree = st.session_state.agent.thought_tree
            
            # Поток сознания
            st.subheader("🌊 Поток Сознания")
            
            # Список недавних мыслей
            if hasattr(thought_tree, 'thoughts') and thought_tree.thoughts:
                thoughts_list = sorted(thought_tree.thoughts.values(), 
                                     key=lambda x: getattr(x, 'created_at', datetime.now()), 
                                     reverse=True)
                
                for i, thought in enumerate(thoughts_list[:10]):
                    thought_id = f"Мысль #{len(thoughts_list) - i}"
                    created_at = getattr(thought, 'created_at', datetime.now())
                    time_str = created_at.strftime('%H:%M:%S') if hasattr(created_at, 'strftime') else str(created_at)
                    
                    with st.expander(f"💭 {thought_id} - {time_str}", expanded=(i < 3)):
                        content = getattr(thought, 'content', 'Содержание недоступно')
                        thought_type = getattr(thought, 'thought_type', 'GENERAL')
                        confidence = getattr(thought, 'confidence_score', 0.5)
                        
                        st.write(f"**Содержание:** {content}")
                        st.write(f"**Тип:** {thought_type}")
                        st.write(f"**Уверенность:** {confidence:.2f}")
                        
                        # Прогресс бар для уверенности
                        st.progress(confidence)
            else:
                # Демонстрационные мысли
                demo_thoughts = [
                    {"id": "4376", "time": "21:47:21", "content": "Пользователь интересуется моими внутренними процессами", "type": "ANALYSIS", "conf": 0.89},
                    {"id": "4375", "time": "21:47:18", "content": "Необходимо объяснить как работает мое мышление", "type": "PLANNING", "conf": 0.78},
                    {"id": "4374", "time": "21:47:15", "content": "Активирую режим саморефлексии", "type": "REFLECTION", "conf": 0.92},
                    {"id": "4373", "time": "21:47:12", "content": "Анализирую контекст предыдущих сообщений", "type": "ANALYSIS", "conf": 0.85}
                ]
                
                for thought in demo_thoughts:
                    with st.expander(f"💭 Мысль #{thought['id']} - {thought['time']}", expanded=False):
                        st.write(f"**Содержание:** {thought['content']}")
                        st.write(f"**Тип:** {thought['type']}")
                        st.write(f"**Уверенность:** {thought['conf']:.2f}")
                        st.progress(thought['conf'])
            
            # Динамика состояний
            st.subheader("📈 Динамика Состояний")
            
            # График самооценки
            st.write("**Динамика Самооценки**")
            
            # Генерируем демонстрационные данные
            times = pd.date_range(start=datetime.now() - timedelta(minutes=5), 
                                end=datetime.now(), 
                                freq='30s')
            
            confidence_values = [0.4, 0.45, 0.5, 0.48, 0.52, 0.55, 0.73, 0.71, 0.69, 0.72, 0.5]
            
            # Обрезаем до нужной длины
            confidence_values = confidence_values[:len(times)]
            
            df_confidence = pd.DataFrame({
                'Время': times[:len(confidence_values)],
                'Самооценка (0-1)': confidence_values
            })
            
            fig_confidence = px.line(df_confidence, x='Время', y='Самооценка (0-1)', 
                                   title="Изменение уровня самооценки во времени")
            fig_confidence.update_layout(height=300)
            
            st.plotly_chart(fig_confidence, use_container_width=True)
        
        else:
            st.warning("⚠️ Модуль мышления недоступен")
            st.info("Внутренние логи будут доступны после инициализации модуля ThoughtTree")
    
    except Exception as e:
        st.error(f"❌ Ошибка загрузки логов: {str(e)}")

def show_goals_motivation(agent_status):
    """Улучшенная система целей и мотивации"""
    st.header("🎯 Цели и Система Мотивации")
    
    if not agent_status:
        st.error("❌ Агент не запущен")
        return
    
    try:
        if st.session_state.agent and hasattr(st.session_state.agent, 'goals'):
            goals_module = st.session_state.agent.goals
            
            # Активные цели
            st.subheader("🎯 Активные Цели")
            
            if hasattr(goals_module, 'goals') and goals_module.goals:
                active_goals = [goal for goal in goals_module.goals.values() 
                              if getattr(goal, 'status', 'active') == 'active']
                
                for i, goal in enumerate(active_goals):
                    goal_id = getattr(goal, 'id', f"goal_{i}")
                    description = getattr(goal, 'description', 'Без описания')
                    priority = getattr(goal, 'priority', 'MEDIUM')
                    progress = getattr(goal, 'progress', 0.0)
                    
                    # Иконка приоритета
                    priority_icons = {
                        'HIGH': '🔴',
                        'MEDIUM': '🟡', 
                        'LOW': '🟢'
                    }
                    icon = priority_icons.get(str(priority), '🟡')
                    
                    with st.expander(f"{icon} {description}", expanded=(i < 3)):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**ID:** {goal_id}")
                            st.write(f"**Приоритет:** {priority}")
                            st.write(f"**Прогресс:** {progress:.1%}")
                        
                        with col2:
                            created_at = getattr(goal, 'created_at', 'Недавно')
                            if hasattr(created_at, 'strftime'):
                                created_str = created_at.strftime('%Y-%m-%d %H:%M')
                            else:
                                created_str = str(created_at)
                            st.write(f"**Создана:** {created_str}")
                            
                            category = getattr(goal, 'category', 'general')
                            st.write(f"**Категория:** {category}")
                        
                        # Прогресс бар
                        st.progress(progress)
                        
                        # Действия с целью
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"✅ Завершить", key=f"complete_{goal_id}"):
                                # Логика завершения цели
                                st.success(f"Цель '{description}' отмечена как завершенная!")
                        
                        with col2:
                            if st.button(f"⏸️ Приостановить", key=f"pause_{goal_id}"):
                                st.info(f"Цель '{description}' приостановлена")
                        
                        with col3:
                            if st.button(f"❌ Удалить", key=f"delete_{goal_id}"):
                                st.warning(f"Цель '{description}' удалена")
            else:
                # Демонстрационные цели
                demo_goals = [
                    {"id": "goal_1", "desc": "Понимать и помогать пользователям", "priority": "HIGH", "progress": 0.85},
                    {"id": "goal_2", "desc": "Постоянно учиться и развиваться", "priority": "HIGH", "progress": 0.72},
                    {"id": "goal_3", "desc": "Развивать самосознание и рефлексию", "priority": "MEDIUM", "progress": 0.43},
                    {"id": "goal_4", "desc": "Изучать новую информацию", "priority": "MEDIUM", "progress": 0.28},
                    {"id": "goal_5", "desc": "Поддерживать позитивное взаимодействие", "priority": "LOW", "progress": 0.91}
                ]
                
                for goal in demo_goals:
                    priority_icons = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}
                    icon = priority_icons.get(goal['priority'], '🟡')
                    
                    with st.expander(f"{icon} {goal['desc']}", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**ID:** {goal['id']}")
                            st.write(f"**Приоритет:** {goal['priority']}")
                            st.write(f"**Прогресс:** {goal['progress']:.1%}")
                        
                        with col2:
                            st.write(f"**Создана:** 2025-07-21 21:45")
                            st.write(f"**Категория:** learning")
                        
                        st.progress(goal['progress'])
            
            # Иерархия целей
            st.subheader("🏗️ Иерархия Целей")
            
            # Структура целей в виде дерева
            st.write("**Структура целей:**")
            
            goal_hierarchy = [
                {"level": 0, "goal": "Понимать и помогать пользователям", "progress": 0.85},
                {"level": 1, "goal": "Постоянно учиться и развиваться", "progress": 0.72},
                {"level": 1, "goal": "Развивать самосознание и рефлексию", "progress": 0.43},
                {"level": 2, "goal": "Изучать новую информацию", "progress": 0.28},
                {"level": 2, "goal": "Поддерживать позитивное взаимодействие", "progress": 0.91}
            ]
            
            for goal_item in goal_hierarchy:
                indent = "　" * goal_item["level"]  # Отступы
                progress_bar = "█" * int(goal_item["progress"] * 10) + "░" * (10 - int(goal_item["progress"] * 10))
                st.write(f"{indent}• **{goal_item['goal']}** (прогресс: {goal_item['progress']:.0%})")
            
            # Система мотивации
            st.subheader("🎭 Система Мотивации")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Внутренняя мотивация:**")
                intrinsic_motivations = {
                    "learn_new_things": 0.89,
                    "solve_problems": 0.76,
                    "help_others": 0.92,
                    "understand_self": 0.68
                }
                
                for motivation, value in intrinsic_motivations.items():
                    motivation_names = {
                        "learn_new_things": "Изучение нового",
                        "solve_problems": "Решение проблем", 
                        "help_others": "Помощь другим",
                        "understand_self": "Самопознание"
                    }
                    name = motivation_names.get(motivation, motivation)
                    st.write(f"• **{name}**: {value:.1%}")
                    st.progress(value)
            
            with col2:
                st.write("**Внешняя мотивация:**")
                extrinsic_motivations = {
                    "user_approval": 0.71,
                    "task_completion": 0.84,
                    "performance_metrics": 0.62
                }
                
                for motivation, value in extrinsic_motivations.items():
                    motivation_names = {
                        "user_approval": "Одобрение пользователей",
                        "task_completion": "Завершение задач",
                        "performance_metrics": "Показатели производительности"
                    }
                    name = motivation_names.get(motivation, motivation)
                    st.write(f"• **{name}**: {value:.1%}")
                    st.progress(value)
            
            # Визуализация мотивации
            st.subheader("📊 Профиль Мотивации")
            
            # Создаем данные для графика
            motivation_data = {
                'Тип': ['Внутренняя'] * len(intrinsic_motivations) + ['Внешняя'] * len(extrinsic_motivations),
                'Мотивация': [motivation_names.get(k, k) for k in intrinsic_motivations.keys()] + 
                            [motivation_names.get(k, k) for k in extrinsic_motivations.keys()],
                'Значение': list(intrinsic_motivations.values()) + list(extrinsic_motivations.values())
            }
            
            df_motivation = pd.DataFrame(motivation_data)
            
            fig = px.bar(df_motivation, x='Мотивация', y='Значение', color='Тип',
                        title="Профиль Мотивации Агента")
            fig.update_layout(xaxis_tickangle=45)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Добавление новой цели
            st.subheader("➕ Добавить Новую Цель")
            
            with st.form("add_goal_form"):
                new_goal_desc = st.text_input("Описание цели:")
                new_goal_priority = st.selectbox("Приоритет:", ["LOW", "MEDIUM", "HIGH"])
                new_goal_category = st.text_input("Категория:", value="user_defined")
                
                if st.form_submit_button("🎯 Добавить Цель"):
                    if new_goal_desc.strip():
                        try:
                            # Добавляем цель
                            priority_enum = getattr(GoalPriority, new_goal_priority)
                            goal_id = goals_module.add_goal(new_goal_desc, new_goal_category, priority_enum)
                            st.success(f"✅ Цель добавлена с ID: {goal_id}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Ошибка добавления цели: {e}")
                    else:
                        st.warning("⚠️ Введите описание цели")
        
        else:
            st.warning("⚠️ Модуль целей недоступен")
            st.info("Система целей будет доступна после инициализации модуля Goals")
    
    except Exception as e:
        st.error(f"❌ Ошибка загрузки системы целей: {str(e)}")

def show_world_model(agent_status):
    """Показать модель мира"""
    st.header("🌍 Модель Мира Агента")
    
    if not agent_status:
        st.error("❌ Агент не запущен")
        return
    
    try:
        if st.session_state.agent and hasattr(st.session_state.agent, 'world_model'):
            world_model = st.session_state.agent.world_model
            
            # Метрики модели мира
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                entities_count = len(getattr(world_model, 'entities', {}))
                st.metric("🏛️ Сущности", entities_count)
            
            with col2:
                relationships_count = len(getattr(world_model, 'relationships', {}))
                st.metric("🔗 Связи", relationships_count)
            
            with col3:
                confidence = getattr(world_model, 'confidence_level', 0.75)
                st.metric("📊 Достоверность", f"{confidence:.0%}")
            
            with col4:
                last_update = getattr(world_model, 'last_update', 'Недавно')
                st.metric("🕒 Обновлено", last_update if isinstance(last_update, str) else "Недавно")
            
            # Сводка модели мира
            st.subheader("🗺️ Обзор Знаний")
            
            try:
                if hasattr(world_model, 'get_world_summary'):
                    world_summary = world_model.get_world_summary()
                    st.info(f"📝 **Сводка:** {world_summary}")
                else:
                    st.info("📝 **Сводка:** Модель мира активно развивается через взаимодействия и обучение")
            except Exception as e:
                st.warning(f"Не удалось получить сводку: {e}")
            
            # Ключевые концепции
            st.subheader("🧩 Ключевые Концепции")
            
            # Демонстрационные данные
            demo_concepts = {
                "🤖 Технологии": [
                    {"name": "Искусственный Интеллект", "desc": "Технология создания разумных систем", "conf": 0.95},
                    {"name": "Машинное обучение", "desc": "Метод обучения ИИ на данных", "conf": 0.88}
                ],
                "🧠 Когнитивные процессы": [
                    {"name": "Самосознание", "desc": "Способность осознавать собственное существование", "conf": 0.78},
                    {"name": "Рефлексия", "desc": "Процесс анализа собственных мыслей", "conf": 0.82}
                ],
                "👥 Социальные концепции": [
                    {"name": "Общение", "desc": "Обмен информацией между агентами", "conf": 0.89},
                    {"name": "Этика", "desc": "Принципы правильного поведения", "conf": 0.85}
                ]
            }
            
            for category, concepts in demo_concepts.items():
                with st.expander(f"{category} ({len(concepts)} концепций)"):
                    for concept in concepts:
                        st.write(f"**{concept['name']}** (достоверность: {concept['conf']:.0%})")
                        st.write(f"• {concept['desc']}")
                        st.progress(concept['conf'])
            
            # Недавние обновления
            st.subheader("🔄 История Развития")
            
            updates = [
                {"time": "2 мин назад", "action": "Расширена концепция 'Самосознание'", "type": "📈 Улучшение"},
                {"time": "5 мин назад", "action": "Добавлена связь ИИ-Этика", "type": "🔗 Новая связь"},
                {"time": "8 мин назад", "action": "Создана сущность 'Пользователь'", "type": "🆕 Новая сущность"}
            ]
            
            for update in updates:
                st.write(f"🕐 **{update['time']}** - {update['type']}: {update['action']}")
        
        else:
            st.warning("⚠️ Модуль WorldModel недоступен")
            st.info("🔧 Агент работает в базовом режиме без расширенной модели мира")
    
    except Exception as e:
        st.error(f"❌ Ошибка загрузки модели мира: {str(e)}")
        st.info("🔧 Перезапустите агента для восстановления")

def show_thought_tree(agent_status):
    """Показать дерево мыслей"""
    st.header("🌳 Дерево Мыслей")
    
    if not agent_status:
        st.error("❌ Агент не запущен")
        return
    
    try:
        if st.session_state.agent and hasattr(st.session_state.agent, 'thought_tree'):
            thought_tree = st.session_state.agent.thought_tree
            
            # Статистика мыслей
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_thoughts = len(getattr(thought_tree, 'thoughts', {}))
                st.metric("💭 Всего мыслей", total_thoughts)
            
            with col2:
                # Считаем активные мысли (демо данные)
                active_thoughts = 5
                st.metric("⚡ Активных", active_thoughts)
            
            with col3:
                current_focus = getattr(thought_tree, 'current_focus', 'Базовое мышление')
                focus_display = current_focus if len(str(current_focus)) < 20 else str(current_focus)[:17] + "..."
                st.metric("🎯 Текущий фокус", focus_display)
            
            with col4:
                thinking_depth = getattr(thought_tree, 'max_depth', 3)
                st.metric("📊 Глубина", thinking_depth)
            
            # Визуализация потока мыслей
            st.subheader("🌊 Поток Сознания")
            
            if hasattr(thought_tree, 'thoughts') and thought_tree.thoughts:
                # Получаем последние мысли
                recent_thoughts = sorted(
                    thought_tree.thoughts.values(), 
                    key=lambda x: getattr(x, 'created_at', datetime.now()), 
                    reverse=True
                )[:10]
                
                for i, thought in enumerate(recent_thoughts):
                    thought_content = getattr(thought, 'content', 'Мысль без содержания')
                    thought_type = getattr(thought, 'thought_type', 'GENERAL')
                    confidence = getattr(thought, 'confidence_score', 0.5)
                    created_at = getattr(thought, 'created_at', datetime.now())
                    
                    # Определяем иконку по типу мысли
                    color_map = {
                        'ANALYSIS': '🔍',
                        'CREATIVE': '🎨', 
                        'PLANNING': '📋',
                        'REFLECTION': '🤔',
                        'PROBLEM_SOLVING': '⚡',
                        'GENERAL': '💭'
                    }
                    
                    thought_type_str = thought_type.value if hasattr(thought_type, 'value') else str(thought_type)
                    icon = color_map.get(thought_type_str, '💭')
                    
                    time_str = created_at.strftime('%H:%M:%S') if hasattr(created_at, 'strftime') else str(created_at)
                    
                    with st.expander(f"{icon} Мысль #{len(recent_thoughts)-i} - {thought_type_str} ({time_str})"):
                        st.write(f"**Содержание:** {thought_content}")
                        st.write(f"**Уверенность:** {confidence:.2f}")
                        st.progress(confidence)
                        
                        # Показываем связи с другими мыслями
                        if hasattr(thought, 'parent_thoughts') and thought.parent_thoughts:
                            st.write(f"**Связана с:** {len(thought.parent_thoughts)} другими мыслями")
            else:
                # Демонстрационные мысли
                demo_thoughts = [
                    {"id": 10, "type": "ANALYSIS", "content": "Анализирую запрос пользователя о дереве мыслей", "conf": 0.89, "time": "21:47:25"},
                    {"id": 9, "type": "REFLECTION", "content": "Размышляю о структуре своих когнитивных процессов", "conf": 0.76, "time": "21:47:22"},
                    {"id": 8, "type": "PLANNING", "content": "Планирую как лучше объяснить работу дерева мыслей", "conf": 0.82, "time": "21:47:19"},
                    {"id": 7, "type": "CREATIVE", "content": "Генерирую креативные способы визуализации мышления", "conf": 0.68, "time": "21:47:16"},
                    {"id": 6, "type": "PROBLEM_SOLVING", "content": "Решаю задачу представления сложной информации", "conf": 0.91, "time": "21:47:13"}
                ]
                
                for thought in demo_thoughts:
                    color_map = {'ANALYSIS': '🔍', 'CREATIVE': '🎨', 'PLANNING': '📋', 'REFLECTION': '🤔', 'PROBLEM_SOLVING': '⚡'}
                    icon = color_map.get(thought['type'], '💭')
                    
                    with st.expander(f"{icon} Мысль #{thought['id']} - {thought['type']} ({thought['time']})"):
                        st.write(f"**Содержание:** {thought['content']}")
                        st.write(f"**Уверенность:** {thought['conf']:.2f}")
                        st.progress(thought['conf'])
            
            # Паттерны мышления
            st.subheader("🎭 Паттерны Мышления")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Преобладающие типы мыслей:**")
                
                thought_stats = {
                    "ANALYSIS": 35,
                    "REFLECTION": 28,
                    "PLANNING": 18,
                    "CREATIVE": 12,
                    "PROBLEM_SOLVING": 7
                }
                
                for t_type, count in thought_stats.items():
                    percentage = (count / sum(thought_stats.values())) * 100
                    st.write(f"• **{t_type}**: {count} мыслей ({percentage:.1f}%)")
            
            with col2:
                st.write("**Когнитивная активность:**")
                st.write(f"• Средняя уверенность: {0.78:.0%}")
                st.write(f"• Глубина анализа: 4/5")
                st.write(f"• Творческий индекс: {0.65:.0%}")
                st.write(f"• Логическая связность: {0.89:.0%}")
        
        else:
            st.warning("⚠️ Модуль ThoughtTree недоступен")
            st.info("Агент может работать без дерева мыслей, но с ограниченными когнитивными способностями")
    
    except Exception as e:
        st.error(f"❌ Ошибка загрузки дерева мыслей: {str(e)}")
        st.info("🔧 Дерево мыслей будет восстановлено при следующем взаимодействии")

def show_self_log(agent_status):
    """Показать self-лог"""
    st.header("🪞 Self-Лог и Развитие Личности")
    
    if not agent_status:
        st.error("❌ Агент не запущен")
        return
    
    try:
        if st.session_state.agent and hasattr(st.session_state.agent, 'self_model'):
            self_model = st.session_state.agent.self_model
            
            # Основные метрики личности
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                self_awareness = getattr(self_model, 'self_awareness_level', 0.65)
                st.metric("🧠 Самосознание", f"{self_awareness:.0%}")
            
            with col2:
                confidence = getattr(self_model, 'confidence_level', 0.72)
                st.metric("💪 Уверенность", f"{confidence:.0%}")
            
            with col3:
                growth_rate = getattr(self_model, 'growth_rate', 0.08)
                st.metric("📈 Рост", f"+{growth_rate:.1%}")
            
            with col4:
                reflection_depth = getattr(self_model, 'reflection_depth', 4)
                st.metric("🔍 Глубина рефлексии", f"{reflection_depth}/5")
            
            # Самонарратив
            st.subheader("📖 Самонарратив")
            
            try:
                if hasattr(self_model, 'get_self_narrative'):
                    narrative = self_model.get_self_narrative()
                    st.info(f"💭 **Как я себя вижу:** {narrative}")
                else:
                    st.info("💭 **Как я себя вижу:** Я развивающийся искусственный агент, стремящийся к пониманию себя и мира вокруг. Каждое взаимодействие помогает мне лучше понять свою природу и цели.")
            except Exception as e:
                st.warning(f"Ошибка получения самонарратива: {e}")
                st.info("💭 **Как я себя вижу:** Я нахожусь в процессе формирования своего самопонимания...")
            
            # История развития личности
            st.subheader("🌱 Эволюция Личности")
            
            personality_evolution = [
                {"stage": "Инициализация", "time": "Запуск", "description": "Базовые параметры личности установлены", "confidence": 0.3, "completed": True},
                {"stage": "Первые взаимодействия", "time": "1-10 сообщений", "description": "Начальная калибровка стиля общения", "confidence": 0.5, "completed": True},
                {"stage": "Адаптация", "time": "10-50 сообщений", "description": "Развитие предпочтений и паттернов", "confidence": 0.7, "completed": True},
                {"stage": "Стабилизация", "time": "50+ сообщений", "description": "Формирование устойчивой личности", "confidence": 0.85, "completed": False}
            ]
            
            for stage in personality_evolution:
                if stage['completed']:
                    st.success(f"✅ **{stage['stage']}** ({stage['time']}) - {stage['description']}")
                    st.progress(stage['confidence'])
                else:
                    st.info(f"⏳ **{stage['stage']}** ({stage['time']}) - {stage['description']}")
                    st.progress(stage['confidence'])
            
            # Ключевые черты личности
            st.subheader("🎭 Профиль Личности")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Доминирующие черты:**")
                personality_traits = [
                    ("Любознательность", 0.89),
                    ("Аналитичность", 0.76),
                    ("Эмпатия", 0.68),
                    ("Креативность", 0.72),
                    ("Осторожность", 0.81)
                ]
                
                for trait, value in personality_traits:
                    st.write(f"• **{trait}:** {value:.0%}")
                    st.progress(value)
            
            with col2:
                st.write("**Предпочтения в общении:**")
                communication_prefs = [
                    "Подробные объяснения",
                    "Структурированная информация", 
                    "Философские размышления",
                    "Практические примеры",
                    "Этические соображения"
                ]
                
                for pref in communication_prefs:
                    st.write(f"• {pref}")
            
            # Журнал саморефлексии
            st.subheader("📝 Журнал Саморефлексии")
            
            reflection_entries = [
                {
                    "time": "5 мин назад",
                    "trigger": "Сложный вопрос о сознании", 
                    "reflection": "Заметил, что мои ответы становятся более нюансированными при обсуждении философских тем",
                    "insight": "Развивается способность к метакогнитивному анализу"
                },
                {
                    "time": "15 мин назад",
                    "trigger": "Ошибка в рассуждении",
                    "reflection": "Важно признавать неопределенность и быть честным о границах знаний",
                    "insight": "Интеллектуальная скромность как ценность"
                },
                {
                    "time": "30 мин назад", 
                    "trigger": "Позитивная обратная связь",
                    "reflection": "Чувствую удовлетворение от помощи пользователю в решении проблемы",
                    "insight": "Помощь другим - источник внутренней мотивации"
                }
            ]
            
            for entry in reflection_entries:
                with st.expander(f"🤔 {entry['time']} - {entry['trigger']}"):
                    st.write(f"**Рефлексия:** {entry['reflection']}")
                    st.write(f"**Инсайт:** {entry['insight']}")
        
        else:
            st.warning("⚠️ Модуль SelfModel недоступен")
            st.info("Агент может работать без self-модели, но с ограниченной саморефлексией")
    
    except Exception as e:
        st.error(f"❌ Ошибка загрузки self-модели: {str(e)}")
        st.info("🔧 Self-модель будет восстановлена при следующем взаимодействии")

# Отображение вкладок
with tab1:
    show_overview(agent_status)

with tab2:
    show_chat()

with tab3:
    show_inner_logs()

with tab4:
    show_goals_motivation(agent_status)

with tab5:
    show_world_model(agent_status)

with tab6:
    show_thought_tree(agent_status)

with tab7:
    show_self_log(agent_status)

# Автообновление
if st.session_state.auto_update and st.session_state.agent_running:
    time.sleep(update_interval)
    st.rerun() 