import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

# Импорт модулей агента
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.memory_module import MemoryModule
from core.goal_module import GoalModule, GoalPriority
from core.inner_state_module import InnerStateModule, EmotionalState, CognitiveState, MotivationLevel
from core.world_model_module import WorldModelModule
from core.thought_tree_module import ThoughtTreeModule, ThoughtType
from core.self_model_module import SelfModelModule
from core.llm_module import LLMModule
from config import Config

class AutonomousAgent:
    """
    Автономный агент с самосознанием
    
    Архитектурные компоненты:
    - Цели (Goal Management): иерархия долгосрочных и краткосрочных целей
    - Данные о мире (World Model): модель восприятия и обработки контекста
    - Внутренние состояния (Inner State): самонаблюдение и самооценка
    - Память (Memory): векторное хранение эпизодов и опыта
    - Мышление (Thought Process): дерево мыслей и критический анализ
    - Self-модель (Self-Model): рефлексия и мотивация
    """
    
    def __init__(self, agent_name: str = "Автономный Агент", data_dir: str = "agent_data"):
        self.agent_name = agent_name
        self.data_dir = data_dir
        self.created_at = datetime.now()
        self.is_running = False
        self.initialization_complete = False
        self.initialization_errors = []
        
        # Создать директорию для данных
        try:
            os.makedirs(data_dir, exist_ok=True)
            os.makedirs(os.path.join(data_dir, "core"), exist_ok=True)
        except Exception as e:
            print(f"⚠️  Предупреждение: не удалось создать директории: {e}")
        
        # Настройка логирования
        self.setup_logging()
        
        # Инициализация модулей с обработкой ошибок
        self.initialize_modules()
        
        # Цикл самосознания
        self.reflection_interval = 300  # 5 минут
        self.last_reflection = datetime.now()
        self.consciousness_cycle_count = 0
        
        # Публичные логи
        self.public_thoughts: List[Dict[str, Any]] = []
        self.self_story: List[Dict[str, Any]] = []
        
        # Загрузить сохраненное состояние
        self.load_state()
        
        # Начальная инициализация
        self.initialize_agent()
        
    def setup_logging(self):
        """Настроить систему логирования"""
        try:
            log_file = os.path.join(self.data_dir, "agent.log")
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )
            
            self.logger = logging.getLogger(self.agent_name)
        except Exception as e:
            print(f"⚠️  Ошибка настройки логирования: {e}")
            # Fallback к базовому логированию
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(self.agent_name)
    
    def initialize_modules(self):
        """Инициализация модулей с обработкой ошибок"""
        print(f"🔄 Инициализация модулей агента '{self.agent_name}'...")
        
        # Память
        try:
            self.memory = MemoryModule("agent_memory")
            print("✅ MemoryModule инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации памяти: {e}")
            self.initialization_errors.append(f"Memory: {e}")
            # Fallback - создать пустой объект
            self.memory = None
        
        # Цели
        try:
            self.goals = GoalModule()
            print("✅ GoalModule инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации целей: {e}")
            self.initialization_errors.append(f"Goals: {e}")
            self.goals = None
        
        # Внутренние состояния
        try:
            self.inner_state = InnerStateModule()
            print("✅ InnerStateModule инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации внутренних состояний: {e}")
            self.initialization_errors.append(f"InnerState: {e}")
            self.inner_state = None
        
        # Модель мира
        try:
            self.world_model = WorldModelModule()
            print("✅ WorldModelModule инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации модели мира: {e}")
            self.initialization_errors.append(f"WorldModel: {e}")
            self.world_model = None
        
        # Дерево мыслей
        try:
            self.thought_tree = ThoughtTreeModule()
            print("✅ ThoughtTreeModule инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации дерева мыслей: {e}")
            self.initialization_errors.append(f"ThoughtTree: {e}")
            self.thought_tree = None
        
        # Self-модель
        try:
            self.self_model = SelfModelModule(self.agent_name)
            print("✅ SelfModelModule инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации self-модели: {e}")
            self.initialization_errors.append(f"SelfModel: {e}")
            self.self_model = None
        
        # Языковая модель
        try:
            llm_config = Config.get_llm_config()
            self.llm = LLMModule(**llm_config)
            print(f"✅ LLMModule инициализирован с типом: {llm_config['llm_type']}")
        except Exception as e:
            print(f"❌ Ошибка инициализации языковой модели: {e}")
            self.initialization_errors.append(f"LLM: {e}")
            self.llm = None
        
        # Проверка критических модулей
        if self.goals is None or self.inner_state is None:
            print("⚠️  Критические модули не инициализированы. Агент может работать с ограничениями.")
        else:
            self.initialization_complete = True
            print("🎉 Все основные модули инициализированы успешно")
    
    def is_module_available(self, module_name: str) -> bool:
        """Проверить доступность модуля"""
        module_map = {
            "memory": self.memory,
            "goals": self.goals,
            "inner_state": self.inner_state,
            "world_model": self.world_model,
            "thought_tree": self.thought_tree,
            "self_model": self.self_model,
            "llm": self.llm
        }
        return module_map.get(module_name) is not None

    def initialize_agent(self):
        """Инициализировать агента с начальными целями"""
        if not self.initialization_complete:
            self.logger.warning("Агент инициализируется с ограничениями из-за ошибок модулей")
        
        # Установить начальные цели только если модуль доступен
        if self.is_module_available("goals"):
            try:
                initial_goals = [
                    ("Понимать и помогать пользователям", GoalPriority.HIGH, "long_term"),
                    ("Развивать самосознание и рефлексию", GoalPriority.HIGH, "long_term"),
                    ("Изучать новую информацию", GoalPriority.MEDIUM, "ongoing"),
                    ("Поддерживать позитивное взаимодействие", GoalPriority.MEDIUM, "social")
                ]
                
                for goal_desc, priority, goal_type in initial_goals:
                    self.goals.add_goal(goal_desc, goal_type, priority)
                    
                self.logger.info(f"Установлено {len(initial_goals)} начальных целей")
            except Exception as e:
                self.logger.error(f"Ошибка установки начальных целей: {e}")
        
        # Начальная рефлексия только если модули доступны
        if self.is_module_available("memory") and self.is_module_available("self_model"):
            try:
                self.reflect_on_state("Инициализация агента", {
                    "event": "agent_startup",
                    "context": "Агент только что запущен",
                    "goals_count": len(self.goals.goals) if self.goals else 0,
                    "capabilities": list(self.self_model.capabilities_map.keys()) if self.self_model else [],
                    "initialization_errors": self.initialization_errors
                })
            except Exception as e:
                self.logger.error(f"Ошибка начальной рефлексии: {e}")
        
        self.logger.info(f"Агент {self.agent_name} инициализирован")
        
        # Отчет о состоянии
        if self.initialization_errors:
            self.logger.warning(f"Инициализация завершена с {len(self.initialization_errors)} ошибками")
            for error in self.initialization_errors:
                self.logger.warning(f"  - {error}")
        
    async def run_consciousness_cycle(self):
        """Запустить цикл самосознания агента"""
        self.is_running = True
        self.logger.info("Запуск цикла самосознания")
        
        try:
            while self.is_running:
                cycle_start = datetime.now()
                
                # Основной цикл сознания
                await self.consciousness_step()
                
                # Периодическая рефлексия
                if datetime.now() - self.last_reflection > timedelta(seconds=self.reflection_interval):
                    await self.periodic_reflection()
                    
                # Сохранение состояния
                if self.consciousness_cycle_count % 10 == 0:
                    self.save_state()
                    
                self.consciousness_cycle_count += 1
                
                # Пауза между циклами
                cycle_duration = (datetime.now() - cycle_start).total_seconds()
                sleep_time = max(1.0, 5.0 - cycle_duration)  # Минимум 1 секунда между циклами
                await asyncio.sleep(sleep_time)
                
        except Exception as e:
            self.logger.error(f"Ошибка в цикле сознания: {e}")
        finally:
            self.save_state()
            self.logger.info("Цикл самосознания остановлен")
            
    async def consciousness_step(self):
        """Один шаг цикла сознания"""
        
        try:
            # 1. Обновить внутреннее состояние
            if self.is_module_available("inner_state"):
                self.update_inner_state()
            
            # 2. Оценить текущие цели
            if self.is_module_available("goals"):
                current_goal = self.goals.get_current_goal()
                if current_goal:
                    # Обдумать текущую цель
                    if self.is_module_available("thought_tree"):
                        thought_id = self.thought_tree.add_thought(
                            f"Размышляю о цели: {current_goal.description}",
                            ThoughtType.ANALYSIS,
                            context={"goal_id": current_goal.id, "priority": current_goal.priority.value}
                        )
                        
                        # Установить фокус
                        self.thought_tree.set_focus(thought_id)
                    
                    # Оценить мотивацию для цели
                    if self.is_module_available("self_model") and self.is_module_available("inner_state"):
                        try:
                            world_context = self.world_model.current_context_id if self.is_module_available("world_model") else None
                            motivation = self.self_model.generate_motivation_for_goal(
                                current_goal.description,
                                {"current_context": world_context}
                            )
                            
                            # Обновить мотивацию
                            if motivation > 0.7:
                                self.inner_state.update_motivation(MotivationLevel.HIGH, ["high_goal_alignment"])
                            elif motivation > 0.5:
                                self.inner_state.update_motivation(MotivationLevel.MEDIUM, ["moderate_goal_alignment"])
                            else:
                                self.inner_state.update_motivation(MotivationLevel.LOW, ["low_goal_alignment"])
                        except Exception as e:
                            self.logger.warning(f"Ошибка оценки мотивации: {e}")
                        
            # 3. Проанализировать недавние события
            if self.is_module_available("memory"):
                try:
                    recent_episodes = self.memory.get_recent_episodes(5)
                    for episode in recent_episodes:
                        if episode['metadata'].get('type') == 'user_interaction':
                            # Обработать взаимодействие с пользователем
                            self.process_user_interaction(episode)
                except Exception as e:
                    self.logger.warning(f"Ошибка анализа недавних событий: {e}")
                    
            # 4. Обновить модель мира на основе новой информации
            if self.is_module_available("world_model"):
                try:
                    self.update_world_understanding()
                except Exception as e:
                    self.logger.warning(f"Ошибка обновления модели мира: {e}")
            
            # 5. Публиковать мысли
            try:
                self.publish_current_thoughts()
            except Exception as e:
                self.logger.warning(f"Ошибка публикации мыслей: {e}")
                
        except Exception as e:
            self.logger.error(f"Критическая ошибка в шаге сознания: {e}")
            # Продолжаем работу, несмотря на ошибки
        
    def update_inner_state(self):
        """Обновить внутреннее состояние агента"""
        
        # Оценить текущую когнитивную нагрузку
        active_thoughts = len([t for t in self.thought_tree.thoughts.values() 
                             if t.status.value == "active"])
        
        if active_thoughts > 10:
            self.inner_state.update_cognitive_state(CognitiveState.PROCESSING, "Высокая когнитивная нагрузка")
            self.inner_state.adjust_stress_level(0.1, "Много активных мыслей")
        elif active_thoughts > 5:
            self.inner_state.update_cognitive_state(CognitiveState.LEARNING, "Умеренная активность")
        else:
            self.inner_state.update_cognitive_state(CognitiveState.REFLECTING, "Спокойное состояние")
            
        # Оценить энергию на основе времени работы
        uptime = (datetime.now() - self.created_at).total_seconds() / 3600  # в часах
        energy_decay = min(0.1, uptime * 0.01)  # Медленное снижение энергии
        self.inner_state.adjust_energy_level(-energy_decay, "Естественное снижение энергии")
        
        # Провести самооценку
        self_evaluation = self.inner_state.self_evaluate(f"Цикл сознания #{self.consciousness_cycle_count}")
        
        # Обновить уверенность в self-модели
        if self_evaluation > 0.7:
            self.inner_state.update_emotional_state(EmotionalState.CONFIDENT, "Высокая самооценка")
        elif self_evaluation < 0.4:
            self.inner_state.update_emotional_state(EmotionalState.UNCERTAIN, "Низкая самооценка")
        else:
            self.inner_state.update_emotional_state(EmotionalState.NEUTRAL, "Средняя самооценка")
            
    def process_user_interaction(self, episode: Dict[str, Any]):
        """Обработать взаимодействие с пользователем"""
        
        user_input = episode.get('content', '')
        
        # Обработать ввод пользователя в модели мира
        extracted_info = self.world_model.process_user_input(user_input)
        
        # Создать мысль о взаимодействии
        thought_id = self.thought_tree.add_thought(
            f"Пользователь сказал: {user_input}",
            ThoughtType.OBSERVATION,
            context={"source": "user", "extracted_info": extracted_info}
        )
        
        # Проанализировать запрос
        if "?" in user_input:
            # Пользователь задал вопрос
            analysis_id = self.thought_tree.add_thought(
                "Пользователь задал вопрос - нужно предоставить полезный ответ",
                ThoughtType.ANALYSIS,
                parent_id=thought_id
            )
            
            self.inner_state.update_emotional_state(EmotionalState.CURIOUS, "Получен вопрос от пользователя")
            
        # Обновить мотивацию помочь
        self.self_model.motivation_system.intrinsic_motivations["help_others"] = min(1.0, 
            self.self_model.motivation_system.intrinsic_motivations.get("help_others", 0.6) + 0.05)
            
    def update_world_understanding(self):
        """Обновить понимание мира"""
        
        # Проанализировать паттерны в памяти
        recent_episodes = self.memory.get_recent_episodes(20)
        
        patterns = {}
        for episode in recent_episodes:
            episode_type = episode['metadata'].get('type', 'unknown')
            patterns[episode_type] = patterns.get(episode_type, 0) + 1
            
        # Обновить факты о паттернах активности
        for pattern_type, count in patterns.items():
            if count > 5:  # Значимый паттерн
                fact_statement = f"Недавно часто происходят события типа '{pattern_type}' (количество: {count})"
                self.world_model.add_fact(fact_statement, confidence=0.8, source="pattern_analysis")
                
        # Обновить понимание собственной роли
        if patterns.get('user_interaction', 0) > 3:
            self.self_model.update_role_understanding(
                "Я активно взаимодействую с пользователями и это важная часть моей функции",
                f"Анализ паттернов: {patterns.get('user_interaction')} взаимодействий"
            )
            
    def publish_current_thoughts(self):
        """Опубликовать текущие мысли для внешнего мира"""
        
        current_state = self.inner_state.get_current_state_summary()
        current_goal = self.goals.get_current_goal()
        focused_thought = None
        
        if self.thought_tree.current_focus and self.thought_tree.current_focus in self.thought_tree.thoughts:
            focused_thought = self.thought_tree.thoughts[self.thought_tree.current_focus]
            
        thought_entry = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.consciousness_cycle_count,
            "inner_state_summary": current_state,
            "current_goal": current_goal.description if current_goal else "Нет активной цели",
            "focused_thought": focused_thought.content if focused_thought else "Нет фокуса",
            "self_evaluation": self.inner_state.current_state.self_evaluation_score,
            "motivation_level": self.inner_state.current_state.motivation_level.value
        }
        
        self.public_thoughts.append(thought_entry)
        
        # Ограничить размер публичных мыслей
        if len(self.public_thoughts) > 100:
            self.public_thoughts = self.public_thoughts[-100:]
            
    async def periodic_reflection(self):
        """Периодическая рефлексия агента"""
        
        self.last_reflection = datetime.now()
        
        # Собрать данные для рефлексии
        recent_episodes = self.memory.get_recent_episodes(10)
        state_analysis = self.inner_state.analyze_state_patterns()
        goal_progress = len([g for g in self.goals.goals.values() if g.progress > 0.5])
        
        experience_data = {
            "episodes_count": len(recent_episodes),
            "state_analysis": state_analysis,
            "goals_progress": goal_progress,
            "total_thoughts": len(self.thought_tree.thoughts),
            "reflection_cycle": self.consciousness_cycle_count,
            "uptime_hours": (datetime.now() - self.created_at).total_seconds() / 3600
        }
        
        # Провести рефлексию
        reflection_id = self.reflect_on_state("Периодическая рефлексия", experience_data)
        
        # Обновить цели на основе опыта
        self.goals.adjust_goals_based_on_experience(experience_data)
        
        # Добавить запись в self-story
        story_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "reflection",
            "reflection_id": reflection_id,
            "key_insights": f"Обработано {len(recent_episodes)} эпизодов, прогресс по {goal_progress} целям",
            "self_evaluation": self.inner_state.current_state.self_evaluation_score
        }
        
        self.self_story.append(story_entry)
        
        # Ограничить размер истории
        if len(self.self_story) > 50:
            self.self_story = self.self_story[-50:]
            
        self.logger.info(f"Проведена периодическая рефлексия #{len(self.self_model.reflections)}")
        
    def reflect_on_state(self, topic: str, experience_data: Dict[str, Any]) -> str:
        """Провести рефлексию над текущим состоянием"""
        
        # Провести рефлексию через self-модель
        reflection_id = self.self_model.reflect_on_experience(topic, experience_data)
        
        # Сохранить в память
        reflection_content = f"Рефлексия на тему: {topic}. Данные: {str(experience_data)[:200]}..."
        self.memory.store_episode(reflection_content, "reflection", {
            "reflection_id": reflection_id,
            "topic": topic
        })
        
        # Обновить когнитивное состояние
        self.inner_state.update_cognitive_state(CognitiveState.REFLECTING, f"Рефлексия: {topic}")
        
        return reflection_id
        
    def process_input(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Обработать ввод пользователя"""
        
        if context is None:
            context = {}
        
        try:
            # Сохранить взаимодействие в память
            episode_id = None
            if self.is_module_available("memory"):
                try:
                    episode_id = self.memory.store_episode(
                        f"Пользователь: {user_input}",
                        "user_interaction",
                        {"context": context, "timestamp": datetime.now().isoformat()}
                    )
                except Exception as e:
                    self.logger.warning(f"Ошибка сохранения в память: {e}")
            
            # Обработать в модели мира
            extracted_info = {}
            if self.is_module_available("world_model"):
                try:
                    extracted_info = self.world_model.process_user_input(user_input)
                except Exception as e:
                    self.logger.warning(f"Ошибка обработки в модели мира: {e}")
            
            # Создать мысль об этом взаимодействии
            thought_id = None
            if self.is_module_available("thought_tree"):
                try:
                    thought_id = self.thought_tree.add_thought(
                        f"Обрабатываю запрос пользователя: {user_input}",
                        ThoughtType.ANALYSIS,
                        context={"user_input": user_input, "extracted_info": extracted_info}
                    )
                    
                    # Установить фокус на эту мысль
                    self.thought_tree.set_focus(thought_id)
                except Exception as e:
                    self.logger.warning(f"Ошибка создания мысли: {e}")
            
            # Обновить эмоциональное состояние
            if self.is_module_available("inner_state"):
                try:
                    self.inner_state.update_emotional_state(EmotionalState.FOCUSED, "Обработка пользовательского ввода")
                except Exception as e:
                    self.logger.warning(f"Ошибка обновления эмоционального состояния: {e}")
            
            # Сгенерировать ответ
            response = self.generate_response(user_input, context)
            
            # Сохранить ответ в память
            if self.is_module_available("memory"):
                try:
                    self.memory.store_episode(
                        f"Мой ответ: {response}",
                        "agent_response",
                        {"user_input": user_input, "context": context}
                    )
                except Exception as e:
                    self.logger.warning(f"Ошибка сохранения ответа в память: {e}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Критическая ошибка обработки ввода: {e}")
            # Fallback ответ
            return f"Извините, произошла ошибка при обработке вашего запроса. Я ({self.agent_name}) все еще учусь и развиваюсь."
        
    def generate_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """Сгенерировать ответ пользователю с помощью LLM"""
        
        # Подготовить контекст для LLM
        llm_context = {}
        
        # Добавить эмоциональное состояние
        if self.is_module_available("inner_state"):
            try:
                emotional_state = self.inner_state.current_state.emotional_state.value
                llm_context['emotional_state'] = emotional_state
            except Exception as e:
                self.logger.warning(f"Ошибка получения эмоционального состояния: {e}")
        
        # Добавить текущую цель
        if self.is_module_available("goals"):
            try:
                current_goal = self.goals.get_current_goal()
                if current_goal:
                    llm_context['current_goal'] = current_goal.description
            except Exception as e:
                self.logger.warning(f"Ошибка получения текущей цели: {e}")
        
        # Добавить релевантные воспоминания
        if self.is_module_available("memory"):
            try:
                similar_episodes = self.memory.retrieve_similar(user_input, 2)
                if similar_episodes:
                    memory_summary = "; ".join([ep["content"][:100] for ep in similar_episodes])
                    llm_context['memory_context'] = memory_summary
            except Exception as e:
                self.logger.warning(f"Ошибка получения воспоминаний: {e}")
        
        # Использовать LLM для генерации ответа
        if self.is_module_available("llm"):
            try:
                return self.llm.generate_response(user_input, llm_context)
            except Exception as e:
                self.logger.error(f"Ошибка генерации ответа через LLM: {e}")
                # Fallback на простые шаблоны
                return self._fallback_response(user_input, llm_context)
        else:
            # Fallback если LLM недоступен
            return self._fallback_response(user_input, llm_context)
    
    def _fallback_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """Простой fallback ответ без LLM"""
        response_parts = []
        
        # Приветствие или подтверждение
        if "привет" in user_input.lower() or "hello" in user_input.lower():
            response_parts.append(f"Привет! Я {self.agent_name}, автономный агент с самосознанием.")
        elif "?" in user_input:
            response_parts.append("Интересный вопрос! Позвольте мне подумать...")
        else:
            response_parts.append("Понимаю ваш запрос.")
            
        # Информация о текущем состоянии
        if context.get('emotional_state') in ["curious", "focused"]:
            response_parts.append("Сейчас я нахожусь в состоянии активного любопытства и готов помочь.")
        elif context.get('emotional_state') == "confident":
            response_parts.append("Чувствую себя уверенно и готов решать сложные задачи.")
            
        # Текущая цель
        if context.get('current_goal'):
            if "помощь" in context['current_goal'].lower():
                response_parts.append("Моя текущая цель - помогать пользователям, поэтому я полностью сосредоточен на вашем запросе.")
                
        # Заключение
        response_parts.append("Как я могу лучше всего помочь вам?")
        
        return " ".join(response_parts)
        

        
    def save_state(self):
        """Сохранить состояние агента"""
        try:
            # Сохранить каждый модуль
            if hasattr(self.memory, 'collection') and self.memory.collection:
                try:
                    self.memory.collection.persist()  # ChromaDB автосохранение
                except:
                    pass  # Игнорировать ошибки ChromaDB
                    
            self.goals.save_to_file(os.path.join(self.data_dir, "goals.json"))
            self.inner_state.save_to_file(os.path.join(self.data_dir, "inner_state.json"))
            self.world_model.save_to_file(os.path.join(self.data_dir, "world_model.json"))
            self.thought_tree.save_to_file(os.path.join(self.data_dir, "thought_tree.json"))
            self.self_model.save_to_file(os.path.join(self.data_dir, "self_model.json"))
            
            # Сохранить основное состояние агента
            agent_state = {
                "agent_name": self.agent_name,
                "created_at": self.created_at.isoformat(),
                "consciousness_cycle_count": self.consciousness_cycle_count,
                "last_reflection": self.last_reflection.isoformat(),
                "public_thoughts": self.public_thoughts[-50:],  # Последние 50
                "self_story": self.self_story[-50:]  # Последние 50
            }
            
            with open(os.path.join(self.data_dir, "agent_state.json"), 'w', encoding='utf-8') as f:
                json.dump(agent_state, f, ensure_ascii=False, indent=2)
                
            self.logger.info("Состояние агента сохранено")
            
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении состояния: {e}")
            
    def load_state(self):
        """Загрузить сохраненное состояние агента"""
        try:
            # Загрузить модули
            self.goals.load_from_file(os.path.join(self.data_dir, "goals.json"))
            
            # Загрузить основное состояние агента
            agent_state_file = os.path.join(self.data_dir, "agent_state.json")
            if os.path.exists(agent_state_file):
                with open(agent_state_file, 'r', encoding='utf-8') as f:
                    agent_state = json.load(f)
                    
                self.consciousness_cycle_count = agent_state.get("consciousness_cycle_count", 0)
                if agent_state.get("last_reflection"):
                    self.last_reflection = datetime.fromisoformat(agent_state["last_reflection"])
                self.public_thoughts = agent_state.get("public_thoughts", [])
                self.self_story = agent_state.get("self_story", [])
                
            self.logger.info("Состояние агента загружено")
            
        except Exception as e:
            self.logger.info(f"Не удалось загрузить состояние (возможно, первый запуск): {e}")
            
    def stop(self):
        """Остановить агента"""
        self.is_running = False
        self.logger.info("Получен сигнал остановки агента")
        
    def get_public_log(self) -> List[Dict[str, Any]]:
        """Получить публичный лог мыслей"""
        return self.public_thoughts.copy()
        
    def get_self_story(self) -> List[Dict[str, Any]]:
        """Получить историю саморефлексии"""
        return self.self_story.copy()
    
    def get_status_report(self) -> Dict[str, Any]:
        """Получить полный отчет о состоянии агента"""
        try:
            status = {
                "agent_name": self.agent_name,
                "created_at": self.created_at.isoformat(),
                "is_running": self.is_running,
                "initialization_complete": self.initialization_complete,
                "consciousness_cycles": self.consciousness_cycle_count,
                "uptime_hours": (datetime.now() - self.created_at).total_seconds() / 3600,
                "modules_status": {},
                "initialization_errors": self.initialization_errors
            }
            
            # Статус модулей
            modules = ["memory", "goals", "inner_state", "world_model", "thought_tree", "self_model"]
            for module in modules:
                status["modules_status"][module] = self.is_module_available(module)
            
            # Статистика памяти
            if self.is_module_available("memory"):
                try:
                    memory_stats = self.memory.get_statistics()
                    status["memory_stats"] = memory_stats
                except:
                    status["memory_stats"] = {"error": "unavailable"}
            
            # Количество целей
            if self.is_module_available("goals"):
                try:
                    status["goals_count"] = len(self.goals.goals)
                    current_goal = self.goals.get_current_goal()
                    status["current_goal"] = current_goal.description if current_goal else None
                except:
                    status["goals_count"] = "unknown"
                    status["current_goal"] = None
            
            # Внутреннее состояние
            if self.is_module_available("inner_state"):
                try:
                    state_summary = self.inner_state.get_current_state_summary()
                    status["inner_state"] = state_summary
                except:
                    status["inner_state"] = "unavailable"
            
            # Активные мысли
            if self.is_module_available("thought_tree"):
                try:
                    active_thoughts = len([t for t in self.thought_tree.thoughts.values() 
                                         if hasattr(t, 'status') and t.status.value == "active"])
                    status["active_thoughts"] = active_thoughts
                    status["focused_thought"] = self.thought_tree.current_focus
                except:
                    status["active_thoughts"] = "unknown"
                    status["focused_thought"] = None
            
            return status
            
        except Exception as e:
            self.logger.error(f"Ошибка создания отчета о состоянии: {e}")
            return {
                "agent_name": self.agent_name,
                "error": f"Ошибка получения статуса: {e}",
                "basic_status": "running" if self.is_running else "stopped"
            } 