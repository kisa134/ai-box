import uuid
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

class GoalPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class GoalStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

@dataclass
class Goal:
    description: str
    category: str
    priority: GoalPriority
    id: str = None
    status: GoalStatus = GoalStatus.ACTIVE
    progress: float = 0.0
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    parent_goal_id: Optional[str] = None
    sub_goals: List[str] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())[:8]
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.sub_goals is None:
            self.sub_goals = []

class MotivationSystem:
    """Система мотивации агента"""
    
    def __init__(self):
        # Внутренняя мотивация
        self.intrinsic_motivations = {
            "learn_new_things": 0.89,
            "solve_problems": 0.76, 
            "help_others": 0.92,
            "understand_self": 0.68
        }
        
        # Внешняя мотивация
        self.extrinsic_motivations = {
            "user_approval": 0.71,
            "task_completion": 0.84,
            "performance_metrics": 0.62
        }
    
    def update_motivation(self, goal: Goal, success: bool):
        """Обновить мотивацию на основе результата цели"""
        if success:
            # Увеличиваем соответствующую мотивацию
            if goal.category == "learning":
                self.intrinsic_motivations["learn_new_things"] = min(1.0, 
                    self.intrinsic_motivations["learn_new_things"] + 0.05)
            elif goal.category == "communication":
                self.intrinsic_motivations["help_others"] = min(1.0,
                    self.intrinsic_motivations["help_others"] + 0.03)
            
            self.extrinsic_motivations["task_completion"] = min(1.0,
                self.extrinsic_motivations["task_completion"] + 0.02)
        else:
            # Небольшое снижение при неудаче
            self.extrinsic_motivations["task_completion"] = max(0.0,
                self.extrinsic_motivations["task_completion"] - 0.01)
    
    def get_motivation_for_goal(self, goal: Goal) -> float:
        """Получить уровень мотивации для конкретной цели"""
        category_motivation = {
            "learning": self.intrinsic_motivations["learn_new_things"],
            "communication": self.intrinsic_motivations["help_others"],
            "self_development": self.intrinsic_motivations["understand_self"],
            "problem_solving": self.intrinsic_motivations["solve_problems"]
        }
        
        base_motivation = category_motivation.get(goal.category, 0.5)
        priority_bonus = {
            GoalPriority.HIGH: 0.2,
            GoalPriority.MEDIUM: 0.1,
            GoalPriority.LOW: 0.0
        }
        
        return min(1.0, base_motivation + priority_bonus[goal.priority])

class GoalModule:
    """Модуль управления целями агента с интегрированной системой мотивации"""
    
    def __init__(self, data_dir: str = "agent_data"):
        self.data_dir = data_dir
        self.goals: Dict[str, Goal] = {}
        self.motivation_system = MotivationSystem()
        self.goal_hierarchy = {}  # Иерархия целей
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Инициализация базовых целей
        self._initialize_default_goals()
    
    def _initialize_default_goals(self):
        """Инициализация базовых целей без дублирования"""
        initial_goals = [
            ("Понимать и помогать пользователям", "communication", GoalPriority.HIGH),
            ("Постоянно учиться и развиваться", "learning", GoalPriority.HIGH),
            ("Развивать самосознание и рефлексию", "self_development", GoalPriority.MEDIUM),
            ("Поддерживать позитивное взаимодействие", "social", GoalPriority.LOW)
        ]
        
        for description, category, priority in initial_goals:
            self.add_goal(description, category, priority)
    
    def add_goal(self, description: str, category: str, priority: GoalPriority) -> str:
        """Добавить новую цель с проверкой дублирования"""
        # Проверяем на дублирование
        for existing_goal in self.goals.values():
            if existing_goal.description.lower() == description.lower():
                self.logger.info(f"Цель уже существует: {description}")
                return existing_goal.id
        
        goal = Goal(description, category, priority)
        self.goals[goal.id] = goal
        
        # Интеграция с другими модулями
        self._integrate_with_motivation(goal)
        self._update_goal_hierarchy()
        
        self.logger.info(f"Добавлена новая цель: {description}")
        return goal.id
    
    def _integrate_with_motivation(self, goal: Goal):
        """Интеграция цели с системой мотивации"""
        motivation_level = self.motivation_system.get_motivation_for_goal(goal)
        
        # Корректируем приоритет на основе мотивации
        if motivation_level > 0.8 and goal.priority == GoalPriority.MEDIUM:
            goal.priority = GoalPriority.HIGH
            self.logger.info(f"Повышен приоритет цели '{goal.description}' до HIGH из-за высокой мотивации")
    
    def _update_goal_hierarchy(self):
        """Обновить иерархию целей"""
        self.goal_hierarchy = {}
        
        # Группируем цели по категориям
        for goal in self.goals.values():
            if goal.category not in self.goal_hierarchy:
                self.goal_hierarchy[goal.category] = []
            self.goal_hierarchy[goal.category].append(goal.id)
        
        # Сортируем по приоритету
        for category in self.goal_hierarchy:
            self.goal_hierarchy[category].sort(
                key=lambda goal_id: self.goals[goal_id].priority.value, 
                reverse=True
            )
    
    def update_goal_progress(self, goal_id: str, progress: float):
        """Обновить прогресс цели"""
        if goal_id in self.goals:
            old_progress = self.goals[goal_id].progress
            self.goals[goal_id].progress = max(0.0, min(1.0, progress))
            
            # Проверяем завершение
            if progress >= 1.0 and self.goals[goal_id].status == GoalStatus.ACTIVE:
                self.complete_goal(goal_id)
            
            # Обновляем мотивацию
            if progress > old_progress:
                self.motivation_system.update_motivation(self.goals[goal_id], True)
            
            self.logger.info(f"Обновлен прогресс цели {goal_id}: {progress:.2%}")
    
    def complete_goal(self, goal_id: str):
        """Завершить цель"""
        if goal_id in self.goals:
            self.goals[goal_id].status = GoalStatus.COMPLETED
            self.goals[goal_id].completed_at = datetime.now()
            self.goals[goal_id].progress = 1.0
            
            # Обновляем мотивацию
            self.motivation_system.update_motivation(self.goals[goal_id], True)
            
            self.logger.info(f"Завершена цель: {self.goals[goal_id].description}")
            
            # Генерируем подцели если необходимо
            self._generate_follow_up_goals(goal_id)
    
    def _generate_follow_up_goals(self, completed_goal_id: str):
        """Генерация последующих целей на основе завершенной"""
        completed_goal = self.goals[completed_goal_id]
        
        # Примеры автоматической генерации подцелей
        if completed_goal.category == "learning":
            new_description = f"Применить знания из '{completed_goal.description}'"
            self.add_goal(new_description, "application", GoalPriority.MEDIUM)
        
        elif completed_goal.category == "communication":
            new_description = f"Улучшить навыки на основе '{completed_goal.description}'"
            self.add_goal(new_description, "improvement", GoalPriority.LOW)
    
    def get_active_goals(self) -> List[Goal]:
        """Получить список активных целей"""
        return [goal for goal in self.goals.values() if goal.status == GoalStatus.ACTIVE]
    
    def get_goals_by_priority(self, priority: GoalPriority) -> List[Goal]:
        """Получить цели по приоритету"""
        return [goal for goal in self.goals.values() 
                if goal.priority == priority and goal.status == GoalStatus.ACTIVE]
    
    def get_next_goal(self) -> Optional[Goal]:
        """Получить следующую цель для выполнения"""
        active_goals = self.get_active_goals()
        if not active_goals:
            return None
        
        # Сортируем по приоритету и прогрессу
        return sorted(active_goals, 
                     key=lambda g: (g.priority.value, -g.progress))[0]
    
    def get_current_goal(self) -> Optional[Goal]:
        """Получить текущую активную цель (синоним для get_next_goal)"""
        return self.get_next_goal()
    
    def get_goal_statistics(self) -> Dict[str, Any]:
        """Получить статистику по целям"""
        total = len(self.goals)
        active = len([g for g in self.goals.values() if g.status == GoalStatus.ACTIVE])
        completed = len([g for g in self.goals.values() if g.status == GoalStatus.COMPLETED])
        
        avg_progress = sum(g.progress for g in self.get_active_goals()) / max(1, active)
        
        return {
            "total_goals": total,
            "active_goals": active,
            "completed_goals": completed,
            "average_progress": avg_progress,
            "goal_hierarchy": self.goal_hierarchy,
            "motivation_system": {
                "intrinsic": self.motivation_system.intrinsic_motivations,
                "extrinsic": self.motivation_system.extrinsic_motivations
            }
        }
    
    def save_state(self, filepath: str):
        """Сохранить состояние модуля"""
        state = {
            "goals": {goal_id: asdict(goal) for goal_id, goal in self.goals.items()},
            "motivation_system": {
                "intrinsic": self.motivation_system.intrinsic_motivations,
                "extrinsic": self.motivation_system.extrinsic_motivations
            },
            "goal_hierarchy": self.goal_hierarchy
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2, default=str)
    
    def load_state(self, filepath: str):
        """Загрузить состояние модуля"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # Восстанавливаем цели
            self.goals = {}
            for goal_id, goal_data in state.get("goals", {}).items():
                goal_data["created_at"] = datetime.fromisoformat(goal_data["created_at"])
                if goal_data.get("completed_at"):
                    goal_data["completed_at"] = datetime.fromisoformat(goal_data["completed_at"])
                goal_data["priority"] = GoalPriority(goal_data["priority"])
                goal_data["status"] = GoalStatus(goal_data["status"])
                
                self.goals[goal_id] = Goal(**goal_data)
            
            # Восстанавливаем мотивацию
            motivation_data = state.get("motivation_system", {})
            self.motivation_system.intrinsic_motivations.update(
                motivation_data.get("intrinsic", {})
            )
            self.motivation_system.extrinsic_motivations.update(
                motivation_data.get("extrinsic", {})
            )
            
            # Восстанавливаем иерархию
            self.goal_hierarchy = state.get("goal_hierarchy", {})
            
            self.logger.info(f"Загружено {len(self.goals)} целей из {filepath}")
        
        except Exception as e:
            self.logger.error(f"Ошибка загрузки состояния: {e}")
            self._initialize_default_goals()  # Инициализируем дефолтные цели при ошибке 