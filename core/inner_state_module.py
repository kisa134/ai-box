from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import json
import uuid

class EmotionalState(Enum):
    NEUTRAL = "neutral"
    CURIOUS = "curious"
    FOCUSED = "focused"
    CONFUSED = "confused"
    SATISFIED = "satisfied"
    FRUSTRATED = "frustrated"
    CONFIDENT = "confident"
    UNCERTAIN = "uncertain"

class CognitiveState(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    LEARNING = "learning"
    PROBLEM_SOLVING = "problem_solving"
    REFLECTING = "reflecting"
    PLANNING = "planning"
    EXECUTING = "executing"

class MotivationLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

class InnerStateSnapshot:
    """Снимок внутреннего состояния агента в конкретный момент"""
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.emotional_state = EmotionalState.NEUTRAL
        self.cognitive_state = CognitiveState.IDLE
        self.motivation_level = MotivationLevel.MEDIUM
        self.attention_focus: Optional[str] = None
        self.energy_level = 1.0  # 0.0 to 1.0
        self.stress_level = 0.0  # 0.0 to 1.0
        self.confidence_level = 0.5  # 0.0 to 1.0
        self.learning_rate = 0.5  # 0.0 to 1.0
        self.context_awareness = 0.5  # 0.0 to 1.0
        self.self_evaluation_score = 0.5  # 0.0 to 1.0
        self.current_thoughts: List[str] = []
        self.active_concerns: List[str] = []
        self.metadata: Dict[str, Any] = {}
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "emotional_state": self.emotional_state.value,
            "cognitive_state": self.cognitive_state.value,
            "motivation_level": self.motivation_level.value,
            "attention_focus": self.attention_focus,
            "energy_level": self.energy_level,
            "stress_level": self.stress_level,
            "confidence_level": self.confidence_level,
            "learning_rate": self.learning_rate,
            "context_awareness": self.context_awareness,
            "self_evaluation_score": self.self_evaluation_score,
            "current_thoughts": self.current_thoughts,
            "active_concerns": self.active_concerns,
            "metadata": self.metadata
        }

class InnerStateModule:
    """
    Модуль внутренних состояний: самонаблюдение, самооценка эмоционального
    и когнитивного статуса, мотивация
    """
    
    def __init__(self):
        self.current_state = InnerStateSnapshot()
        self.state_history: List[InnerStateSnapshot] = []
        self.max_history_length = 1000
        self.state_transitions: Dict[str, int] = {}
        self.reflection_log: List[Dict[str, Any]] = []
        
    def update_emotional_state(self, 
                              new_state: EmotionalState,
                              reason: Optional[str] = None):
        """Обновить эмоциональное состояние"""
        old_state = self.current_state.emotional_state
        self.current_state.emotional_state = new_state
        
        # Записать переход состояния
        transition = f"{old_state.value} -> {new_state.value}"
        self.state_transitions[transition] = self.state_transitions.get(transition, 0) + 1
        
        if reason:
            self.current_state.metadata["emotional_change_reason"] = reason
            
        self._save_state_snapshot()
    
    def update_cognitive_state(self, 
                              new_state: CognitiveState,
                              context: Optional[str] = None):
        """Обновить когнитивное состояние"""
        old_state = self.current_state.cognitive_state
        self.current_state.cognitive_state = new_state
        
        if context:
            self.current_state.attention_focus = context
            
        transition = f"cognitive: {old_state.value} -> {new_state.value}"
        self.state_transitions[transition] = self.state_transitions.get(transition, 0) + 1
        
        self._save_state_snapshot()
    
    def update_motivation(self, 
                         level: MotivationLevel,
                         factors: Optional[List[str]] = None):
        """Обновить уровень мотивации"""
        self.current_state.motivation_level = level
        
        if factors:
            self.current_state.metadata["motivation_factors"] = factors
            
        self._save_state_snapshot()
    
    def adjust_energy_level(self, delta: float, reason: Optional[str] = None):
        """Изменить уровень энергии"""
        old_energy = self.current_state.energy_level
        self.current_state.energy_level = max(0.0, min(1.0, old_energy + delta))
        
        if reason:
            self.current_state.metadata["energy_change_reason"] = reason
            
        self._save_state_snapshot()
    
    def adjust_stress_level(self, delta: float, stressor: Optional[str] = None):
        """Изменить уровень стресса"""
        old_stress = self.current_state.stress_level
        self.current_state.stress_level = max(0.0, min(1.0, old_stress + delta))
        
        if stressor:
            if "stressors" not in self.current_state.metadata:
                self.current_state.metadata["stressors"] = []
            self.current_state.metadata["stressors"].append(stressor)
            
        self._save_state_snapshot()
    
    def update_confidence(self, new_level: float, context: Optional[str] = None):
        """Обновить уровень уверенности"""
        self.current_state.confidence_level = max(0.0, min(1.0, new_level))
        
        if context:
            self.current_state.metadata["confidence_context"] = context
            
        self._save_state_snapshot()
    
    def add_thought(self, thought: str):
        """Добавить текущую мысль"""
        self.current_state.current_thoughts.append(thought)
        
        # Ограничить количество мыслей
        if len(self.current_state.current_thoughts) > 10:
            self.current_state.current_thoughts = self.current_state.current_thoughts[-10:]
    
    def add_concern(self, concern: str):
        """Добавить активную проблему/озабоченность"""
        if concern not in self.current_state.active_concerns:
            self.current_state.active_concerns.append(concern)
    
    def resolve_concern(self, concern: str):
        """Разрешить проблему"""
        if concern in self.current_state.active_concerns:
            self.current_state.active_concerns.remove(concern)
    
    def self_evaluate(self, context: str = "") -> float:
        """Провести самооценку текущего состояния"""
        # Алгоритм самооценки на основе различных факторов
        factors = {
            "energy": self.current_state.energy_level,
            "confidence": self.current_state.confidence_level,
            "stress": 1.0 - self.current_state.stress_level,  # Инвертировать стресс
            "motivation": self.current_state.motivation_level.value / 4.0,
            "concerns": max(0.0, 1.0 - len(self.current_state.active_concerns) / 10.0)
        }
        
        # Взвешенная оценка
        weights = {
            "energy": 0.2,
            "confidence": 0.3,
            "stress": 0.2,
            "motivation": 0.2,
            "concerns": 0.1
        }
        
        evaluation_score = sum(factors[key] * weights[key] for key in factors)
        self.current_state.self_evaluation_score = evaluation_score
        
        # Записать рефлексию
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "evaluation_score": evaluation_score,
            "factors": factors,
            "state": self.current_state.to_dict()
        }
        
        self.reflection_log.append(reflection)
        
        # Ограничить лог рефлексии
        if len(self.reflection_log) > 100:
            self.reflection_log = self.reflection_log[-100:]
            
        return evaluation_score
    
    def analyze_state_patterns(self) -> Dict[str, Any]:
        """Анализ паттернов в состояниях"""
        if len(self.state_history) < 2:
            return {"message": "Недостаточно данных для анализа"}
            
        analysis = {
            "total_states": len(self.state_history),
            "state_transitions": self.state_transitions,
            "average_energy": sum(s.energy_level for s in self.state_history) / len(self.state_history),
            "average_stress": sum(s.stress_level for s in self.state_history) / len(self.state_history),
            "average_confidence": sum(s.confidence_level for s in self.state_history) / len(self.state_history),
            "most_common_emotional_state": self._get_most_common_state("emotional"),
            "most_common_cognitive_state": self._get_most_common_state("cognitive"),
            "concerns_frequency": self._analyze_concerns()
        }
        
        return analysis
    
    def _get_most_common_state(self, state_type: str) -> str:
        """Найти наиболее частое состояние"""
        if state_type == "emotional":
            states = [s.emotional_state.value for s in self.state_history]
        else:
            states = [s.cognitive_state.value for s in self.state_history]
            
        return max(set(states), key=states.count) if states else "unknown"
    
    def _analyze_concerns(self) -> Dict[str, int]:
        """Анализ частоты проблем"""
        concern_count = {}
        for state in self.state_history:
            for concern in state.active_concerns:
                concern_count[concern] = concern_count.get(concern, 0) + 1
        return concern_count
    
    def get_current_state_summary(self) -> str:
        """Получить текстовое описание текущего состояния"""
        state = self.current_state
        
        summary = f"""
Эмоциональное состояние: {state.emotional_state.value}
Когнитивное состояние: {state.cognitive_state.value}
Мотивация: {state.motivation_level.value}
Энергия: {state.energy_level:.2f}
Стресс: {state.stress_level:.2f}
Уверенность: {state.confidence_level:.2f}
Самооценка: {state.self_evaluation_score:.2f}
Фокус внимания: {state.attention_focus or 'не определен'}
Активные мысли: {len(state.current_thoughts)}
Активные проблемы: {len(state.active_concerns)}
"""
        
        if state.current_thoughts:
            summary += f"\nПоследние мысли:\n" + "\n".join(f"- {thought}" for thought in state.current_thoughts[-3:])
            
        if state.active_concerns:
            summary += f"\nАктивные проблемы:\n" + "\n".join(f"- {concern}" for concern in state.active_concerns)
            
        return summary.strip()
    
    def _save_state_snapshot(self):
        """Сохранить снимок состояния в историю"""
        # Создать копию текущего состояния
        snapshot = InnerStateSnapshot()
        snapshot.timestamp = self.current_state.timestamp
        snapshot.emotional_state = self.current_state.emotional_state
        snapshot.cognitive_state = self.current_state.cognitive_state
        snapshot.motivation_level = self.current_state.motivation_level
        snapshot.attention_focus = self.current_state.attention_focus
        snapshot.energy_level = self.current_state.energy_level
        snapshot.stress_level = self.current_state.stress_level
        snapshot.confidence_level = self.current_state.confidence_level
        snapshot.learning_rate = self.current_state.learning_rate
        snapshot.context_awareness = self.current_state.context_awareness
        snapshot.self_evaluation_score = self.current_state.self_evaluation_score
        snapshot.current_thoughts = self.current_state.current_thoughts.copy()
        snapshot.active_concerns = self.current_state.active_concerns.copy()
        snapshot.metadata = self.current_state.metadata.copy()
        
        self.state_history.append(snapshot)
        
        # Ограничить размер истории
        if len(self.state_history) > self.max_history_length:
            self.state_history = self.state_history[-self.max_history_length:]
    
    def save_to_file(self, filepath: str):
        """Сохранить состояние в файл"""
        data = {
            "current_state": self.current_state.to_dict(),
            "state_history": [state.to_dict() for state in self.state_history[-100:]],
            "state_transitions": self.state_transitions,
            "reflection_log": self.reflection_log[-50:]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2) 