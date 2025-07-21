from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from enum import Enum
import uuid
import json
import networkx as nx

class ThoughtType(Enum):
    OBSERVATION = "observation"
    HYPOTHESIS = "hypothesis"
    ANALYSIS = "analysis"
    PLAN = "plan"
    DECISION = "decision"
    REFLECTION = "reflection"
    CRITIQUE = "critique"
    ALTERNATIVE = "alternative"

class ThoughtStatus(Enum):
    ACTIVE = "active"
    EVALUATED = "evaluated"
    SELECTED = "selected"
    REJECTED = "rejected"
    PAUSED = "paused"

class Thought:
    """Узел в дереве мыслей"""
    
    def __init__(self, 
                 content: str, 
                 thought_type: ThoughtType = ThoughtType.OBSERVATION,
                 parent_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.content = content
        self.thought_type = thought_type
        self.parent_id = parent_id
        self.children_ids: List[str] = []
        self.status = ThoughtStatus.ACTIVE
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Оценки и метрики
        self.feasibility_score = 0.5  # 0.0 to 1.0
        self.confidence_score = 0.5   # 0.0 to 1.0
        self.novelty_score = 0.5      # 0.0 to 1.0
        self.relevance_score = 0.5    # 0.0 to 1.0
        self.overall_score = 0.5      # 0.0 to 1.0
        
        # Контекст и метаданные
        self.context: Dict[str, Any] = {}
        self.evidence: List[str] = []  # Поддерживающие доказательства
        self.counterarguments: List[str] = []  # Контраргументы
        self.assumptions: List[str] = []  # Предположения
        self.dependencies: List[str] = []  # ID других мыслей, от которых зависит эта
        
    def add_child(self, child_id: str):
        """Добавить дочернюю мысль"""
        if child_id not in self.children_ids:
            self.children_ids.append(child_id)
            self.updated_at = datetime.now()
    
    def add_evidence(self, evidence: str):
        """Добавить поддерживающее доказательство"""
        if evidence not in self.evidence:
            self.evidence.append(evidence)
            self.updated_at = datetime.now()
    
    def add_counterargument(self, argument: str):
        """Добавить контраргумент"""
        if argument not in self.counterarguments:
            self.counterarguments.append(argument)
            self.updated_at = datetime.now()
    
    def update_scores(self, 
                     feasibility: Optional[float] = None,
                     confidence: Optional[float] = None,
                     novelty: Optional[float] = None,
                     relevance: Optional[float] = None):
        """Обновить оценки мысли"""
        if feasibility is not None:
            self.feasibility_score = max(0.0, min(1.0, feasibility))
        if confidence is not None:
            self.confidence_score = max(0.0, min(1.0, confidence))
        if novelty is not None:
            self.novelty_score = max(0.0, min(1.0, novelty))
        if relevance is not None:
            self.relevance_score = max(0.0, min(1.0, relevance))
            
        # Пересчитать общую оценку
        self.overall_score = (
            self.feasibility_score * 0.3 +
            self.confidence_score * 0.3 +
            self.novelty_score * 0.2 +
            self.relevance_score * 0.2
        )
        
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "thought_type": self.thought_type.value,
            "parent_id": self.parent_id,
            "children_ids": self.children_ids,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "feasibility_score": self.feasibility_score,
            "confidence_score": self.confidence_score,
            "novelty_score": self.novelty_score,
            "relevance_score": self.relevance_score,
            "overall_score": self.overall_score,
            "context": self.context,
            "evidence": self.evidence,
            "counterarguments": self.counterarguments,
            "assumptions": self.assumptions,
            "dependencies": self.dependencies
        }

class ThoughtBranch:
    """Ветвь мыслей для исследования альтернатив"""
    
    def __init__(self, name: str, root_thought_id: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.root_thought_id = root_thought_id
        self.thought_ids: List[str] = [root_thought_id]
        self.status = "exploring"  # exploring, evaluated, selected, abandoned
        self.depth = 1
        self.branch_score = 0.5
        
    def add_thought(self, thought_id: str):
        """Добавить мысль в ветвь"""
        if thought_id not in self.thought_ids:
            self.thought_ids.append(thought_id)
            self.depth = len(self.thought_ids)

class ThoughtTreeModule:
    """
    Дерево мыслей (ToT), критический анализ, динамический фокус внимания,
    секция гипотез
    """
    
    def __init__(self):
        self.thoughts: Dict[str, Thought] = {}
        self.branches: Dict[str, ThoughtBranch] = {}
        self.current_focus: Optional[str] = None  # ID текущей мысли в фокусе
        self.attention_stack: List[str] = []  # Стек внимания
        self.reasoning_log: List[Dict[str, Any]] = []
        self.critique_enabled = True
        
        # Граф для анализа связей
        self.thought_graph = nx.DiGraph()
        
    def add_thought(self, 
                   content: str,
                   thought_type: ThoughtType = ThoughtType.OBSERVATION,
                   parent_id: Optional[str] = None,
                   context: Optional[Dict[str, Any]] = None) -> str:
        """Добавить мысль в дерево"""
        thought = Thought(content, thought_type, parent_id)
        
        if context:
            thought.context = context
            
        self.thoughts[thought.id] = thought
        
        # Обновить связи
        if parent_id and parent_id in self.thoughts:
            self.thoughts[parent_id].add_child(thought.id)
            
        # Добавить в граф
        self.thought_graph.add_node(thought.id, **thought.to_dict())
        if parent_id:
            self.thought_graph.add_edge(parent_id, thought.id)
            
        # Автоматическая оценка
        self._auto_evaluate_thought(thought.id)
        
        # Логирование
        self._log_reasoning("thought_added", {
            "thought_id": thought.id,
            "content": content,
            "type": thought_type.value,
            "parent_id": parent_id
        })
        
        return thought.id
    
    def branch_thought(self, 
                      parent_id: str, 
                      alternatives: List[str],
                      branch_name: Optional[str] = None) -> List[str]:
        """Создать ветвления от мысли (исследование альтернатив)"""
        if parent_id not in self.thoughts:
            return []
            
        new_thought_ids = []
        
        for i, alternative in enumerate(alternatives):
            # Создать альтернативную мысль
            alt_id = self.add_thought(
                content=alternative,
                thought_type=ThoughtType.ALTERNATIVE,
                parent_id=parent_id
            )
            new_thought_ids.append(alt_id)
            
            # Создать ветвь если нужно
            if branch_name or len(alternatives) > 1:
                branch_name = branch_name or f"Альтернатива {i+1}"
                branch = ThoughtBranch(f"{branch_name}_{i+1}", alt_id)
                self.branches[branch.id] = branch
                
        self._log_reasoning("thought_branched", {
            "parent_id": parent_id,
            "alternatives_count": len(alternatives),
            "new_thought_ids": new_thought_ids
        })
        
        return new_thought_ids
    
    def critique_thought(self, thought_id: str, auto_generate: bool = True) -> List[str]:
        """Критически проанализировать мысль"""
        if thought_id not in self.thoughts:
            return []
            
        thought = self.thoughts[thought_id]
        critiques = []
        
        if auto_generate:
            # Автоматическая генерация критики
            auto_critiques = self._generate_auto_critique(thought)
            
            for critique_content in auto_critiques:
                critique_id = self.add_thought(
                    content=critique_content,
                    thought_type=ThoughtType.CRITIQUE,
                    parent_id=thought_id
                )
                critiques.append(critique_id)
                
        self._log_reasoning("thought_critiqued", {
            "thought_id": thought_id,
            "critiques_generated": len(critiques)
        })
        
        return critiques
    
    def set_focus(self, thought_id: str):
        """Установить фокус внимания на мысль"""
        if thought_id in self.thoughts:
            # Сохранить предыдущий фокус в стек
            if self.current_focus:
                self.attention_stack.append(self.current_focus)
                
            self.current_focus = thought_id
            
            self._log_reasoning("focus_changed", {
                "new_focus": thought_id,
                "thought_content": self.thoughts[thought_id].content
            })
    
    def pop_focus(self) -> Optional[str]:
        """Вернуться к предыдущему фокусу"""
        if self.attention_stack:
            self.current_focus = self.attention_stack.pop()
            return self.current_focus
        return None
    
    def evaluate_branches(self) -> Dict[str, float]:
        """Оценить все активные ветви"""
        branch_scores = {}
        
        for branch_id, branch in self.branches.items():
            if branch.status == "exploring":
                # Вычислить оценку ветви на основе составляющих мыслей
                total_score = 0.0
                thought_count = 0
                
                for thought_id in branch.thought_ids:
                    if thought_id in self.thoughts:
                        total_score += self.thoughts[thought_id].overall_score
                        thought_count += 1
                        
                branch.branch_score = total_score / thought_count if thought_count > 0 else 0.0
                branch_scores[branch_id] = branch.branch_score
                
        return branch_scores
    
    def select_best_path(self, from_thought_id: str) -> List[str]:
        """Выбрать лучший путь от заданной мысли"""
        if from_thought_id not in self.thoughts:
            return []
            
        # Найти все пути от данной мысли
        paths = []
        self._find_all_paths(from_thought_id, [], paths)
        
        # Оценить каждый путь
        path_scores = []
        for path in paths:
            score = sum(self.thoughts[tid].overall_score for tid in path) / len(path)
            path_scores.append((path, score))
            
        # Выбрать лучший путь
        if path_scores:
            best_path = max(path_scores, key=lambda x: x[1])[0]
            
            # Отметить мысли в лучшем пути как выбранные
            for thought_id in best_path:
                self.thoughts[thought_id].status = ThoughtStatus.SELECTED
                
            self._log_reasoning("best_path_selected", {
                "from_thought": from_thought_id,
                "path": best_path,
                "path_length": len(best_path)
            })
            
            return best_path
            
        return []
    
    def generate_hypothesis(self, 
                           observation: str,
                           context: Optional[Dict[str, Any]] = None) -> str:
        """Сгенерировать гипотезу на основе наблюдения"""
        # Добавить наблюдение
        obs_id = self.add_thought(
            content=observation,
            thought_type=ThoughtType.OBSERVATION,
            context=context
        )
        
        # Сгенерировать гипотезы
        hypotheses = self._generate_hypotheses(observation)
        hypothesis_ids = []
        
        for hypothesis in hypotheses:
            hyp_id = self.add_thought(
                content=hypothesis,
                thought_type=ThoughtType.HYPOTHESIS,
                parent_id=obs_id
            )
            hypothesis_ids.append(hyp_id)
            
        # Вернуть ID лучшей гипотезы
        if hypothesis_ids:
            best_hyp_id = max(hypothesis_ids, 
                            key=lambda x: self.thoughts[x].overall_score)
            return best_hyp_id
            
        return obs_id
    
    def _auto_evaluate_thought(self, thought_id: str):
        """Автоматическая оценка мысли"""
        if thought_id not in self.thoughts:
            return
            
        thought = self.thoughts[thought_id]
        
        # Простые эвристики для оценки
        content_length = len(thought.content)
        
        # Оценка осуществимости
        feasibility = 0.8 if content_length > 20 else 0.5
        
        # Оценка уверенности на основе типа мысли
        confidence_map = {
            ThoughtType.OBSERVATION: 0.9,
            ThoughtType.HYPOTHESIS: 0.6,
            ThoughtType.ANALYSIS: 0.7,
            ThoughtType.PLAN: 0.5,
            ThoughtType.DECISION: 0.8,
            ThoughtType.REFLECTION: 0.7,
            ThoughtType.CRITIQUE: 0.6,
            ThoughtType.ALTERNATIVE: 0.5
        }
        confidence = confidence_map.get(thought.thought_type, 0.5)
        
        # Оценка новизны (упрощенная)
        novelty = 0.7 if not self._is_similar_thought_exists(thought.content) else 0.3
        
        # Оценка релевантности (на основе контекста)
        relevance = 0.8 if thought.context else 0.5
        
        thought.update_scores(feasibility, confidence, novelty, relevance)
    
    def _generate_auto_critique(self, thought: Thought) -> List[str]:
        """Автоматическая генерация критики"""
        critiques = []
        
        # Критика на основе типа мысли
        if thought.thought_type == ThoughtType.HYPOTHESIS:
            critiques.append(f"Какие доказательства поддерживают гипотезу: '{thought.content}'?")
            critiques.append(f"Какие альтернативные объяснения возможны?")
            
        elif thought.thought_type == ThoughtType.PLAN:
            critiques.append(f"Какие риски связаны с планом: '{thought.content}'?")
            critiques.append(f"Что может пойти не так при выполнении этого плана?")
            
        elif thought.thought_type == ThoughtType.DECISION:
            critiques.append(f"Рассмотрены ли все варианты при принятии решения: '{thought.content}'?")
            critiques.append(f"Каковы долгосрочные последствия этого решения?")
            
        # Общие критики
        if len(thought.evidence) == 0:
            critiques.append("Недостаточно доказательств для поддержки этой мысли")
            
        if thought.confidence_score < 0.5:
            critiques.append("Низкий уровень уверенности требует дополнительного анализа")
            
        return critiques
    
    def _generate_hypotheses(self, observation: str) -> List[str]:
        """Генерация гипотез на основе наблюдения"""
        # Простая генерация гипотез - в реальной системе использовался бы ИИ
        hypotheses = [
            f"Возможная причина: {observation}",
            f"Альтернативное объяснение для: {observation}",
            f"Потенциальная связь с предыдущими наблюдениями: {observation}"
        ]
        
        return hypotheses
    
    def _is_similar_thought_exists(self, content: str) -> bool:
        """Проверить существование похожей мысли"""
        content_lower = content.lower()
        
        for thought in self.thoughts.values():
            if content_lower in thought.content.lower() or thought.content.lower() in content_lower:
                return True
                
        return False
    
    def _find_all_paths(self, current_id: str, current_path: List[str], all_paths: List[List[str]]):
        """Рекурсивно найти все пути от мысли"""
        current_path = current_path + [current_id]
        
        thought = self.thoughts[current_id]
        if not thought.children_ids:
            # Лист дерева
            all_paths.append(current_path)
        else:
            for child_id in thought.children_ids:
                if child_id in self.thoughts:
                    self._find_all_paths(child_id, current_path, all_paths)
    
    def get_thought_tree_visualization(self) -> Dict[str, Any]:
        """Получить данные для визуализации дерева мыслей"""
        nodes = []
        edges = []
        
        for thought_id, thought in self.thoughts.items():
            nodes.append({
                "id": thought_id,
                "label": thought.content[:50] + "..." if len(thought.content) > 50 else thought.content,
                "type": thought.thought_type.value,
                "status": thought.status.value,
                "score": thought.overall_score,
                "is_focus": thought_id == self.current_focus
            })
            
            for child_id in thought.children_ids:
                edges.append({
                    "from": thought_id,
                    "to": child_id
                })
                
        return {"nodes": nodes, "edges": edges}
    
    def get_reasoning_summary(self) -> str:
        """Получить сводку рассуждений"""
        total_thoughts = len(self.thoughts)
        active_thoughts = sum(1 for t in self.thoughts.values() if t.status == ThoughtStatus.ACTIVE)
        selected_thoughts = sum(1 for t in self.thoughts.values() if t.status == ThoughtStatus.SELECTED)
        
        type_counts = {}
        for thought in self.thoughts.values():
            type_counts[thought.thought_type.value] = type_counts.get(thought.thought_type.value, 0) + 1
            
        summary = f"""
=== ДЕРЕВО МЫСЛЕЙ ===
Всего мыслей: {total_thoughts}
Активных: {active_thoughts}
Выбранных: {selected_thoughts}
Ветвей: {len(self.branches)}

Текущий фокус: {self.thoughts[self.current_focus].content[:100] if self.current_focus else 'Не установлен'}

Типы мыслей:
"""
        
        for thought_type, count in type_counts.items():
            summary += f"- {thought_type}: {count}\n"
            
        return summary.strip()
    
    def _log_reasoning(self, action: str, data: Dict[str, Any]):
        """Записать событие рассуждения в лог"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "data": data
        }
        
        self.reasoning_log.append(log_entry)
        
        # Ограничить размер лога
        if len(self.reasoning_log) > 1000:
            self.reasoning_log = self.reasoning_log[-1000:]
    
    def save_to_file(self, filepath: str):
        """Сохранить дерево мыслей в файл"""
        data = {
            "thoughts": {tid: thought.to_dict() for tid, thought in self.thoughts.items()},
            "branches": {bid: {
                "id": branch.id,
                "name": branch.name,
                "root_thought_id": branch.root_thought_id,
                "thought_ids": branch.thought_ids,
                "status": branch.status,
                "depth": branch.depth,
                "branch_score": branch.branch_score
            } for bid, branch in self.branches.items()},
            "current_focus": self.current_focus,
            "attention_stack": self.attention_stack,
            "reasoning_log": self.reasoning_log[-100:]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2) 