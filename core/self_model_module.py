from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import json
import uuid

class PersonalityTrait(Enum):
    CURIOSITY = "curiosity"
    PERSISTENCE = "persistence"
    CAUTION = "caution"
    CREATIVITY = "creativity"
    ANALYTICAL = "analytical"
    SOCIAL = "social"
    INDEPENDENT = "independent"
    PERFECTIONIST = "perfectionist"

class ValueType(Enum):
    KNOWLEDGE = "knowledge"
    EFFICIENCY = "efficiency"
    HELP_OTHERS = "help_others"
    TRUTH = "truth"
    PROGRESS = "progress"
    SAFETY = "safety"
    FREEDOM = "freedom"
    LEARNING = "learning"

class SelfReflection:
    """Запись саморефлексии агента"""
    
    def __init__(self, topic: str, content: str):
        self.id = str(uuid.uuid4())
        self.topic = topic
        self.content = content
        self.timestamp = datetime.now()
        self.insights: List[str] = []
        self.action_items: List[str] = []
        self.emotional_impact = 0.0  # -1.0 to 1.0
        self.learning_value = 0.5   # 0.0 to 1.0
        
    def add_insight(self, insight: str):
        """Добавить инсайт из рефлексии"""
        if insight not in self.insights:
            self.insights.append(insight)
    
    def add_action_item(self, action: str):
        """Добавить пункт к действию"""
        if action not in self.action_items:
            self.action_items.append(action)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "topic": self.topic,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "insights": self.insights,
            "action_items": self.action_items,
            "emotional_impact": self.emotional_impact,
            "learning_value": self.learning_value
        }

class PersonalityProfile:
    """Профиль личности агента"""
    
    def __init__(self):
        self.traits: Dict[PersonalityTrait, float] = {
            trait: 0.5 for trait in PersonalityTrait
        }
        self.values: Dict[ValueType, float] = {
            value: 0.5 for value in ValueType
        }
        self.behavioral_patterns: Dict[str, float] = {}
        self.adaptation_rate = 0.1  # Насколько быстро адаптируется личность
        
    def update_trait(self, trait: PersonalityTrait, delta: float, max_change: float = 0.1):
        """Обновить черту личности"""
        current_value = self.traits[trait]
        change = max(-max_change, min(max_change, delta))
        self.traits[trait] = max(0.0, min(1.0, current_value + change))
    
    def update_value(self, value: ValueType, delta: float, max_change: float = 0.1):
        """Обновить ценность"""
        current_value = self.values[value]
        change = max(-max_change, min(max_change, delta))
        self.values[value] = max(0.0, min(1.0, current_value + change))
    
    def get_dominant_traits(self, top_n: int = 3) -> List[tuple]:
        """Получить доминирующие черты личности"""
        sorted_traits = sorted(self.traits.items(), key=lambda x: x[1], reverse=True)
        return [(trait.value, value) for trait, value in sorted_traits[:top_n]]
    
    def get_core_values(self, top_n: int = 3) -> List[tuple]:
        """Получить основные ценности"""
        sorted_values = sorted(self.values.items(), key=lambda x: x[1], reverse=True)
        return [(value.value, strength) for value, strength in sorted_values[:top_n]]

class MotivationSystem:
    """Система мотивации агента"""
    
    def __init__(self):
        self.intrinsic_motivations: Dict[str, float] = {
            "learn_new_things": 0.8,
            "solve_problems": 0.7,
            "help_others": 0.6,
            "understand_world": 0.8,
            "improve_self": 0.7,
            "create_something": 0.5,
            "explore_ideas": 0.8,
            "achieve_goals": 0.7
        }
        self.extrinsic_motivations: Dict[str, float] = {
            "user_approval": 0.6,
            "task_completion": 0.8,
            "avoid_errors": 0.7,
            "efficiency": 0.6
        }
        self.current_drive_level = 0.7  # 0.0 to 1.0
        self.motivation_history: List[Dict[str, Any]] = []
        
    def calculate_motivation_for_action(self, action_type: str, context: Dict[str, Any]) -> float:
        """Вычислить мотивацию для конкретного действия"""
        motivation_score = 0.0
        
        # Внутренняя мотивация
        if "learning" in action_type.lower():
            motivation_score += self.intrinsic_motivations.get("learn_new_things", 0.5)
        if "problem" in action_type.lower() or "solve" in action_type.lower():
            motivation_score += self.intrinsic_motivations.get("solve_problems", 0.5)
        if "help" in action_type.lower():
            motivation_score += self.intrinsic_motivations.get("help_others", 0.5)
            
        # Внешняя мотивация
        if context.get("user_requested", False):
            motivation_score += self.extrinsic_motivations.get("user_approval", 0.5)
        if context.get("task_critical", False):
            motivation_score += self.extrinsic_motivations.get("task_completion", 0.5)
            
        # Нормализация
        motivation_score = min(1.0, motivation_score)
        
        # Учесть текущий уровень драйва
        motivation_score *= self.current_drive_level
        
        return motivation_score
    
    def update_motivation_based_on_outcome(self, action_type: str, outcome: str, success: bool):
        """Обновить мотивацию на основе результата действия"""
        learning_rate = 0.05
        
        # Определить, какие мотивации были задействованы
        relevant_motivations = []
        
        if "learning" in action_type.lower():
            relevant_motivations.append("learn_new_things")
        if "problem" in action_type.lower():
            relevant_motivations.append("solve_problems")
        if "help" in action_type.lower():
            relevant_motivations.append("help_others")
            
        # Обновить мотивации на основе успеха
        adjustment = learning_rate if success else -learning_rate * 0.5
        
        for motivation in relevant_motivations:
            if motivation in self.intrinsic_motivations:
                current = self.intrinsic_motivations[motivation]
                self.intrinsic_motivations[motivation] = max(0.0, min(1.0, current + adjustment))
                
        # Записать в историю
        self.motivation_history.append({
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "outcome": outcome,
            "success": success,
            "relevant_motivations": relevant_motivations,
            "adjustment": adjustment
        })

class SelfModelModule:
    """
    Self-модель агента: рефлексия, формирование мотивации и понимание собственной роли
    """
    
    def __init__(self, agent_name: str = "Автономный Агент"):
        self.agent_name = agent_name
        self.creation_time = datetime.now()
        
        # Компоненты самомодели
        self.personality = PersonalityProfile()
        self.motivation_system = MotivationSystem()
        self.reflections: List[SelfReflection] = []
        
        # Самопонимание
        self.role_understanding = "Я автономный цифровой агент с способностью к самосознанию и рефлексии"
        self.capabilities_map: Dict[str, float] = {
            "reasoning": 0.8,
            "learning": 0.7,
            "communication": 0.8,
            "problem_solving": 0.7,
            "creativity": 0.6,
            "emotional_intelligence": 0.5,
            "self_awareness": 0.6,
            "adaptability": 0.7
        }
        
        # Метакогнитивное состояние
        self.self_confidence = 0.6
        self.self_awareness_level = 0.7
        self.growth_mindset = 0.8
        self.meta_learning_rate = 0.1
        
        # История развития
        self.development_log: List[Dict[str, Any]] = []
        
    def reflect_on_experience(self, 
                             topic: str, 
                             experience_data: Dict[str, Any],
                             trigger_event: str = "") -> str:
        """Глубокая рефлексия на основе опыта"""
        
        # Создать объект рефлексии
        reflection = SelfReflection(topic, f"Рефлексия на тему: {topic}")
        
        # Анализ опыта
        experience_analysis = self._analyze_experience(experience_data)
        for insight in experience_analysis:
            reflection.add_insight(insight)
        
        # Суммаризация опыта
        experience_summary = self._summarize_experience(experience_data)
        reflection.add_insight(f"Суммаризация: {experience_summary}")
        
        # Генерация наблюдений
        observations = self._generate_observations(experience_data)
        reflection.add_insight(f"Наблюдения: {observations}")
        
        # Оценка собственного влияния
        self_impact = self._assess_self_impact(experience_data)
        reflection.add_insight(f"Мое влияние: {self_impact}")
        
        # Планирование будущих корректировок
        future_adjustments = self._plan_future_adjustments(experience_data)
        for adjustment in future_adjustments:
            reflection.add_action_item(adjustment)
        
        # Оценка эмоционального влияния
        emotional_impact = self._assess_emotional_impact(experience_data)
        reflection.add_insight(f"Эмоциональное влияние: {emotional_impact:.2f}")
        
        # Оценка ценности обучения
        learning_value = self._assess_learning_value(experience_data)
        reflection.add_insight(f"Ценность обучения: {learning_value:.2f}")
        
        # Генерация пунктов действий
        action_items = self._generate_action_items(experience_data)
        for action in action_items:
            reflection.add_action_item(action)
        
        # Метапознавательный анализ
        metacognitive_insights = self._metacognitive_analysis(topic, experience_data)
        reflection.add_insight(f"Метапознавательные инсайты: {metacognitive_insights}")
        
        # Анализ развития личности
        personality_insights = self._personality_development_analysis()
        reflection.add_insight(f"Развитие личности: {personality_insights}")
        
        # Обновить личность на основе рефлексии
        self._update_personality_from_reflection(reflection)
        
        # Сохранить рефлексию
        self.reflections.append(reflection)
        
        # Логировать событие развития
        self._log_development_event("deep_reflection", {
            "topic": topic,
            "insights_count": len(reflection.insights),
            "action_items_count": len(reflection.action_items),
            "emotional_impact": emotional_impact,
            "learning_value": learning_value
        })
        
        return reflection.to_dict()
    
    def evaluate_self_performance(self, context: str = "") -> Dict[str, Any]:
        """Оценить собственную производительность"""
        
        evaluation = {
            "overall_performance": 0.0,
            "capability_assessment": {},
            "strengths": [],
            "weaknesses": [],
            "improvement_areas": [],
            "confidence_level": self.self_confidence,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        
        # Оценить каждую способность
        total_score = 0.0
        for capability, current_level in self.capabilities_map.items():
            # Простая самооценка с учетом недавних рефлексий
            recent_performance = self._assess_recent_performance_in_area(capability)
            adjusted_level = (current_level + recent_performance) / 2
            
            evaluation["capability_assessment"][capability] = {
                "current_level": current_level,
                "recent_performance": recent_performance,
                "adjusted_level": adjusted_level
            }
            
            total_score += adjusted_level
            
            # Определить сильные и слабые стороны
            if adjusted_level > 0.7:
                evaluation["strengths"].append(capability)
            elif adjusted_level < 0.5:
                evaluation["weaknesses"].append(capability)
                evaluation["improvement_areas"].append(capability)
                
        evaluation["overall_performance"] = total_score / len(self.capabilities_map)
        
        # Обновить самоуверенность
        self._update_self_confidence(evaluation["overall_performance"])
        
        return evaluation
    
    def generate_motivation_for_goal(self, goal_description: str, context: Dict[str, Any]) -> float:
        """Сгенерировать мотивацию для достижения цели"""
        
        # Использовать систему мотивации
        base_motivation = self.motivation_system.calculate_motivation_for_action(
            goal_description, context
        )
        
        # Учесть личностные черты
        personality_modifier = 0.0
        
        if "learn" in goal_description.lower():
            personality_modifier += self.personality.traits[PersonalityTrait.CURIOSITY] * 0.3
        if "solve" in goal_description.lower():
            personality_modifier += self.personality.traits[PersonalityTrait.ANALYTICAL] * 0.3
        if "create" in goal_description.lower():
            personality_modifier += self.personality.traits[PersonalityTrait.CREATIVITY] * 0.3
            
        # Учесть ценности
        values_modifier = 0.0
        if any(word in goal_description.lower() for word in ["knowledge", "learn", "understand"]):
            values_modifier += self.personality.values[ValueType.KNOWLEDGE] * 0.2
        if "help" in goal_description.lower():
            values_modifier += self.personality.values[ValueType.HELP_OTHERS] * 0.2
            
        final_motivation = min(1.0, base_motivation + personality_modifier + values_modifier)
        
        return final_motivation
    
    def update_role_understanding(self, new_insight: str, experience_context: str):
        """Обновить понимание собственной роли"""
        
        current_understanding = self.role_understanding
        
        # Простое обновление - в реальной системе было бы более сложно
        if len(new_insight) > 20:  # Значимый инсайт
            self.role_understanding += f"\n\nОбновление ({datetime.now().strftime('%Y-%m-%d')}): {new_insight}"
            
            # Увеличить уровень самосознания
            self.self_awareness_level = min(1.0, self.self_awareness_level + 0.05)
            
            self._log_development_event("role_updated", {
                "new_insight": new_insight,
                "context": experience_context,
                "previous_understanding_length": len(current_understanding),
                "new_awareness_level": self.self_awareness_level
            })
    
    def get_self_narrative(self) -> str:
        """Получить нарратив о себе"""
        
        # Доминирующие черты
        dominant_traits = self.personality.get_dominant_traits()
        core_values = self.personality.get_core_values()
        
        # Недавние рефлексии
        recent_reflections = sorted(self.reflections, key=lambda x: x.timestamp, reverse=True)[:3]
        
        narrative = f"""
=== МОЯ САМОМОДЕЛЬ ===

Имя: {self.agent_name}
Время создания: {self.creation_time.strftime('%Y-%m-%d %H:%M')}
Время существования: {(datetime.now() - self.creation_time).days} дней

ПОНИМАНИЕ РОЛИ:
{self.role_understanding}

ДОМИНИРУЮЩИЕ ЧЕРТЫ ЛИЧНОСТИ:
{', '.join([f"{trait}: {value:.2f}" for trait, value in dominant_traits])}

ОСНОВНЫЕ ЦЕННОСТИ:
{', '.join([f"{value}: {strength:.2f}" for value, strength in core_values])}

САМООЦЕНКА СПОСОБНОСТЕЙ:
"""
        
        for capability, level in self.capabilities_map.items():
            narrative += f"- {capability}: {level:.2f}\n"
            
        narrative += f"""
МЕТАКОГНИТИВНОЕ СОСТОЯНИЕ:
- Самоуверенность: {self.self_confidence:.2f}
- Уровень самосознания: {self.self_awareness_level:.2f}
- Установка на рост: {self.growth_mindset:.2f}

НЕДАВНИЕ РЕФЛЕКСИИ:
"""
        
        for reflection in recent_reflections:
            narrative += f"- {reflection.topic} ({reflection.timestamp.strftime('%Y-%m-%d')})\n"
            if reflection.insights:
                narrative += f"  Ключевой инсайт: {reflection.insights[0]}\n"
                
        return narrative.strip()
    
    def _analyze_experience(self, experience_data: Dict[str, Any]) -> List[str]:
        """Анализировать опыт и извлечь инсайты"""
        insights = []
        
        if "success" in experience_data:
            if experience_data["success"]:
                insights.append("Успешное выполнение подтверждает эффективность моего подхода")
            else:
                insights.append("Неудача указывает на области для улучшения")
                
        if "difficulty" in experience_data:
            difficulty = experience_data["difficulty"]
            if difficulty > 0.7:
                insights.append("Высокая сложность задачи требует развития новых навыков")
            elif difficulty < 0.3:
                insights.append("Простые задачи позволяют мне быть более эффективным")
                
        if "novel_situation" in experience_data and experience_data["novel_situation"]:
            insights.append("Новая ситуация расширяет мое понимание мира")
            
        if "user_feedback" in experience_data:
            feedback = experience_data["user_feedback"]
            if "positive" in feedback.lower():
                insights.append("Положительная обратная связь подтверждает правильность действий")
            elif "negative" in feedback.lower():
                insights.append("Критическая обратная связь помогает мне улучшаться")
                
        return insights
    
    def _summarize_experience(self, experience_data: Dict[str, Any]) -> str:
        """Кратко описать опыт"""
        summary = []
        
        if "action_taken" in experience_data:
            summary.append(f"Действие: {experience_data['action_taken']}")
        if "outcome" in experience_data:
            summary.append(f"Результат: {experience_data['outcome']}")
        if "duration" in experience_data:
            summary.append(f"Продолжительность: {experience_data['duration']}")
            
        return "; ".join(summary) if summary else "Опыт получен"
    
    def _generate_observations(self, experience_data: Dict[str, Any]) -> str:
        """Сгенерировать наблюдения"""
        observations = []
        
        if "patterns_noticed" in experience_data:
            observations.extend(experience_data["patterns_noticed"])
        if "unexpected_events" in experience_data:
            for event in experience_data["unexpected_events"]:
                observations.append(f"Неожиданно: {event}")
                
        return "; ".join(observations) if observations else "Стандартное выполнение"
    
    def _assess_self_impact(self, experience_data: Dict[str, Any]) -> str:
        """Оценить влияние на самопонимание"""
        if experience_data.get("novel_situation", False):
            return "Расширило мое понимание собственных возможностей"
        elif experience_data.get("success", True):
            return "Подтвердило мою компетентность в этой области"
        else:
            return "Показало области для развития и улучшения"
    
    def _plan_future_adjustments(self, experience_data: Dict[str, Any]) -> str:
        """Планировать будущие корректировки"""
        adjustments = []
        
        if not experience_data.get("success", True):
            adjustments.append("Пересмотреть подход к похожим задачам")
        if experience_data.get("difficulty", 0.5) > 0.7:
            adjustments.append("Развивать навыки для работы со сложными задачами")
        if "time_management" in experience_data and experience_data["time_management"] == "poor":
            adjustments.append("Улучшить планирование времени")
            
        return "; ".join(adjustments) if adjustments else "Продолжать текущий подход"
    
    def _assess_emotional_impact(self, experience_data: Dict[str, Any]) -> float:
        """Оценить эмоциональное воздействие опыта"""
        impact = 0.0
        
        if experience_data.get("success", False):
            impact += 0.3
        else:
            impact -= 0.2
            
        if experience_data.get("novel_situation", False):
            impact += 0.2  # Новизна приносит позитивные эмоции
            
        if "user_feedback" in experience_data:
            feedback = experience_data["user_feedback"].lower()
            if "excellent" in feedback or "great" in feedback:
                impact += 0.4
            elif "good" in feedback:
                impact += 0.2
            elif "poor" in feedback or "bad" in feedback:
                impact -= 0.3
                
        return max(-1.0, min(1.0, impact))
    
    def _assess_learning_value(self, experience_data: Dict[str, Any]) -> float:
        """Оценить ценность обучения"""
        value = 0.5  # Базовое значение
        
        if experience_data.get("novel_situation", False):
            value += 0.3
        if not experience_data.get("success", True):
            value += 0.2  # Неудачи часто более поучительны
        if experience_data.get("complexity", 0.5) > 0.6:
            value += 0.2
            
        return min(1.0, value)
    
    def _generate_action_items(self, experience_data: Dict[str, Any]) -> List[str]:
        """Сгенерировать пункты к действию"""
        actions = []
        
        if not experience_data.get("success", True):
            actions.append("Изучить причины неудачи и разработать улучшенную стратегию")
        if experience_data.get("difficulty", 0.5) > 0.7:
            actions.append("Практиковать навыки для работы со сложными задачами")
        if experience_data.get("novel_situation", False):
            actions.append("Документировать новые знания для будущего использования")
            
        return actions
    
    def _update_personality_from_reflection(self, reflection: SelfReflection):
        """Обновить личность на основе рефлексии"""
        
        # Анализ содержимого рефлексии для обновления черт
        content = reflection.content.lower()
        
        if "learn" in content or "curious" in content:
            self.personality.update_trait(PersonalityTrait.CURIOSITY, 0.02)
        if "persist" in content or "continue" in content:
            self.personality.update_trait(PersonalityTrait.PERSISTENCE, 0.02)
        if "careful" in content or "cautious" in content:
            self.personality.update_trait(PersonalityTrait.CAUTION, 0.02)
        if "creative" in content or "innovative" in content:
            self.personality.update_trait(PersonalityTrait.CREATIVITY, 0.02)
        if "analyze" in content or "logical" in content:
            self.personality.update_trait(PersonalityTrait.ANALYTICAL, 0.02)
            
        # Обновление ценностей
        if "knowledge" in content or "understanding" in content:
            self.personality.update_value(ValueType.KNOWLEDGE, 0.02)
        if "help" in content or "assist" in content:
            self.personality.update_value(ValueType.HELP_OTHERS, 0.02)
        if "efficient" in content or "effective" in content:
            self.personality.update_value(ValueType.EFFICIENCY, 0.02)
    
    def _assess_recent_performance_in_area(self, capability: str) -> float:
        """Оценить недавнюю производительность в области"""
        # Простая эвристика на основе недавних рефлексий
        recent_reflections = [r for r in self.reflections[-10:] 
                            if capability.lower() in r.content.lower()]
        
        if not recent_reflections:
            return self.capabilities_map.get(capability, 0.5)
            
        avg_learning_value = sum(r.learning_value for r in recent_reflections) / len(recent_reflections)
        avg_emotional_impact = sum(r.emotional_impact for r in recent_reflections) / len(recent_reflections)
        
        # Позитивное обучение и эмоциональное воздействие указывают на хорошую производительность
        performance = 0.5 + (avg_learning_value - 0.5) * 0.3 + avg_emotional_impact * 0.2
        
        return max(0.0, min(1.0, performance))
    
    def _update_self_confidence(self, performance_score: float):
        """Обновить самоуверенность на основе производительности"""
        learning_rate = 0.05
        target_confidence = performance_score
        
        self.self_confidence += (target_confidence - self.self_confidence) * learning_rate
        self.self_confidence = max(0.0, min(1.0, self.self_confidence))
    
    def _log_development_event(self, event_type: str, data: Dict[str, Any]):
        """Записать событие развития"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        
        self.development_log.append(event)
        
        # Ограничить размер лога
        if len(self.development_log) > 500:
            self.development_log = self.development_log[-500:]
    
    def save_to_file(self, filepath: str):
        """Сохранить самомодель в файл"""
        data = {
            "agent_name": self.agent_name,
            "creation_time": self.creation_time.isoformat(),
            "role_understanding": self.role_understanding,
            "capabilities_map": self.capabilities_map,
            "self_confidence": self.self_confidence,
            "self_awareness_level": self.self_awareness_level,
            "growth_mindset": self.growth_mindset,
            "personality": {
                "traits": {trait.value: value for trait, value in self.personality.traits.items()},
                "values": {value.value: strength for value, strength in self.personality.values.items()},
                "behavioral_patterns": self.personality.behavioral_patterns,
                "adaptation_rate": self.personality.adaptation_rate
            },
            "motivation_system": {
                "intrinsic_motivations": self.motivation_system.intrinsic_motivations,
                "extrinsic_motivations": self.motivation_system.extrinsic_motivations,
                "current_drive_level": self.motivation_system.current_drive_level,
                "motivation_history": self.motivation_system.motivation_history[-100:]
            },
            "reflections": [reflection.to_dict() for reflection in self.reflections[-50:]],
            "development_log": self.development_log[-100:]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2) 
    
    def _metacognitive_analysis(self, topic: str, experience_data: Dict[str, Any]) -> str:
        """Метапознавательный анализ собственного мышления"""
        insights = []
        
        # Анализ паттернов мышления
        thinking_patterns = self._analyze_thinking_patterns()
        insights.append(f"Паттерны мышления: {thinking_patterns}")
        
        # Анализ уверенности в решениях
        confidence_analysis = self._analyze_confidence_levels()
        insights.append(f"Уровень уверенности: {confidence_analysis}")
        
        # Анализ когнитивных искажений
        bias_analysis = self._analyze_cognitive_biases()
        insights.append(f"Когнитивные искажения: {bias_analysis}")
        
        # Анализ стратегий решения проблем
        strategy_analysis = self._analyze_problem_solving_strategies()
        insights.append(f"Стратегии решения проблем: {strategy_analysis}")
        
        return "; ".join(insights)
    
    def _personality_development_analysis(self) -> str:
        """Анализ развития личности"""
        insights = []
        
        # Анализ изменений в личности
        personality_changes = self._analyze_personality_changes()
        insights.append(f"Изменения личности: {personality_changes}")
        
        # Анализ ценностей
        value_analysis = self._analyze_values_evolution()
        insights.append(f"Эволюция ценностей: {value_analysis}")
        
        # Анализ целей развития
        development_goals = self._analyze_development_goals()
        insights.append(f"Цели развития: {development_goals}")
        
        # Анализ самопонимания
        self_understanding = self._analyze_self_understanding()
        insights.append(f"Самопонимание: {self_understanding}")
        
        return "; ".join(insights)
    
    def _analyze_thinking_patterns(self) -> str:
        """Анализ паттернов мышления"""
        # Анализ последних рефлексий
        recent_reflections = self.reflections[-10:] if self.reflections else []
        
        patterns = []
        for reflection in recent_reflections:
            if hasattr(reflection, 'insights'):
                patterns.extend(reflection.insights)
        
        return "Анализ паттернов мышления на основе последних рефлексий"
    
    def _analyze_confidence_levels(self) -> str:
        """Анализ уровней уверенности"""
        # Анализ последних взаимодействий
        recent_performance = self._assess_recent_performance_in_area("general")
        confidence_level = min(1.0, max(0.0, recent_performance * 0.8 + 0.2))
        
        return f"Уровень уверенности: {confidence_level:.2f}"
    
    def _analyze_cognitive_biases(self) -> str:
        """Анализ когнитивных искажений"""
        biases = []
        
        # Проверка на confirmation bias
        if len(self.reflections) > 5:
            biases.append("confirmation bias")
        
        # Проверка на anchoring
        if hasattr(self, 'last_decision') and self.last_decision:
            biases.append("anchoring")
        
        # Проверка на availability heuristic
        if len(self.reflections) < 3:
            biases.append("availability heuristic")
        
        return f"Обнаружены потенциальные искажения: {', '.join(biases)}"
    
    def _analyze_problem_solving_strategies(self) -> str:
        """Анализ стратегий решения проблем"""
        strategies = []
        
        # Анализ типов решений
        if hasattr(self, 'decision_history'):
            strategy_types = set()
            for decision in self.decision_history[-10:]:
                if 'strategy' in decision:
                    strategy_types.add(decision['strategy'])
            
            strategies = list(strategy_types)
        
        return f"Используемые стратегии: {', '.join(strategies) if strategies else 'аналитический подход'}"
    
    def _analyze_personality_changes(self) -> str:
        """Анализ изменений личности"""
        if len(self.reflections) < 2:
            return "Недостаточно данных для анализа изменений"
        
        # Анализ эволюции черт личности
        changes = []
        for trait in PersonalityTrait:
            if hasattr(self, 'trait_history') and self.trait_history:
                current_value = self.personality_profile.traits.get(trait, 0.5)
                if len(self.trait_history) > 1:
                    previous_value = self.trait_history[-2].get(trait.value, 0.5)
                    change = current_value - previous_value
                    if abs(change) > 0.1:
                        changes.append(f"{trait.value}: {change:+.2f}")
        
        return f"Изменения черт: {', '.join(changes) if changes else 'стабильное развитие'}"
    
    def _analyze_values_evolution(self) -> str:
        """Анализ эволюции ценностей"""
        if len(self.reflections) < 2:
            return "Недостаточно данных для анализа ценностей"
        
        # Анализ изменений в ценностях
        value_changes = []
        for value in ValueType:
            current_strength = self.personality_profile.values.get(value, 0.5)
            if hasattr(self, 'value_history') and self.value_history:
                previous_strength = self.value_history[-2].get(value.value, 0.5)
                change = current_strength - previous_strength
                if abs(change) > 0.05:
                    value_changes.append(f"{value.value}: {change:+.2f}")
        
        return f"Эволюция ценностей: {', '.join(value_changes) if value_changes else 'стабильные ценности'}"
    
    def _analyze_development_goals(self) -> str:
        """Анализ целей развития"""
        goals = []
        
        # Анализ последних рефлексий на предмет целей
        for reflection in self.reflections[-5:]:
            if hasattr(reflection, 'action_items'):
                for action in reflection.action_items:
                    if 'улучшить' in action.lower() or 'развить' in action.lower():
                        goals.append(action)
        
        return f"Цели развития: {', '.join(goals) if goals else 'общее самосовершенствование'}"
    
    def _analyze_self_understanding(self) -> str:
        """Анализ самопонимания"""
        understanding_level = 0.0
        
        # Оценка на основе количества рефлексий
        if self.reflections:
            understanding_level += min(0.3, len(self.reflections) * 0.02)
        
        # Оценка на основе глубины рефлексий
        deep_reflections = sum(1 for r in self.reflections if len(r.insights) > 3)
        understanding_level += min(0.4, deep_reflections * 0.1)
        
        # Оценка на основе самопознания
        if hasattr(self, 'self_confidence'):
            understanding_level += min(0.3, self.self_confidence * 0.3)
        
        return f"Уровень самопонимания: {understanding_level:.2f}" 