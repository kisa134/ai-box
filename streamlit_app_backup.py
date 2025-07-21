import streamlit as st
import asyncio
import threading
import time
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import networkx as nx
import plotly.figure_factory as ff

from autonomous_agent import AutonomousAgent

# Конфигурация страницы
st.set_page_config(
    page_title="Автономный Агент с Самосознанием",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class AgentInterface:
    """Интерфейс для управления агентом"""
    
    def __init__(self):
        self.agent = None
        self.agent_thread = None
        self.is_running = False
        
    def start_agent(self):
        """Запустить агента в отдельном потоке"""
        if not self.is_running:
            self.agent = AutonomousAgent("Автономный Агент", "agent_data")
            self.is_running = True
            
            # Запустить в отдельном потоке
            self.agent_thread = threading.Thread(
                target=self._run_agent_loop,
                daemon=True
            )
            self.agent_thread.start()
            return True
        return False
    
    def _run_agent_loop(self):
        """Запустить асинхронный цикл агента"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.agent.run_consciousness_cycle())
        except Exception as e:
            print(f"Ошибка в цикле агента: {e}")
            self.is_running = False
    
    def stop_agent(self):
        """Остановить агента"""
        if self.agent and self.is_running:
            self.agent.stop()
            self.is_running = False
            return True
        return False
    
    def get_agent_status(self):
        """Получить статус агента"""
        if self.agent:
            return self.agent.get_status_report()
        return None
    
    def send_message(self, message: str):
        """Отправить сообщение агенту"""
        if self.agent and self.is_running:
            try:
                return self.agent.process_input(message)
            except Exception as e:
                return f"Ошибка при обработке сообщения: {str(e)}"
        return "Агент не запущен"

# Инициализация интерфейса
if 'agent_interface' not in st.session_state:
    st.session_state.agent_interface = AgentInterface()

def main():
    """Основная функция интерфейса"""
    
    st.title("🤖 Автономный Агент с Самосознанием")
    st.markdown("---")
    
    # Боковая панель управления
    with st.sidebar:
        st.header("Управление Агентом")
        
        # Статус агента
        if st.session_state.agent_interface.is_running:
            st.success("🟢 Агент запущен")
            if st.button("⏹️ Остановить агента"):
                st.session_state.agent_interface.stop_agent()
                st.rerun()
        else:
            st.error("🔴 Агент остановлен")
            if st.button("▶️ Запустить агента"):
                if st.session_state.agent_interface.start_agent():
                    st.success("Агент запущен!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Не удалось запустить агента")
        
        st.markdown("---")
        
        # Настройки обновления
        auto_refresh = st.checkbox("Автообновление", value=True)
        if auto_refresh:
            refresh_interval = st.selectbox(
                "Интервал обновления (сек)",
                [1, 3, 5, 10, 30],
                index=2
            )
        
        st.markdown("---")
        
        # Быстрые команды
        st.subheader("⚡ Быстрые Команды")
        if st.button("🔄 Принудительная Рефлексия"):
            if st.session_state.agent_interface.agent:
                st.session_state.agent_interface.agent.reflect_on_state(
                    "Принудительная рефлексия", 
                    {"trigger": "user_request", "timestamp": datetime.now().isoformat()}
                )
                st.success("Рефлексия запущена!")
        
        if st.button("💾 Сохранить Состояние"):
            if st.session_state.agent_interface.agent:
                st.session_state.agent_interface.agent.save_state()
                st.success("Состояние сохранено!")
    
    # Основной интерфейс с вкладками
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Обзор",
        "💬 Чат с Агентом", 
        "🧠 Внутренние Логи", 
        "🎯 Цели и Мотивация", 
        "🌍 Модель Мира", 
        "💭 Дерево Мыслей",
        "🪞 Self-Лог"
    ])
    
    # Получить данные агента
    agent_status = st.session_state.agent_interface.get_agent_status()
    
    with tab1:
        show_overview(agent_status)
    
    with tab2:
        show_chat_interface(agent_status)
    
    with tab3:
        show_inner_logs(agent_status)
    
    with tab4:
        show_goals_motivation(agent_status)
    
    with tab5:
        show_world_model(agent_status)
    
    with tab6:
        show_thought_tree(agent_status)
    
    with tab7:
        show_self_log(agent_status)
    
    # Автообновление
    if auto_refresh and st.session_state.agent_interface.is_running:
        time.sleep(refresh_interval)
        st.rerun()

def show_overview(agent_status):
    """Показать обзор агента"""
    
    st.header("📊 Обзор Состояния Агента")
    
    if not agent_status:
        st.warning("Агент не запущен или данные недоступны")
        return
    
    # Основные метрики
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Циклы Сознания",
            agent_status['consciousness_cycles'],
            delta=1 if agent_status['is_running'] else 0
        )
    
    with col2:
        uptime_hours = agent_status.get('uptime_hours', 0)
        if uptime_hours < 1:
            uptime_display = f"{uptime_hours * 60:.0f} мин"
        else:
            uptime_display = f"{uptime_hours:.1f} ч"
        
        st.metric(
            "Время Работы",
            uptime_display
        )
    
    with col3:
        inner_state = agent_status.get('inner_state', {})
        if isinstance(inner_state, str):
            # Парсим строку состояния
            energy_val = 0.0
            try:
                if "Энергия:" in inner_state:
                    energy_line = [line for line in inner_state.split('\n') if 'Энергия:' in line][0]
                    energy_val = float(energy_line.split(':')[1].strip())
            except:
                pass
        else:
            energy_val = inner_state.get('energy_level', 0)
            
        st.metric(
            "Энергия",
            f"{energy_val:.2f}",
            delta=None
        )
    
    with col4:
        if isinstance(inner_state, str):
            # Парсим строку состояния
            eval_val = 0.0
            try:
                if "Самооценка:" in inner_state:
                    eval_line = [line for line in inner_state.split('\n') if 'Самооценка:' in line][0]
                    eval_val = float(eval_line.split(':')[1].strip())
            except:
                pass
        else:
            eval_val = inner_state.get('self_evaluation', 0)
            
        st.metric(
            "Самооценка", 
            f"{eval_val:.2f}",
            delta=None
        )
    
    # Состояние агента
    st.subheader("Текущее Состояние")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if isinstance(inner_state, str):
            # Извлекаем состояния из строки
            emotional_state = "неизвестно"
            cognitive_state = "неизвестно" 
            motivation_level = "неизвестно"
            
            try:
                lines = inner_state.split('\n')
                for line in lines:
                    if "Эмоциональное состояние:" in line:
                        emotional_state = line.split(':')[1].strip()
                    elif "Когнитивное состояние:" in line:
                        cognitive_state = line.split(':')[1].strip()
                    elif "Мотивация:" in line:
                        motivation_level = line.split(':')[1].strip()
            except:
                pass
                
            st.write("**Эмоциональное состояние:**", emotional_state)
            st.write("**Когнитивное состояние:**", cognitive_state) 
            st.write("**Уровень мотивации:**", motivation_level)
        else:
            st.write("**Эмоциональное состояние:**", inner_state.get('emotional_state', 'неизвестно'))
            st.write("**Когнитивное состояние:**", inner_state.get('cognitive_state', 'неизвестно'))
            st.write("**Уровень мотивации:**", inner_state.get('motivation_level', 'неизвестно'))
    
    with col2:
        st.write("**Текущая цель:**", agent_status.get('current_goal', 'Нет активной цели'))
        
        # Статистика модулей
        goals_count = agent_status.get('goals_count', 0)
        memory_stats = agent_status.get('memory_stats', {})
        active_thoughts = agent_status.get('active_thoughts', 0)
        
        st.write("**Активные цели:**", goals_count)
        st.write("**Эпизодов в памяти:**", memory_stats.get('local_episodes', 0))
        st.write("**Активные мысли:**", active_thoughts)
    
    # График состояния
    st.subheader("Визуализация Состояния")
    
    # Круговая диаграмма состояний
    fig = go.Figure(data=go.Scatterpolar(
        r=[
            energy_val * 100,
            eval_val * 100,
            max(0, min(100, 80)),  # Базовое спокойствие
            min(100, goals_count * 25),  # Нормализованные цели
            min(100, active_thoughts * 10)  # Нормализованные мысли
        ],
        theta=['Энергия', 'Самооценка', 'Спокойствие', 'Цели', 'Мысли'],
        fill='toself',
        name='Состояние Агента'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Радарная Диаграмма Состояния"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_inner_logs(agent_status):
    """Показать внутренние логи агента"""
    
    st.header("🧠 Внутренние Логи Мышления")
    
    if not agent_status:
        st.warning("Агент не запущен или данные недоступны")
        return
    
    # Получить публичные мысли
    agent = st.session_state.agent_interface.agent
    if agent:
        public_thoughts = agent.get_public_log()
        
        if public_thoughts:
            st.subheader("Поток Сознания")
            
            # Показать последние мысли
            for i, thought in enumerate(reversed(public_thoughts[-10:])):
                with st.expander(f"Цикл #{thought['cycle']} - {thought['timestamp'][:19]}"):
                    st.write("**Внутреннее состояние:**")
                    st.text(thought['inner_state_summary'])
                    
                    st.write("**Текущая цель:**", thought['current_goal'])
                    st.write("**Фокус внимания:**", thought['focused_thought'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Самооценка", f"{thought['self_evaluation']:.2f}")
                    with col2:
                        st.metric("Мотивация", thought['motivation_level'])
        else:
            st.info("Пока нет записей потока сознания")
    
    # Временной график состояний
    if agent and public_thoughts:
        st.subheader("Динамика Состояний")
        
        # Подготовить данные для графика
        timestamps = [datetime.fromisoformat(t['timestamp']) for t in public_thoughts]
        evaluations = [t['self_evaluation'] for t in public_thoughts]
        cycles = [t['cycle'] for t in public_thoughts]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=evaluations,
            mode='lines+markers',
            name='Самооценка',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Динамика Самооценки",
            xaxis_title="Время",
            yaxis_title="Самооценка (0-1)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_goals_motivation(agent_status):
    """Показать цели и мотивацию"""
    
    st.header("🎯 Цели и Система Мотивации")
    
    if not agent_status:
        st.warning("Агент не запущен или данные недоступны")
        return
    
    agent = st.session_state.agent_interface.agent
    if not agent:
        return
    
    # Цели агента
    st.subheader("Активные Цели")
    
    active_goals = agent.goals.get_active_goals()
    
    if active_goals:
        for goal in active_goals:
            with st.expander(f"🎯 {goal.description}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Тип:**", goal.goal_type)
                    st.write("**Приоритет:**", goal.priority.value)
                
                with col2:
                    st.write("**Прогресс:**", f"{goal.progress:.1%}")
                    st.progress(goal.progress)
                
                with col3:
                    st.write("**Попытки:**", goal.attempts)
                    st.write("**Создана:**", goal.created_at.strftime("%Y-%m-%d %H:%M"))
                
                if goal.success_criteria:
                    st.write("**Критерии успеха:**")
                    for criterion in goal.success_criteria:
                        st.write(f"- {criterion}")
    else:
        st.info("Нет активных целей")
    
    # Иерархия целей
    st.subheader("Иерархия Целей")
    goal_hierarchy = agent.goals.get_goal_hierarchy()
    
    if goal_hierarchy['all_goals']:
        # Создать граф целей
        G = nx.DiGraph()
        
        # Добавить узлы
        for goal_id, goal_data in goal_hierarchy['all_goals'].items():
            G.add_node(goal_id, 
                      label=goal_data['description'][:30] + "...",
                      progress=goal_data['progress'],
                      priority=goal_data['priority'])
        
        # Добавить связи
        for goal_id, goal_data in goal_hierarchy['all_goals'].items():
            if goal_data['parent_id']:
                G.add_edge(goal_data['parent_id'], goal_id)
        
        if G.nodes():
            # Простое отображение иерархии
            st.write("**Структура целей:**")
            for root_goal_id in goal_hierarchy['root_goals']:
                if root_goal_id in goal_hierarchy['all_goals']:
                    root_goal = goal_hierarchy['all_goals'][root_goal_id]
                    st.write(f"🎯 **{root_goal['description']}** (прогресс: {root_goal['progress']:.1%})")
                    
                    # Показать подцели
                    for child_id in root_goal.get('children_ids', []):
                        if child_id in goal_hierarchy['all_goals']:
                            child_goal = goal_hierarchy['all_goals'][child_id]
                            st.write(f"  └─ {child_goal['description']} (прогресс: {child_goal['progress']:.1%})")
    
    # Система мотивации
    st.subheader("Система Мотивации")
    
    motivation_system = agent.self_model.motivation_system
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Внутренняя мотивация:**")
        for motivation, value in motivation_system.intrinsic_motivations.items():
            st.write(f"- {motivation}: {value:.2f}")
            st.progress(value)
    
    with col2:
        st.write("**Внешняя мотивация:**")
        for motivation, value in motivation_system.extrinsic_motivations.items():
            st.write(f"- {motivation}: {value:.2f}")
            st.progress(value)
    
    # График мотивации
    motivation_data = {
        'Тип': ['Внутренняя'] * len(motivation_system.intrinsic_motivations) + 
               ['Внешняя'] * len(motivation_system.extrinsic_motivations),
        'Мотивация': list(motivation_system.intrinsic_motivations.keys()) + 
                    list(motivation_system.extrinsic_motivations.keys()),
        'Значение': list(motivation_system.intrinsic_motivations.values()) + 
                   list(motivation_system.extrinsic_motivations.values())
    }
    
    df_motivation = pd.DataFrame(motivation_data)
    
    fig = px.bar(df_motivation, x='Мотивация', y='Значение', color='Тип',
                title="Профиль Мотивации Агента")
    fig.update_layout(xaxis_tickangle=45)
    
    st.plotly_chart(fig, use_container_width=True)

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
            
            if hasattr(world_model, 'entities') and world_model.entities:
                # Группировка по типам
                entity_types = {}
                for entity_id, entity in world_model.entities.items():
                    entity_type = getattr(entity, 'type', 'Общее')
                    if entity_type not in entity_types:
                        entity_types[entity_type] = []
                    entity_types[entity_type].append(entity)
                
                for entity_type, entities in entity_types.items():
                    with st.expander(f"📁 {entity_type} ({len(entities)} элементов)"):
                        for entity in entities[:5]:  # Показываем первые 5
                            name = getattr(entity, 'name', entity_id)
                            description = getattr(entity, 'description', 'Описание отсутствует')
                            confidence = getattr(entity, 'confidence', 0.5)
                            
                            st.write(f"**{name}**")
                            st.write(f"• {description}")
                            st.progress(confidence)
            else:
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
                entity_types[entity_type] = []
            entity_types[entity_type].append(entity)
        
        for entity_type, entities in entity_types.items():
            with st.expander(f"📁 {entity_type} ({len(entities)} шт.)"):
                for entity in entities:
                    st.write(f"**{entity.name}**")
                    if entity.properties:
                        for prop_key, prop_data in entity.properties.items():
                            if isinstance(prop_data, dict) and 'value' in prop_data:
                                st.write(f"- {prop_key}: {prop_data['value']}")
                    st.write(f"Источник: {entity.source}")
                    st.write("---")
    else:
        st.info("Пока нет сущностей в модели мира")
    
    # Факты
    st.subheader("Факты о Мире")
    
    recent_facts = sorted(agent.world_model.facts.values(), 
                         key=lambda x: x.timestamp, 
                         reverse=True)[:10]
    
    if recent_facts:
        for fact in recent_facts:
            confidence_color = "green" if fact.confidence > 0.7 else "orange" if fact.confidence > 0.4 else "red"
            st.markdown(f"**{fact.statement}**")
            st.markdown(f"<span style='color: {confidence_color}'>Уверенность: {fact.confidence:.2f}</span>", 
                       unsafe_allow_html=True)
            st.write(f"Источник: {fact.source}")
            st.write(f"Время: {fact.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write("---")
    else:
        st.info("Пока нет фактов о мире")
    
    # Контексты
    st.subheader("Контексты")
    
    if agent.world_model.contexts:
        for context_id, context in agent.world_model.contexts.items():
            is_current = context_id == agent.world_model.current_context_id
            icon = "🎯" if is_current else "📋"
            
            with st.expander(f"{icon} {context.name} {'(текущий)' if is_current else ''}"):
                st.write(f"**Описание:** {context.description}")
                st.write(f"**Активные сущности:** {len(context.active_entities)}")
                st.write(f"**Релевантные факты:** {len(context.relevant_facts)}")
                st.write(f"**Создан:** {context.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.info("Нет созданных контекстов")

def show_thought_tree(agent_status):
    """Показать дерево мыслей"""
    
    st.header("💭 Дерево Мыслей и Рассуждения")
    
    if not agent_status:
        st.warning("Агент не запущен или данные недоступны")
        return
    
    agent = st.session_state.agent_interface.agent
    if not agent:
        return
    
    # Сводка рассуждений
    reasoning_summary = agent.thought_tree.get_reasoning_summary()
    st.text(reasoning_summary)
    
    # Текущий фокус
    if agent.thought_tree.current_focus:
        current_thought = agent.thought_tree.thoughts[agent.thought_tree.current_focus]
        st.subheader("🎯 Текущий Фокус Внимания")
        
        st.info(f"**{current_thought.content}**")
        st.write(f"Тип: {current_thought.thought_type.value}")
        st.write(f"Общая оценка: {current_thought.overall_score:.2f}")
    
    # Недавние мысли
    st.subheader("Недавние Мысли")
    
    recent_thoughts = sorted(agent.thought_tree.thoughts.values(), 
                           key=lambda x: x.created_at, 
                           reverse=True)[:15]
    
    if recent_thoughts:
        for thought in recent_thoughts:
            thought_icon = {
                'observation': '👁️',
                'hypothesis': '💡',
                'analysis': '🔍',
                'plan': '📋',
                'decision': '✅',
                'reflection': '🪞',
                'critique': '❗',
                'alternative': '🔄'
            }.get(thought.thought_type.value, '💭')
            
            with st.expander(f"{thought_icon} {thought.content[:50]}..."):
                st.write(f"**Полное содержание:** {thought.content}")
                st.write(f"**Тип:** {thought.thought_type.value}")
                st.write(f"**Статус:** {thought.status.value}")
                st.write(f"**Создана:** {thought.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Оценки
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Осуществимость", f"{thought.feasibility_score:.2f}")
                with col2:
                    st.metric("Уверенность", f"{thought.confidence_score:.2f}")
                with col3:
                    st.metric("Новизна", f"{thought.novelty_score:.2f}")
                with col4:
                    st.metric("Релевантность", f"{thought.relevance_score:.2f}")
                
                # Доказательства и контраргументы
                if thought.evidence:
                    st.write("**Доказательства:**")
                    for evidence in thought.evidence:
                        st.write(f"+ {evidence}")
                
                if thought.counterarguments:
                    st.write("**Контраргументы:**")
                    for counter in thought.counterarguments:
                        st.write(f"- {counter}")
    else:
        st.info("Пока нет мыслей в дереве")
    
    # Анализ типов мыслей
    if recent_thoughts:
        st.subheader("Анализ Типов Мыслей")
        
        thought_types = {}
        for thought in agent.thought_tree.thoughts.values():
            thought_type = thought.thought_type.value
            thought_types[thought_type] = thought_types.get(thought_type, 0) + 1
        
        df_thoughts = pd.DataFrame(list(thought_types.items()), columns=['Тип', 'Количество'])
        
        fig = px.pie(df_thoughts, values='Количество', names='Тип', 
                    title="Распределение Типов Мыслей")
        
        st.plotly_chart(fig, use_container_width=True)

def show_chat_interface(agent_status):
    """Показать интерфейс чата с агентом"""
    
    st.header("💬 Чат с Агентом")
    
    # Инициализация истории чата в session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'thinking_process' not in st.session_state:
        st.session_state.thinking_process = []
    
    # Проверка статуса агента
    if not agent_status:
        st.warning("⚠️ Агент не запущен. Запустите агента в боковой панели для начала чата.")
        return
    
    agent = st.session_state.agent_interface.agent
    if not agent:
        st.error("❌ Агент недоступен")
        return
    
    # Контейнер для сообщений
    chat_container = st.container()
    
    # Поле ввода внизу
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Напишите сообщение агенту:",
            key="chat_input",
            placeholder="Например: Привет! Как дела? Расскажи о своих мыслях..."
        )
    
    with col2:
        send_button = st.button("📤 Отправить", type="primary")
    
    # Обработка отправки сообщения
    if send_button and user_input.strip():
        # Добавить сообщение пользователя в историю
        user_message = {
            "type": "user",
            "content": user_input,
            "timestamp": datetime.now(),
            "id": len(st.session_state.chat_history)
        }
        st.session_state.chat_history.append(user_message)
        
        # Показать процесс мышления агента
        with st.spinner("🤖 Агент думает..."):
            try:
                # Зафиксировать начальное состояние мыслей
                initial_thoughts = len(agent.thought_tree.thoughts)
                
                # Отправить сообщение агенту
                response = agent.process_input(user_input)
                
                # Зафиксировать новые мысли
                new_thoughts = len(agent.thought_tree.thoughts) - initial_thoughts
                
                # Получить последние мысли агента
                recent_thoughts = list(agent.thought_tree.thoughts.values())[-new_thoughts:] if new_thoughts > 0 else []
                
                # Создать процесс мышления
                thinking_process = {
                    "user_message_id": user_message["id"],
                    "thoughts": [
                        {
                            "content": thought.content,
                            "type": thought.thought_type.value,
                            "score": thought.overall_score,
                            "timestamp": thought.created_at
                        } for thought in recent_thoughts
                    ],
                    "response_time": datetime.now(),
                    "new_thoughts_count": new_thoughts
                }
                
                st.session_state.thinking_process.append(thinking_process)
                
            except Exception as e:
                response = f"Извините, произошла ошибка при обработке вашего сообщения: {str(e)}"
                thinking_process = {
                    "user_message_id": user_message["id"],
                    "thoughts": [],
                    "response_time": datetime.now(),
                    "new_thoughts_count": 0,
                    "error": str(e)
                }
                st.session_state.thinking_process.append(thinking_process)
        
        # Добавить ответ агента в историю
        agent_message = {
            "type": "agent",
            "content": response,
            "timestamp": datetime.now(),
            "id": len(st.session_state.chat_history),
            "thinking_id": len(st.session_state.thinking_process) - 1
        }
        st.session_state.chat_history.append(agent_message)
        
        # Очистить поле ввода
        st.rerun()
    
    # Отображение истории чата
    with chat_container:
        if not st.session_state.chat_history:
            st.info("💡 **Начните диалог с агентом!**\n\nПримеры вопросов:\n- Привет! Расскажи о себе\n- Какие у тебя сейчас цели?\n- О чем ты думаешь?\n- Как ты оцениваешь свое состояние?")
        else:
            for i, message in enumerate(st.session_state.chat_history):
                if message["type"] == "user":
                    # Сообщение пользователя
                    st.markdown(f"""
                    <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #2196f3;">
                        <strong>👤 Вы ({message["timestamp"].strftime("%H:%M:%S")}):</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                elif message["type"] == "agent":
                    # Сообщение агента
                    st.markdown(f"""
                    <div style="background-color: #f3e5f5; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #9c27b0;">
                        <strong>🤖 Агент ({message["timestamp"].strftime("%H:%M:%S")}):</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Показать процесс мышления
                    if "thinking_id" in message and message["thinking_id"] < len(st.session_state.thinking_process):
                        thinking = st.session_state.thinking_process[message["thinking_id"]]
                        
                        if thinking["thoughts"]:
                            with st.expander(f"🧠 Процесс мышления ({thinking['new_thoughts_count']} новых мыслей)", expanded=False):
                                for thought in thinking["thoughts"]:
                                    thought_icon = {
                                        'observation': '👁️',
                                        'hypothesis': '💡',
                                        'analysis': '🔍',
                                        'plan': '📋',
                                        'decision': '✅',
                                        'reflection': '🪞',
                                        'critique': '❗',
                                        'alternative': '🔄'
                                    }.get(thought["type"], '💭')
                                    
                                    confidence_color = "green" if thought["score"] > 0.7 else "orange" if thought["score"] > 0.4 else "red"
                                    
                                    st.markdown(f"""
                                    <div style="background-color: #f8f9fa; padding: 8px; border-radius: 5px; margin: 3px 0; border-left: 3px solid #6c757d;">
                                        <strong>{thought_icon} {thought["type"].title()}:</strong><br>
                                        {thought["content"]}<br>
                                        <small style="color: {confidence_color};">Уверенность: {thought["score"]:.2f}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
    
    # Кнопки управления чатом
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Очистить Чат"):
            st.session_state.chat_history = []
            st.session_state.thinking_process = []
            st.success("Чат очищен!")
            st.rerun()
    
    with col2:
        if st.button("💾 Экспорт Чата"):
            chat_export = {
                "export_time": datetime.now().isoformat(),
                "messages": st.session_state.chat_history,
                "thinking_processes": st.session_state.thinking_process
            }
            st.download_button(
                label="📥 Скачать JSON",
                data=json.dumps(chat_export, ensure_ascii=False, indent=2, default=str),
                file_name=f"agent_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("📊 Статистика Чата"):
            if st.session_state.chat_history:
                user_messages = [m for m in st.session_state.chat_history if m["type"] == "user"]
                agent_messages = [m for m in st.session_state.chat_history if m["type"] == "agent"]
                total_thoughts = sum(len(tp.get("thoughts", [])) for tp in st.session_state.thinking_process)
                
                st.info(f"""
                **Статистика чата:**
                - 💬 Всего сообщений: {len(st.session_state.chat_history)}
                - 👤 От пользователя: {len(user_messages)}
                - 🤖 От агента: {len(agent_messages)}
                - 🧠 Всего мыслей: {total_thoughts}
                - ⏱️ Начало чата: {st.session_state.chat_history[0]["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if st.session_state.chat_history else "Не начат"}
                """)

def show_self_log(agent_status):
    """Показать self-лог и рефлексии"""
    
    st.header("🪞 Self-Лог и Рефлексии")
    
    if not agent_status:
        st.warning("Агент не запущен или данные недоступны")
        return
    
    agent = st.session_state.agent_interface.agent
    if not agent:
        return
    
    # Самонарратив
    st.subheader("Самоописание Агента")
    
    if agent.self_model:
        try:
            self_narrative = agent.self_model.get_self_narrative()
            st.text(self_narrative)
        except Exception as e:
            st.warning(f"Не удалось получить самоописание: {e}")
            st.info("Агент еще развивает понимание себя...")
    else:
        st.info("Self-модель недоступна")
    
    # История саморефлексии
    st.subheader("История Саморефлексии")
    
    self_story = agent.get_self_story()
    
    if self_story:
        for entry in reversed(self_story[-10:]):  # Последние 10 записей
            with st.expander(f"📝 {entry['timestamp'][:19]} - {entry.get('type', 'event')}"):
                if entry['type'] == 'reflection':
                    st.write(f"**Ключевые инсайты:** {entry.get('key_insights', 'Нет данных')}")
                    st.write(f"**Самооценка:** {entry.get('self_evaluation', 0):.2f}")
                
                st.json(entry)
    else:
        st.info("Пока нет записей в self-логе")
    
    # Рефлексии
    st.subheader("Детальные Рефлексии")
    
    if agent.self_model.reflections:
        for reflection in reversed(agent.self_model.reflections[-5:]):  # Последние 5
            with st.expander(f"🤔 {reflection.topic} - {reflection.timestamp.strftime('%Y-%m-%d %H:%M')}"):
                st.write("**Содержание рефлексии:**")
                st.text(reflection.content)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Эмоциональное воздействие", f"{reflection.emotional_impact:.2f}")
                with col2:
                    st.metric("Ценность обучения", f"{reflection.learning_value:.2f}")
                
                if reflection.insights:
                    st.write("**Ключевые инсайты:**")
                    for insight in reflection.insights:
                        st.write(f"💡 {insight}")
                
                if reflection.action_items:
                    st.write("**Пункты к действию:**")
                    for action in reflection.action_items:
                        st.write(f"📋 {action}")
    else:
        st.info("Пока нет рефлексий")
    
    # Развитие личности
    st.subheader("Развитие Личности")
    
    personality = agent.self_model.personality
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Доминирующие черты личности:**")
        dominant_traits = personality.get_dominant_traits(5)
        for trait, value in dominant_traits:
            st.write(f"- {trait}: {value:.2f}")
            st.progress(value)
    
    with col2:
        st.write("**Основные ценности:**")
        core_values = personality.get_core_values(5)
        for value, strength in core_values:
            st.write(f"- {value}: {strength:.2f}")
            st.progress(strength)

if __name__ == "__main__":
    main() 