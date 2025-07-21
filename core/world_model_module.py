from typing import Dict, Any, List, Optional, Set
from datetime import datetime
import json
import uuid

class Entity:
    """Сущность в модели мира"""
    
    def __init__(self, entity_id: str, entity_type: str, name: str):
        self.id = entity_id
        self.type = entity_type
        self.name = name
        self.properties: Dict[str, Any] = {}
        self.relationships: Dict[str, List[str]] = {}  # тип связи -> список ID сущностей
        self.last_updated = datetime.now()
        self.confidence = 1.0  # уверенность в информации
        self.source = "unknown"
        
    def update_property(self, key: str, value: Any, confidence: float = 1.0):
        """Обновить свойство сущности"""
        self.properties[key] = {
            "value": value,
            "confidence": confidence,
            "last_updated": datetime.now().isoformat()
        }
        self.last_updated = datetime.now()
    
    def add_relationship(self, relation_type: str, target_id: str):
        """Добавить связь с другой сущностью"""
        if relation_type not in self.relationships:
            self.relationships[relation_type] = []
        if target_id not in self.relationships[relation_type]:
            self.relationships[relation_type].append(target_id)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "properties": self.properties,
            "relationships": self.relationships,
            "last_updated": self.last_updated.isoformat(),
            "confidence": self.confidence,
            "source": self.source
        }

class Fact:
    """Факт о мире"""
    
    def __init__(self, statement: str, confidence: float = 1.0, source: str = "observation"):
        self.id = str(uuid.uuid4())
        self.statement = statement
        self.confidence = confidence
        self.source = source
        self.timestamp = datetime.now()
        self.verified = False
        self.contradictions: List[str] = []  # ID фактов, которые противоречат этому
        self.supports: List[str] = []  # ID фактов, которые поддерживают этот
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "statement": self.statement,
            "confidence": self.confidence,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "verified": self.verified,
            "contradictions": self.contradictions,
            "supports": self.supports
        }

class Context:
    """Контекст ситуации"""
    
    def __init__(self, name: str, description: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.active_entities: Set[str] = set()
        self.relevant_facts: Set[str] = set()
        self.state_variables: Dict[str, Any] = {}
        self.timestamp = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "active_entities": list(self.active_entities),
            "relevant_facts": list(self.relevant_facts),
            "state_variables": self.state_variables,
            "timestamp": self.timestamp.isoformat()
        }

class WorldModelModule:
    """
    Модуль восприятия: обработка API/контекста/сенсоров,
    обновление внутренней модели мира
    """
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.facts: Dict[str, Fact] = {}
        self.contexts: Dict[str, Context] = {}
        self.current_context_id: Optional[str] = None
        self.world_state: Dict[str, Any] = {}
        self.perception_log: List[Dict[str, Any]] = []
        self.uncertainty_threshold = 0.3
        self.knowledge_graph: Dict[str, Any] = {} # Новый атрибут для динамического обучения
        self.update_history: List[Dict[str, Any]] = [] # Новый атрибут для истории обновлений
        
    def add_entity(self, 
                   entity_type: str, 
                   name: str, 
                   properties: Optional[Dict[str, Any]] = None,
                   source: str = "observation") -> str:
        """Добавить сущность в модель мира"""
        entity_id = str(uuid.uuid4())
        entity = Entity(entity_id, entity_type, name)
        entity.source = source
        
        if properties:
            for key, value in properties.items():
                entity.update_property(key, value)
                
        self.entities[entity_id] = entity
        
        # Добавить в текущий контекст
        if self.current_context_id and self.current_context_id in self.contexts:
            self.contexts[self.current_context_id].active_entities.add(entity_id)
            
        self._log_perception("entity_added", {
            "entity_id": entity_id,
            "type": entity_type,
            "name": name,
            "source": source
        })
        
        return entity_id
    
    def update_entity(self, 
                     entity_id: str, 
                     properties: Dict[str, Any],
                     confidence: float = 1.0):
        """Обновить свойства сущности"""
        if entity_id in self.entities:
            entity = self.entities[entity_id]
            for key, value in properties.items():
                entity.update_property(key, value, confidence)
                
            self._log_perception("entity_updated", {
                "entity_id": entity_id,
                "properties": properties,
                "confidence": confidence
            })
    
    def add_fact(self, 
                statement: str, 
                confidence: float = 1.0,
                source: str = "observation",
                entity_ids: Optional[List[str]] = None) -> str:
        """Добавить факт о мире"""
        fact = Fact(statement, confidence, source)
        
        # Проверить противоречия с существующими фактами
        self._check_fact_consistency(fact)
        
        self.facts[fact.id] = fact
        
        # Связать с сущностями
        if entity_ids:
            for entity_id in entity_ids:
                if entity_id in self.entities:
                    self.entities[entity_id].add_relationship("related_fact", fact.id)
                    
        # Добавить в текущий контекст
        if self.current_context_id and self.current_context_id in self.contexts:
            self.contexts[self.current_context_id].relevant_facts.add(fact.id)
            
        self._log_perception("fact_added", {
            "fact_id": fact.id,
            "statement": statement,
            "confidence": confidence,
            "source": source
        })
        
        return fact.id
    
    def create_context(self, name: str, description: str) -> str:
        """Создать новый контекст"""
        context = Context(name, description)
        self.contexts[context.id] = context
        
        self._log_perception("context_created", {
            "context_id": context.id,
            "name": name,
            "description": description
        })
        
        return context.id
    
    def switch_context(self, context_id: str):
        """Переключиться на другой контекст"""
        if context_id in self.contexts:
            self.current_context_id = context_id
            
            self._log_perception("context_switched", {
                "new_context_id": context_id,
                "context_name": self.contexts[context_id].name
            })
    
    def process_api_data(self, api_name: str, data: Dict[str, Any]) -> List[str]:
        """Обработать данные из API"""
        processed_entities = []
        
        # Простая логика извлечения информации из API данных
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and "id" in value:
                    # Похоже на объект с ID
                    entity_id = self.add_entity(
                        entity_type=key,
                        name=value.get("name", f"{key}_{value['id']}"),
                        properties=value,
                        source=f"api:{api_name}"
                    )
                    processed_entities.append(entity_id)
                    
                elif isinstance(value, str) and len(value) > 10:
                    # Потенциально важная текстовая информация
                    fact_id = self.add_fact(
                        statement=f"{key}: {value}",
                        source=f"api:{api_name}"
                    )
                    
        self._log_perception("api_processed", {
            "api_name": api_name,
            "entities_created": len(processed_entities),
            "data_size": len(str(data))
        })
        
        return processed_entities
    
    def process_user_input(self, user_input: str) -> List[str]:
        """Обработать ввод пользователя"""
        # Извлечение информации из пользовательского ввода
        extracted_info = []
        
        # Простой парсинг - в реальном агенте здесь был бы NLP
        words = user_input.lower().split()
        
        # Поиск упоминаний сущностей
        for entity_id, entity in self.entities.items():
            if entity.name.lower() in user_input.lower():
                extracted_info.append(f"Упомянута сущность: {entity.name}")
                
        # Создать факт о пользовательском вводе
        fact_id = self.add_fact(
            statement=f"Пользователь сказал: {user_input}",
            source="user_input"
        )
        
        self._log_perception("user_input_processed", {
            "input": user_input,
            "extracted_info": extracted_info,
            "fact_id": fact_id
        })
        
        return extracted_info
    
    def get_relevant_entities(self, query: str, limit: int = 10) -> List[Entity]:
        """Найти релевантные сущности по запросу"""
        relevant = []
        query_lower = query.lower()
        
        for entity in self.entities.values():
            score = 0
            
            # Проверить имя
            if query_lower in entity.name.lower():
                score += 10
                
            # Проверить свойства
            for prop_key, prop_data in entity.properties.items():
                if isinstance(prop_data, dict) and "value" in prop_data:
                    prop_value = str(prop_data["value"]).lower()
                    if query_lower in prop_value or query_lower in prop_key.lower():
                        score += 5
                        
            if score > 0:
                relevant.append((entity, score))
                
        # Сортировать по релевантности
        relevant.sort(key=lambda x: x[1], reverse=True)
        
        return [entity for entity, score in relevant[:limit]]
    
    def get_world_summary(self) -> str:
        """Получить краткое описание модели мира"""
        summary = f"""
=== МОДЕЛЬ МИРА ===
Сущности: {len(self.entities)}
Факты: {len(self.facts)}
Контексты: {len(self.contexts)}
Текущий контекст: {self.contexts[self.current_context_id].name if self.current_context_id else 'Не установлен'}

Типы сущностей:
"""
        
        # Группировка сущностей по типам
        entity_types = {}
        for entity in self.entities.values():
            entity_types[entity.type] = entity_types.get(entity.type, 0) + 1
            
        for entity_type, count in entity_types.items():
            summary += f"- {entity_type}: {count}\n"
            
        # Недавние факты
        recent_facts = sorted(self.facts.values(), 
                            key=lambda x: x.timestamp, 
                            reverse=True)[:3]
        
        if recent_facts:
            summary += "\nНедавние факты:\n"
            for fact in recent_facts:
                summary += f"- {fact.statement} (уверенность: {fact.confidence:.2f})\n"
                
        return summary.strip()
    
    def _check_fact_consistency(self, new_fact: Fact):
        """Проверить согласованность нового факта с существующими"""
        # Простая проверка - в реальной системе была бы более сложная логика
        for existing_fact in self.facts.values():
            similarity = self._calculate_fact_similarity(new_fact.statement, existing_fact.statement)
            
            if similarity > 0.8 and new_fact.confidence != existing_fact.confidence:
                # Потенциальное противоречие
                if abs(new_fact.confidence - existing_fact.confidence) > 0.5:
                    new_fact.contradictions.append(existing_fact.id)
                    existing_fact.contradictions.append(new_fact.id)
    
    def _calculate_fact_similarity(self, statement1: str, statement2: str) -> float:
        """Вычислить сходство между утверждениями"""
        # Простая метрика на основе общих слов
        words1 = set(statement1.lower().split())
        words2 = set(statement2.lower().split())
        
        if len(words1) == 0 or len(words2) == 0:
            return 0.0
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _log_perception(self, action: str, data: Dict[str, Any]):
        """Записать событие восприятия в лог"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "data": data
        }
        
        self.perception_log.append(log_entry)
        
        # Ограничить размер лога
        if len(self.perception_log) > 1000:
            self.perception_log = self.perception_log[-1000:]
    
    def save_to_file(self, filepath: str):
        """Сохранить модель мира в файл"""
        data = {
            "entities": {eid: entity.to_dict() for eid, entity in self.entities.items()},
            "facts": {fid: fact.to_dict() for fid, fact in self.facts.items()},
            "contexts": {cid: context.to_dict() for cid, context in self.contexts.items()},
            "current_context_id": self.current_context_id,
            "world_state": self.world_state,
            "perception_log": self.perception_log[-100:]  # Сохранить последние 100 записей
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2) 

    def update_knowledge(self, new_information: str, source: str = "interaction", confidence: float = 0.8):
        """Обновить знания о мире с динамическим обучением"""
        
        # Анализ новой информации
        extracted_concepts = self._extract_concepts(new_information)
        relationships = self._find_relationships(extracted_concepts)
        
        # Динамическое обновление знаний
        for concept in extracted_concepts:
            if concept not in self.knowledge_graph:
                # Новое понятие
                self.knowledge_graph[concept] = {
                    "definition": self._generate_definition(concept, new_information),
                    "relationships": {},
                    "confidence": confidence,
                    "sources": [source],
                    "last_updated": datetime.now().isoformat(),
                    "usage_count": 1
                }
            else:
                # Обновление существующего понятия
                existing = self.knowledge_graph[concept]
                existing["confidence"] = min(1.0, existing["confidence"] + 0.1)
                existing["sources"].append(source)
                existing["last_updated"] = datetime.now().isoformat()
                existing["usage_count"] += 1
                
                # Обновление определения если новая информация более свежая
                if confidence > existing["confidence"]:
                    existing["definition"] = self._generate_definition(concept, new_information)
        
        # Обновление связей
        for rel in relationships:
            source_concept, target_concept, relationship_type = rel
            if source_concept in self.knowledge_graph and target_concept in self.knowledge_graph:
                if "relationships" not in self.knowledge_graph[source_concept]:
                    self.knowledge_graph[source_concept]["relationships"] = {}
                
                self.knowledge_graph[source_concept]["relationships"][target_concept] = {
                    "type": relationship_type,
                    "confidence": confidence,
                    "last_updated": datetime.now().isoformat()
                }
        
        # Логирование обновления
        self._log_knowledge_update(new_information, source, confidence)
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Извлечение концепций из текста"""
        # Простое извлечение существительных и ключевых слов
        words = text.lower().split()
        concepts = []
        
        # Фильтрация стоп-слов и извлечение концепций
        stop_words = {"и", "в", "на", "с", "по", "для", "от", "до", "из", "к", "у", "о", "об", "а", "но", "или", "что", "как", "где", "когда", "почему"}
        
        for word in words:
            if len(word) > 3 and word not in stop_words:
                # Простая эвристика для определения концепций
                if word.endswith(('ость', 'ние', 'ство', 'изм', 'ция')):
                    concepts.append(word)
                elif word in ['сознание', 'искусственный', 'интеллект', 'обучение', 'память', 'мышление']:
                    concepts.append(word)
        
        return list(set(concepts))
    
    def _find_relationships(self, concepts: List[str]) -> List[tuple]:
        """Поиск связей между концепциями"""
        relationships = []
        
        # Простые эвристики для определения связей
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i+1:]:
                if concept1 != concept2:
                    # Определение типа связи
                    relationship_type = self._determine_relationship_type(concept1, concept2)
                    if relationship_type:
                        relationships.append((concept1, concept2, relationship_type))
        
        return relationships
    
    def _determine_relationship_type(self, concept1: str, concept2: str) -> str:
        """Определение типа связи между концепциями"""
        # Простые эвристики
        if 'сознание' in concept1 and 'искусственный' in concept2:
            return "is_a"
        elif 'обучение' in concept1 and 'память' in concept2:
            return "requires"
        elif 'мышление' in concept1 and 'логика' in concept2:
            return "uses"
        else:
            return "related_to"
    
    def _generate_definition(self, concept: str, context: str) -> str:
        """Генерация определения концепции"""
        # Простые определения на основе контекста
        definitions = {
            "сознание": "Способность осознавать себя и окружающий мир",
            "искусственный": "Созданный человеком, не природный",
            "интеллект": "Способность к мышлению и решению задач",
            "обучение": "Процесс приобретения знаний и навыков",
            "память": "Способность хранить и воспроизводить информацию",
            "мышление": "Процесс обработки информации и решения задач"
        }
        
        return definitions.get(concept, f"Концепция: {concept}")
    
    def _log_knowledge_update(self, information: str, source: str, confidence: float):
        """Логирование обновления знаний"""
        self.update_history.append({
            "timestamp": datetime.now().isoformat(),
            "information": information[:100] + "..." if len(information) > 100 else information,
            "source": source,
            "confidence": confidence
        })
    
    def learn_from_interaction(self, user_input: str, agent_response: str, outcome: str):
        """Обучение на основе взаимодействия"""
        
        # Анализ успешности взаимодействия
        success_score = self._evaluate_interaction_success(user_input, agent_response, outcome)
        
        # Обновление знаний на основе результата
        self.update_knowledge(
            f"Взаимодействие: {user_input} -> {agent_response} -> {outcome}",
            source="interaction",
            confidence=success_score
        )
        
        # Обновление стратегий взаимодействия
        self._update_interaction_strategies(user_input, agent_response, success_score)
    
    def _evaluate_interaction_success(self, user_input: str, agent_response: str, outcome: str) -> float:
        """Оценка успешности взаимодействия"""
        success_score = 0.5  # Базовый уровень
        
        # Простые эвристики для оценки
        if "спасибо" in outcome.lower() or "хорошо" in outcome.lower():
            success_score += 0.3
        elif "неправильно" in outcome.lower() or "ошибка" in outcome.lower():
            success_score -= 0.3
        
        if len(agent_response) > 50:  # Подробный ответ
            success_score += 0.1
        
        return max(0.0, min(1.0, success_score))
    
    def _update_interaction_strategies(self, user_input: str, agent_response: str, success_score: float):
        """Обновление стратегий взаимодействия"""
        # Анализ паттернов успешных взаимодействий
        if success_score > 0.7:
            # Успешное взаимодействие - запомнить паттерн
            pattern = {
                "input_type": self._classify_input_type(user_input),
                "response_style": self._classify_response_style(agent_response),
                "success_score": success_score
            }
            
            if "successful_patterns" not in self.knowledge_graph:
                self.knowledge_graph["successful_patterns"] = []
            
            self.knowledge_graph["successful_patterns"].append(pattern)
    
    def _classify_input_type(self, user_input: str) -> str:
        """Классификация типа ввода пользователя"""
        input_lower = user_input.lower()
        
        if "?" in user_input:
            return "question"
        elif any(word in input_lower for word in ["сделай", "создай", "напиши"]):
            return "request"
        elif any(word in input_lower for word in ["объясни", "расскажи", "что такое"]):
            return "explanation_request"
        else:
            return "statement"
    
    def _classify_response_style(self, response: str) -> str:
        """Классификация стиля ответа"""
        if len(response) > 200:
            return "detailed"
        elif len(response) > 50:
            return "moderate"
        else:
            return "concise" 