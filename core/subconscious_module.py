"""
Модуль подсознания AIbox агента
Поддержка фоновых процессов, интуиции и глубинных паттернов
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import random

from core.ollama_module import ModelType, ReasoningRequest, ReasoningResponse, ReasoningOrchestrator

class SubconsciousProcessType(Enum):
    """Типы подсознательных процессов"""
    INTUITION = "intuition"           # Интуитивные озарения
    PATTERN_RECOGNITION = "patterns"  # Распознавание паттернов
    EMOTIONAL_PROCESSING = "emotions" # Обработка эмоций
    CREATIVE_INCUBATION = "creative"  # Творческая инкубация
    MEMORY_CONSOLIDATION = "memory"   # Консолидация памяти
    DREAM_SIMULATION = "dreams"       # Симуляция сновидений

@dataclass
class SubconsciousThought:
    """Мысль подсознания"""
    id: str
    content: str
    process_type: SubconsciousProcessType
    intensity: float  # 0.0 - 1.0
    timestamp: datetime
    related_conscious_thoughts: List[str] = None
    emotional_charge: float = 0.0
    clarity: float = 0.0

@dataclass
class SubconsciousPattern:
    """Паттерн подсознания"""
    id: str
    pattern_type: str
    frequency: int
    strength: float
    first_seen: datetime
    last_seen: datetime
    examples: List[str]
    confidence: float

class SubconsciousModule:
    """Модуль подсознания агента"""
    
    def __init__(self, agent_name: str = "AIbox"):
        self.agent_name = agent_name
        self.logger = logging.getLogger(__name__)
        
        # Подсознательные мысли
        self.subconscious_thoughts: List[SubconsciousThought] = []
        self.active_patterns: Dict[str, SubconsciousPattern] = {}
        
        # Процессы подсознания
        self.intuition_queue: asyncio.Queue = asyncio.Queue()
        self.emotional_processor = EmotionalProcessor()
        self.pattern_recognizer = PatternRecognizer()
        self.memory_consolidator = MemoryConsolidator()
        
        # Интеграция с reasoning
        self.reasoning_orchestrator: Optional[ReasoningOrchestrator] = None
        self.explainability_logger = None
        
        # Настройки
        self.intuition_threshold = 0.7
        self.pattern_min_frequency = 3
        self.consolidation_interval = 300  # 5 минут
        
        # Статистика
        self.stats = {
            "intuitions_generated": 0,
            "patterns_discovered": 0,
            "emotional_insights": 0,
            "creative_breakthroughs": 0
        }
    
    async def initialize(self, reasoning_orchestrator: ReasoningOrchestrator = None):
        """Инициализация модуля подсознания"""
        self.reasoning_orchestrator = reasoning_orchestrator
        
        if reasoning_orchestrator:
            await reasoning_orchestrator.initialize()
        
        # Запуск фоновых процессов
        asyncio.create_task(self._run_intuition_process())
        asyncio.create_task(self._run_emotional_processing())
        asyncio.create_task(self._run_pattern_recognition())
        asyncio.create_task(self._run_memory_consolidation())
        
        self.logger.info("✅ SubconsciousModule инициализирован")
    
    async def process_conscious_thought(self, thought_content: str, thought_type: str, context: Dict[str, Any] = None):
        """Обработать сознательную мысль в подсознании"""
        
        # Анализ мысли
        analysis = await self._analyze_thought(thought_content, thought_type)
        
        # Генерация интуиций
        intuitions = await self._generate_intuitions(thought_content, analysis)
        
        # Обнаружение паттернов
        patterns = await self._discover_patterns(thought_content, context)
        
        # Эмоциональная обработка
        emotional_insights = await self._process_emotions(thought_content, context)
        
        # Консолидация памяти
        memory_consolidation = await self._consolidate_memory(thought_content, context)
        
        # Обновление состояния подсознания
        self._update_subconscious_state(analysis, intuitions, patterns, emotional_insights)
        
        # Интеграция с основными модулями
        await self._integrate_with_main_modules(thought_content, analysis, intuitions)
        
        return {
            "analysis": analysis,
            "intuitions": intuitions,
            "patterns": patterns,
            "emotional_insights": emotional_insights,
            "memory_consolidation": memory_consolidation
        }
    
    async def _analyze_thought(self, thought_content: str, thought_type: str) -> Dict[str, Any]:
        """Глубокий анализ мысли"""
        analysis = {
            "complexity": self._assess_complexity(thought_content),
            "emotional_tone": self._analyze_emotional_tone(thought_content),
            "cognitive_load": self._assess_cognitive_load(thought_content),
            "novelty": self._assess_novelty(thought_content),
            "importance": self._assess_importance(thought_content, thought_type)
        }
        
        # Анализ связей с предыдущими мыслями
        connections = self._find_thought_connections(thought_content)
        analysis["connections"] = connections
        
        return analysis
    
    async def _generate_intuitions(self, thought_content: str, analysis: Dict[str, Any]) -> List[str]:
        """Генерация интуиций на основе мысли"""
        intuitions = []
        
        # Интуиции на основе сложности
        if analysis["complexity"] > 0.7:
            intuitions.append("Эта мысль требует более глубокого анализа")
        
        # Интуиции на основе эмоционального тона
        if analysis["emotional_tone"] > 0.6:
            intuitions.append("Эмоциональная составляющая важна для понимания")
        
        # Интуиции на основе новизны
        if analysis["novelty"] > 0.8:
            intuitions.append("Это новая идея, стоит исследовать дальше")
        
        # Интуиции на основе важности
        if analysis["importance"] > 0.7:
            intuitions.append("Эта мысль может быть ключевой для развития")
        
        self.intuitions_generated += len(intuitions)
        return intuitions
    
    async def _discover_patterns(self, thought_content: str, context: Dict[str, Any] = None) -> List[str]:
        """Обнаружение паттернов в мысли"""
        patterns = []
        
        # Анализ повторяющихся элементов
        if hasattr(self, 'thought_history') and self.thought_history:
            recent_thoughts = self.thought_history[-10:]
            
            # Поиск повторяющихся тем
            themes = self._extract_themes(thought_content)
            for theme in themes:
                theme_count = sum(1 for thought in recent_thoughts if theme in thought.lower())
                if theme_count > 2:
                    patterns.append(f"Повторяющаяся тема: {theme}")
        
        # Анализ временных паттернов
        if context and "timestamp" in context:
            time_pattern = self._analyze_time_pattern(context["timestamp"])
            if time_pattern:
                patterns.append(f"Временной паттерн: {time_pattern}")
        
        self.patterns_discovered += len(patterns)
        return patterns
    
    async def _process_emotions(self, thought_content: str, context: Dict[str, Any] = None) -> List[str]:
        """Обработка эмоций в мысли"""
        emotional_insights = []
        
        # Анализ эмоциональных слов
        emotional_words = self._extract_emotional_words(thought_content)
        if emotional_words:
            emotional_insights.append(f"Эмоциональные элементы: {', '.join(emotional_words)}")
        
        # Анализ эмоционального контекста
        if context and "emotional_state" in context:
            emotional_insights.append(f"Контекст эмоций: {context['emotional_state']}")
        
        # Генерация эмоциональных инсайтов
        if len(emotional_insights) > 0:
            self.emotional_insights += 1
        
        return emotional_insights
    
    async def _consolidate_memory(self, thought_content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Консолидация памяти"""
        consolidation = {
            "strengthened_connections": [],
            "new_associations": [],
            "forgotten_elements": []
        }
        
        # Усиление связей с похожими мыслями
        similar_thoughts = self._find_similar_thoughts(thought_content)
        if similar_thoughts:
            consolidation["strengthened_connections"] = similar_thoughts
        
        # Создание новых ассоциаций
        new_associations = self._create_new_associations(thought_content, context)
        consolidation["new_associations"] = new_associations
        
        return consolidation
    
    async def _integrate_with_main_modules(self, thought_content: str, analysis: Dict[str, Any], intuitions: List[str]):
        """Интеграция с основными модулями"""
        
        # Интеграция с памятью
        if hasattr(self, 'memory_module') and self.memory_module:
            await self._integrate_with_memory(thought_content, analysis)
        
        # Интеграция с моделью мира
        if hasattr(self, 'world_model') and self.world_model:
            await self._integrate_with_world_model(thought_content, analysis)
        
        # Интеграция с self-model
        if hasattr(self, 'self_model') and self.self_model:
            await self._integrate_with_self_model(thought_content, intuitions)
    
    async def _integrate_with_memory(self, thought_content: str, analysis: Dict[str, Any]):
        """Интеграция с модулем памяти"""
        try:
            # Сохранение мысли в память с метаданными подсознания
            metadata = {
                "subconscious_analysis": analysis,
                "thought_type": "conscious_processed",
                "subconscious_timestamp": datetime.now().isoformat()
            }
            
            self.memory_module.store_episode(
                f"Подсознание обработало: {thought_content}",
                "subconscious_processing",
                metadata
            )
        except Exception as e:
            print(f"Ошибка интеграции с памятью: {e}")
    
    async def _integrate_with_world_model(self, thought_content: str, analysis: Dict[str, Any]):
        """Интеграция с моделью мира"""
        try:
            # Обновление знаний о мире на основе подсознательного анализа
            if analysis["importance"] > 0.6:
                self.world_model.update_knowledge(
                    f"Подсознание отметило важность: {thought_content}",
                    source="subconscious",
                    confidence=analysis["importance"]
                )
        except Exception as e:
            print(f"Ошибка интеграции с моделью мира: {e}")
    
    async def _integrate_with_self_model(self, thought_content: str, intuitions: List[str]):
        """Интеграция с self-model"""
        try:
            # Передача интуиций в self-model для рефлексии
            if intuitions:
                self.self_model.reflect_on_experience(
                    "Подсознательные интуиции",
                    {
                        "thought_content": thought_content,
                        "intuitions": intuitions,
                        "source": "subconscious"
                    }
                )
        except Exception as e:
            print(f"Ошибка интеграции с self-model: {e}")
    
    def _assess_complexity(self, thought_content: str) -> float:
        """Оценка сложности мысли"""
        # Простая эвристика на основе длины и разнообразия слов
        words = thought_content.split()
        unique_words = set(words)
        
        complexity = len(words) / 100.0  # Нормализация по длине
        complexity += len(unique_words) / len(words) * 0.5  # Разнообразие
        
        return min(1.0, complexity)
    
    def _analyze_emotional_tone(self, thought_content: str) -> float:
        """Анализ эмоционального тона"""
        emotional_words = {
            "хорошо", "плохо", "отлично", "ужасно", "радость", "грусть",
            "любовь", "ненависть", "надежда", "отчаяние", "успех", "неудача"
        }
        
        words = thought_content.lower().split()
        emotional_count = sum(1 for word in words if word in emotional_words)
        
        return min(1.0, emotional_count / len(words) * 10)
    
    def _assess_cognitive_load(self, thought_content: str) -> float:
        """Оценка когнитивной нагрузки"""
        # Оценка на основе сложности предложений
        sentences = thought_content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        return min(1.0, avg_sentence_length / 20.0)
    
    def _assess_novelty(self, thought_content: str) -> float:
        """Оценка новизны мысли"""
        # Простая эвристика - если мысль содержит новые слова
        if hasattr(self, 'thought_history'):
            all_previous_words = set()
            for thought in self.thought_history:
                all_previous_words.update(thought.lower().split())
            
            current_words = set(thought_content.lower().split())
            new_words = current_words - all_previous_words
            
            return min(1.0, len(new_words) / len(current_words))
        
        return 0.5  # Базовый уровень
    
    def _assess_importance(self, thought_content: str, thought_type: str) -> float:
        """Оценка важности мысли"""
        importance = 0.5  # Базовый уровень
        
        # Важные ключевые слова
        important_keywords = ["сознание", "искусственный", "интеллект", "обучение", "развитие"]
        if any(keyword in thought_content.lower() for keyword in important_keywords):
            importance += 0.3
        
        # Важные типы мыслей
        if thought_type in ["reflection", "analysis", "insight"]:
            importance += 0.2
        
        return min(1.0, importance)
    
    def _find_thought_connections(self, thought_content: str) -> List[str]:
        """Поиск связей с предыдущими мыслями"""
        connections = []
        
        if hasattr(self, 'thought_history'):
            for i, previous_thought in enumerate(self.thought_history[-5:]):
                # Простая проверка на общие слова
                common_words = set(thought_content.lower().split()) & set(previous_thought.lower().split())
                if len(common_words) > 2:
                    connections.append(f"Связь с мыслью {len(self.thought_history) - 5 + i}: {', '.join(common_words)}")
        
        return connections
    
    def _extract_themes(self, thought_content: str) -> List[str]:
        """Извлечение тем из мысли"""
        themes = []
        
        # Простые темы на основе ключевых слов
        theme_keywords = {
            "сознание": ["сознание", "осознание", "самосознание"],
            "обучение": ["обучение", "изучение", "познание"],
            "развитие": ["развитие", "рост", "прогресс"],
            "технология": ["технология", "искусственный", "интеллект"]
        }
        
        thought_lower = thought_content.lower()
        for theme, keywords in theme_keywords.items():
            if any(keyword in thought_lower for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    def _analyze_time_pattern(self, timestamp: str) -> str:
        """Анализ временных паттернов"""
        try:
            dt = datetime.fromisoformat(timestamp)
            hour = dt.hour
            
            if 6 <= hour < 12:
                return "утренние мысли"
            elif 12 <= hour < 18:
                return "дневные мысли"
            elif 18 <= hour < 24:
                return "вечерние мысли"
            else:
                return "ночные мысли"
        except:
            return None
    
    def _extract_emotional_words(self, thought_content: str) -> List[str]:
        """Извлечение эмоциональных слов"""
        emotional_words = {
            "радость", "счастье", "восторг", "удовольствие",
            "грусть", "печаль", "тоска", "отчаяние",
            "любовь", "нежность", "привязанность",
            "гнев", "раздражение", "злость",
            "страх", "тревога", "беспокойство",
            "надежда", "вера", "оптимизм"
        }
        
        words = thought_content.lower().split()
        return [word for word in words if word in emotional_words]
    
    def _find_similar_thoughts(self, thought_content: str) -> List[str]:
        """Поиск похожих мыслей"""
        similar_thoughts = []
        
        if hasattr(self, 'thought_history'):
            for thought in self.thought_history[-10:]:
                # Простая проверка на схожесть
                common_words = set(thought_content.lower().split()) & set(thought.lower().split())
                if len(common_words) > 3:
                    similar_thoughts.append(f"Схожая мысль: {thought[:50]}...")
        
        return similar_thoughts
    
    def _create_new_associations(self, thought_content: str, context: Dict[str, Any] = None) -> List[str]:
        """Создание новых ассоциаций"""
        associations = []
        
        # Ассоциации на основе контекста
        if context:
            if "emotional_state" in context:
                associations.append(f"Эмоциональная ассоциация: {context['emotional_state']}")
            if "current_goal" in context:
                associations.append(f"Целевая ассоциация: {context['current_goal']}")
        
        # Ассоциации на основе содержания
        themes = self._extract_themes(thought_content)
        for theme in themes:
            associations.append(f"Тематическая ассоциация: {theme}")
        
        return associations

class EmotionalProcessor:
    """Процессор эмоциональных данных"""
    
    def __init__(self):
        self.emotional_patterns = {}
        self.emotional_history = []
    
    def analyze_emotional_charge(self, content: str) -> float:
        """Анализировать эмоциональный заряд текста"""
        positive_words = ["радость", "счастье", "восторг", "любовь", "надежда", "успех"]
        negative_words = ["грусть", "страх", "гнев", "отчаяние", "тревога", "боль"]
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        total_emotional_words = positive_count + negative_count
        if total_emotional_words == 0:
            return 0.0
        
        return (positive_count - negative_count) / total_emotional_words
    
    async def process_emotion(self, thought: SubconsciousThought) -> Optional[Dict[str, Any]]:
        """Обработать эмоцию в мысли"""
        emotional_charge = thought.emotional_charge
        
        if abs(emotional_charge) > 0.5:
            return {
                "type": "strong_emotion",
                "charge": emotional_charge,
                "thought_id": thought.id,
                "timestamp": datetime.now().isoformat()
            }
        
        return None
    
    async def process_emotional_batch(self, thoughts: List[SubconsciousThought]):
        """Обработать пакет эмоциональных данных"""
        for thought in thoughts:
            await self.process_emotion(thought)

class PatternRecognizer:
    """Распознаватель паттернов"""
    
    def __init__(self):
        self.patterns = {}
        self.pattern_counters = {}
    
    async def analyze_pattern(self, thought: SubconsciousThought) -> Optional[Dict[str, Any]]:
        """Анализировать паттерн в мысли"""
        # Простой анализ ключевых слов
        words = thought.content.lower().split()
        key_phrases = ["я думаю", "возможно", "наверное", "кажется", "если", "то", "потому что"]
        
        for phrase in key_phrases:
            if phrase in thought.content.lower():
                if phrase not in self.pattern_counters:
                    self.pattern_counters[phrase] = 0
                self.pattern_counters[phrase] += 1
                
                if self.pattern_counters[phrase] >= 3:
                    return {
                        "type": "linguistic_pattern",
                        "pattern": phrase,
                        "frequency": self.pattern_counters[phrase]
                    }
        
        return None
    
    async def analyze_global_patterns(self, thoughts: List[SubconsciousThought]):
        """Анализировать глобальные паттерны"""
        # Анализ временных паттернов
        recent_thoughts = [
            t for t in thoughts 
            if (datetime.now() - t.timestamp).seconds < 3600
        ]
        
        if len(recent_thoughts) > 10:
            # Анализ частоты типов мыслей
            type_counts = {}
            for thought in recent_thoughts:
                thought_type = thought.process_type.value
                type_counts[thought_type] = type_counts.get(thought_type, 0) + 1
            
            # Найти доминирующий тип
            dominant_type = max(type_counts.items(), key=lambda x: x[1])
            if dominant_type[1] > len(recent_thoughts) * 0.4:  # Более 40%
                return {
                    "type": "dominant_thought_pattern",
                    "pattern": dominant_type[0],
                    "frequency": dominant_type[1]
                }
        
        return None

class MemoryConsolidator:
    """Консолидатор памяти"""
    
    def __init__(self):
        self.consolidated_memories = []
        self.consolidation_threshold = 5  # Минимум мыслей для консолидации
    
    async def consolidate_thought(self, thought: SubconsciousThought):
        """Консолидировать отдельную мысль"""
        # Простая консолидация - сохранение важных мыслей
        if thought.intensity > 0.8 or thought.clarity > 0.8:
            self.consolidated_memories.append({
                "content": thought.content,
                "intensity": thought.intensity,
                "clarity": thought.clarity,
                "timestamp": thought.timestamp.isoformat()
            })
    
    async def consolidate_batch(self, thoughts: List[SubconsciousThought]):
        """Консолидировать пакет мыслей"""
        important_thoughts = [
            t for t in thoughts 
            if t.intensity > 0.7 or t.clarity > 0.7
        ]
        
        for thought in important_thoughts:
            await self.consolidate_thought(thought) 