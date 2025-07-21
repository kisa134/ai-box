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
        
        # Создать подсознательную мысль
        subconscious_thought = SubconsciousThought(
            id=f"sub_{int(time.time() * 1000)}",
            content=thought_content,
            process_type=self._map_conscious_to_subconscious(thought_type),
            intensity=self._calculate_intensity(thought_content, context),
            timestamp=datetime.now(),
            emotional_charge=self.emotional_processor.analyze_emotional_charge(thought_content),
            clarity=self._calculate_clarity(thought_content)
        )
        
        self.subconscious_thoughts.append(subconscious_thought)
        
        # Запустить обработку
        await self._process_subconscious_thought(subconscious_thought)
        
        # Проверить на интуитивные озарения
        if subconscious_thought.intensity > self.intuition_threshold:
            await self._trigger_intuition(subconscious_thought)
    
    async def _process_subconscious_thought(self, thought: SubconsciousThought):
        """Обработать подсознательную мысль"""
        
        # Эмоциональная обработка
        emotional_insight = await self.emotional_processor.process_emotion(thought)
        if emotional_insight:
            self.stats["emotional_insights"] += 1
        
        # Распознавание паттернов
        pattern_insight = await self.pattern_recognizer.analyze_pattern(thought)
        if pattern_insight:
            self.stats["patterns_discovered"] += 1
        
        # Консолидация памяти
        await self.memory_consolidator.consolidate_thought(thought)
    
    async def _trigger_intuition(self, trigger_thought: SubconsciousThought):
        """Запустить процесс интуитивного озарения"""
        
        if not self.reasoning_orchestrator:
            return
        
        # Создать запрос на интуитивное мышление
        intuition_request = ReasoningRequest(
            prompt=f"Интуитивное озарение на основе мысли: {trigger_thought.content}",
            model_type=ModelType.SUBCONSCIOUS,
            context={
                "trigger_thought": trigger_thought.content,
                "intensity": trigger_thought.intensity,
                "emotional_charge": trigger_thought.emotional_charge,
                "process_type": trigger_thought.process_type.value
            },
            priority=8,
            require_explanation=True
        )
        
        # Отправить запрос
        request_id = await self.reasoning_orchestrator.submit_reasoning_request(intuition_request)
        
        # Получить ответ
        response = await self.reasoning_orchestrator.get_reasoning_response(request_id)
        
        if response and response.content:
            # Создать интуитивное озарение
            intuition = SubconsciousThought(
                id=f"intuition_{int(time.time() * 1000)}",
                content=response.content,
                process_type=SubconsciousProcessType.INTUITION,
                intensity=response.confidence,
                timestamp=datetime.now(),
                related_conscious_thoughts=[trigger_thought.id],
                emotional_charge=trigger_thought.emotional_charge,
                clarity=response.confidence
            )
            
            self.subconscious_thoughts.append(intuition)
            self.stats["intuitions_generated"] += 1
            
            # Залогировать интуицию
            if self.explainability_logger:
                self.explainability_logger.log_reasoning_request(intuition_request, response)
    
    async def _run_intuition_process(self):
        """Фоновый процесс генерации интуиций"""
        while True:
            try:
                # Проверить накопленные мысли на интуитивные связи
                recent_thoughts = [
                    t for t in self.subconscious_thoughts 
                    if (datetime.now() - t.timestamp).seconds < 3600  # Последний час
                ]
                
                if len(recent_thoughts) >= 3:
                    # Искать связи между мыслями
                    connections = self._find_thought_connections(recent_thoughts)
                    
                    for connection in connections:
                        if connection["strength"] > 0.8:
                            await self._generate_connection_intuition(connection)
                
                await asyncio.sleep(60)  # Проверка каждую минуту
                
            except Exception as e:
                self.logger.error(f"Ошибка в процессе интуиции: {e}")
                await asyncio.sleep(30)
    
    async def _run_emotional_processing(self):
        """Фоновый процесс обработки эмоций"""
        while True:
            try:
                # Обработать накопленные эмоциональные данные
                emotional_thoughts = [
                    t for t in self.subconscious_thoughts 
                    if t.process_type == SubconsciousProcessType.EMOTIONAL_PROCESSING
                ]
                
                if emotional_thoughts:
                    await self.emotional_processor.process_emotional_batch(emotional_thoughts)
                
                await asyncio.sleep(120)  # Каждые 2 минуты
                
            except Exception as e:
                self.logger.error(f"Ошибка в обработке эмоций: {e}")
                await asyncio.sleep(60)
    
    async def _run_pattern_recognition(self):
        """Фоновый процесс распознавания паттернов"""
        while True:
            try:
                # Анализировать паттерны в мыслях
                await self.pattern_recognizer.analyze_global_patterns(self.subconscious_thoughts)
                
                await asyncio.sleep(300)  # Каждые 5 минут
                
            except Exception as e:
                self.logger.error(f"Ошибка в распознавании паттернов: {e}")
                await asyncio.sleep(120)
    
    async def _run_memory_consolidation(self):
        """Фоновый процесс консолидации памяти"""
        while True:
            try:
                # Консолидировать накопленные мысли
                await self.memory_consolidator.consolidate_batch(self.subconscious_thoughts)
                
                await asyncio.sleep(self.consolidation_interval)
                
            except Exception as e:
                self.logger.error(f"Ошибка в консолидации памяти: {e}")
                await asyncio.sleep(300)
    
    def _map_conscious_to_subconscious(self, conscious_type: str) -> SubconsciousProcessType:
        """Сопоставить сознательную мысль с подсознательным процессом"""
        mapping = {
            "analysis": SubconsciousProcessType.PATTERN_RECOGNITION,
            "reflection": SubconsciousProcessType.EMOTIONAL_PROCESSING,
            "creative": SubconsciousProcessType.CREATIVE_INCUBATION,
            "memory": SubconsciousProcessType.MEMORY_CONSOLIDATION,
            "intuition": SubconsciousProcessType.INTUITION
        }
        return mapping.get(conscious_type, SubconsciousProcessType.EMOTIONAL_PROCESSING)
    
    def _calculate_intensity(self, content: str, context: Dict[str, Any] = None) -> float:
        """Рассчитать интенсивность мысли"""
        base_intensity = min(len(content) / 1000, 1.0)  # Базовая интенсивность по длине
        
        if context:
            if 'emotional_state' in context:
                emotional_multiplier = {
                    'excited': 1.3,
                    'focused': 1.2,
                    'curious': 1.1,
                    'calm': 0.9,
                    'tired': 0.7
                }.get(context['emotional_state'], 1.0)
                base_intensity *= emotional_multiplier
        
        return min(base_intensity, 1.0)
    
    def _calculate_clarity(self, content: str) -> float:
        """Рассчитать ясность мысли"""
        # Простая эвристика на основе структуры и длины
        if len(content) < 50:
            return 0.3
        elif len(content) > 500:
            return 0.9
        else:
            return 0.6
    
    def _find_thought_connections(self, thoughts: List[SubconsciousThought]) -> List[Dict[str, Any]]:
        """Найти связи между мыслями"""
        connections = []
        
        for i, thought1 in enumerate(thoughts):
            for j, thought2 in enumerate(thoughts[i+1:], i+1):
                similarity = self._calculate_thought_similarity(thought1, thought2)
                if similarity > 0.6:
                    connections.append({
                        "thought1": thought1.id,
                        "thought2": thought2.id,
                        "strength": similarity,
                        "type": "semantic_connection"
                    })
        
        return connections
    
    def _calculate_thought_similarity(self, thought1: SubconsciousThought, thought2: SubconsciousThought) -> float:
        """Рассчитать семантическое сходство мыслей"""
        # Простая эвристика на основе общих слов
        words1 = set(thought1.content.lower().split())
        words2 = set(thought2.content.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    async def _generate_connection_intuition(self, connection: Dict[str, Any]):
        """Генерировать интуицию на основе связи мыслей"""
        if not self.reasoning_orchestrator:
            return
        
        # Найти связанные мысли
        thought1 = next((t for t in self.subconscious_thoughts if t.id == connection["thought1"]), None)
        thought2 = next((t for t in self.subconscious_thoughts if t.id == connection["thought2"]), None)
        
        if not thought1 or not thought2:
            return
        
        intuition_request = ReasoningRequest(
            prompt=f"Интуитивное озарение на основе связи мыслей:\nМысль 1: {thought1.content}\nМысль 2: {thought2.content}",
            model_type=ModelType.SUBCONSCIOUS,
            context={
                "connection_strength": connection["strength"],
                "connection_type": connection["type"]
            },
            priority=7
        )
        
        request_id = await self.reasoning_orchestrator.submit_reasoning_request(intuition_request)
        response = await self.reasoning_orchestrator.get_reasoning_response(request_id)
        
        if response and response.content:
            self.stats["intuitions_generated"] += 1
    
    def get_subconscious_state(self) -> Dict[str, Any]:
        """Получить состояние подсознания"""
        recent_thoughts = [
            t for t in self.subconscious_thoughts 
            if (datetime.now() - t.timestamp).seconds < 3600
        ]
        
        return {
            "active_thoughts": len(recent_thoughts),
            "intuitions_generated": self.stats["intuitions_generated"],
            "patterns_discovered": self.stats["patterns_discovered"],
            "emotional_insights": self.stats["emotional_insights"],
            "creative_breakthroughs": self.stats["creative_breakthroughs"],
            "recent_intuitions": [
                {
                    "content": t.content[:100] + "...",
                    "intensity": t.intensity,
                    "timestamp": t.timestamp.isoformat()
                }
                for t in recent_thoughts if t.process_type == SubconsciousProcessType.INTUITION
            ],
            "active_patterns": len(self.active_patterns)
        }

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