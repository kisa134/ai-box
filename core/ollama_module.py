"""
Модуль интеграции с Ollama для AIbox
Поддержка различных моделей для разных типов reasoning
"""

import asyncio
import aiohttp
import json
import logging
import time
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import psutil
import GPUtil

class ModelType(Enum):
    """Типы моделей для разных задач"""
    REASONING = "reasoning"      # Mistral, Mixtral, Llama3
    REFLECTION = "reflection"    # Глубокая рефлексия
    CREATIVE = "creative"        # Творческие задачи
    FAST = "fast"               # Быстрое мышление
    SUBCONSCIOUS = "subconscious" # Mamba, Qwen3
    TESTING = "testing"         # Для тестовых задач

@dataclass
class ModelConfig:
    """Конфигурация модели"""
    name: str
    type: ModelType
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 2048
    context_window: int = 8192
    vram_requirement: int = 0  # GB
    priority: int = 1  # 1-10, где 10 - высший приоритет

@dataclass
class ReasoningRequest:
    """Запрос на reasoning"""
    prompt: str
    model_type: ModelType
    context: Dict[str, Any] = None
    priority: int = 5
    timeout: int = 30
    require_explanation: bool = True

@dataclass
class ReasoningResponse:
    """Ответ от модели"""
    content: str
    model_used: str
    reasoning_chain: List[str]
    confidence: float
    processing_time: float
    vram_used: float
    explanation: Dict[str, Any]

class OllamaClient:
    """Клиент для работы с Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = None
        self.logger = logging.getLogger(__name__)
        self.available_models = {}
        self.model_configs = self._initialize_model_configs()
        
        # Инициализация кэша
        from core.ollama_cache import ollama_cache
        self.ollama_cache = ollama_cache
        
    def _initialize_model_configs(self) -> Dict[str, ModelConfig]:
        """Инициализация конфигураций моделей"""
        return {
            "mistral:latest": ModelConfig(
                name="mistral:latest",
                type=ModelType.REASONING,
                temperature=0.7,
                max_tokens=2048,
                vram_requirement=8,
                priority=8
            ),
            "mixtral:latest": ModelConfig(
                name="mixtral:latest", 
                type=ModelType.REASONING,
                temperature=0.6,
                max_tokens=4096,
                vram_requirement=24,
                priority=9
            ),
            "llama3:latest": ModelConfig(
                name="llama3:latest",
                type=ModelType.REASONING,
                temperature=0.7,
                max_tokens=2048,
                vram_requirement=16,
                priority=7
            ),
            "deepseek-r1:latest": ModelConfig(
                name="deepseek-r1:latest",
                type=ModelType.REASONING,
                temperature=0.6,
                max_tokens=2048,
                vram_requirement=12,
                priority=8
            ),
            "qwen3:latest": ModelConfig(
                name="qwen3:latest",
                type=ModelType.REASONING,
                temperature=0.7,
                max_tokens=2048,
                vram_requirement=12,
                priority=7
            ),
            "Hudson/mamba-chat:latest": ModelConfig(
                name="Hudson/mamba-chat:latest",
                type=ModelType.SUBCONSCIOUS,
                temperature=0.7,
                max_tokens=2048,
                vram_requirement=8,
                priority=6
            )
        }
    
    async def initialize(self):
        """Инициализация клиента"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        await self._discover_models()
    
    async def close(self):
        """Закрыть клиент"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _discover_models(self):
        """Обнаружение доступных моделей"""
        try:
            async with self.session.get(f"{self.base_url}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    for model in data.get("models", []):
                        model_name = model["name"]
                        if model_name in self.model_configs:
                            self.available_models[model_name] = self.model_configs[model_name]
                            self.logger.info(f"✅ Обнаружена модель: {model_name}")
                        else:
                            self.logger.warning(f"⚠️ Неизвестная модель: {model_name}")
                else:
                    self.logger.error(f"Ошибка получения списка моделей: {response.status}")
        except Exception as e:
            self.logger.error(f"Ошибка инициализации Ollama: {e}")
    
    async def generate_response(self, 
                              prompt: str, 
                              model_name: str,
                              temperature: float = None,
                              max_tokens: int = None,
                              system_prompt: str = None) -> Dict[str, Any]:
        
        # Проверить кэш
        cache_key = f"{prompt}_{model_name}_{temperature}_{max_tokens}"
        cached_result = self.ollama_cache.get(prompt, model_name, {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "system_prompt": system_prompt
        })
        
        if cached_result:
            self.logger.info(f"Кэш hit для {model_name}")
            return {
                "success": True,
                "content": cached_result.content,
                "model": cached_result.model_used,
                "processing_time": cached_result.processing_time,
                "tokens_used": cached_result.tokens_used,
                "confidence": cached_result.confidence,
                "cached": True
            }
        
        # Генерация ответа через Ollama
        if not self.session:
            await self.initialize()
        
        config = self.model_configs.get(model_name)
        if not config:
            raise ValueError(f"Неизвестная модель: {model_name}")
        
        # Подготовка запроса
        request_data = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature or config.temperature,
                "top_p": config.top_p,
                "num_predict": max_tokens or config.max_tokens
            }
        }
        
        if system_prompt:
            request_data["system"] = system_prompt
        
        start_time = time.time()
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/generate",
                json=request_data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    processing_time = time.time() - start_time
                    
                    result = {
                        "content": data.get("response", ""),
                        "model": model_name,
                        "processing_time": processing_time,
                        "tokens_used": data.get("eval_count", 0),
                        "success": True
                    }
                    
                    # Сохранить в кэш
                    self.ollama_cache.set(
                        prompt=prompt,
                        model=model_name,
                        content=result["content"],
                        processing_time=processing_time,
                        tokens_used=data.get("eval_count", 0),
                        confidence=0.8,  # Placeholder
                        context={
                            "temperature": temperature,
                            "max_tokens": max_tokens,
                            "system_prompt": system_prompt
                        }
                    )
                    
                    return result
                else:
                    error_text = await response.text()
                    self.logger.error(f"Ошибка генерации: {response.status} - {error_text}")
                    return {
                        "content": f"Ошибка генерации: {error_text}",
                        "model": model_name,
                        "processing_time": time.time() - start_time,
                        "success": False
                    }
                    
        except Exception as e:
            self.logger.error(f"Ошибка запроса к Ollama: {e}")
            return {
                "content": f"Ошибка подключения к Ollama: {e}",
                "model": model_name,
                "processing_time": time.time() - start_time,
                "success": False
            }

class ResourceMonitor:
    """Мониторинг ресурсов системы"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_system_resources(self) -> Dict[str, float]:
        """Получить информацию о ресурсах системы"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # RAM
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            ram_available = memory.available / (1024**3)  # GB
            
            # GPU
            gpu_info = {}
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]  # Основная GPU
                    gpu_info = {
                        "gpu_name": gpu.name,
                        "gpu_load": gpu.load * 100,
                        "gpu_memory_percent": gpu.memoryUtil * 100,
                        "gpu_memory_available": gpu.memoryFree / 1024,  # GB
                        "gpu_memory_total": gpu.memoryTotal / 1024  # GB
                    }
            except Exception as e:
                self.logger.warning(f"Не удалось получить информацию о GPU: {e}")
            
            return {
                "cpu_percent": cpu_percent,
                "ram_percent": ram_percent,
                "ram_available_gb": ram_available,
                "gpu": gpu_info
            }
        except Exception as e:
            self.logger.error(f"Ошибка мониторинга ресурсов: {e}")
            return {}
    
    def can_load_model(self, vram_requirement: float) -> bool:
        """Проверить, можно ли загрузить модель"""
        resources = self.get_system_resources()
        gpu_info = resources.get("gpu", {})
        
        if not gpu_info:
            return True  # Если GPU нет, считаем что можно
        
        available_vram = gpu_info.get("gpu_memory_available", 0)
        return available_vram >= vram_requirement

class ReasoningOrchestrator:
    """Оркестратор reasoning с переключением моделей"""
    
    def __init__(self):
        self.ollama_client = OllamaClient()
        self.resource_monitor = ResourceMonitor()
        self.logger = logging.getLogger(__name__)
        self.reasoning_queue = asyncio.Queue()
        self.active_requests = {}
        
    async def initialize(self):
        """Инициализация оркестратора"""
        await self.ollama_client.initialize()
        self.logger.info("✅ ReasoningOrchestrator инициализирован")
    
    async def submit_reasoning_request(self, request: ReasoningRequest) -> str:
        """Отправить запрос на reasoning"""
        request_id = f"req_{int(time.time() * 1000)}"
        self.active_requests[request_id] = request
        await self.reasoning_queue.put((request_id, request))
        return request_id
    
    async def get_reasoning_response(self, request_id: str) -> Optional[ReasoningResponse]:
        """Получить результат reasoning"""
        if request_id in self.active_requests:
            request = self.active_requests[request_id]
            return await self._process_reasoning_request(request)
        return None
    
    async def _process_reasoning_request(self, request: ReasoningRequest) -> ReasoningResponse:
        """Обработать запрос reasoning"""
        
        # Выбор подходящей модели
        model_name = await self._select_model_for_request(request)
        
        # Подготовка промпта
        system_prompt = self._build_system_prompt(request.model_type, request.context)
        full_prompt = self._build_reasoning_prompt(request.prompt, request.model_type)
        
        # Генерация ответа
        start_time = time.time()
        result = await self.ollama_client.generate_response(
            prompt=full_prompt,
            model_name=model_name,
            system_prompt=system_prompt,
            temperature=0.7 if request.model_type == ModelType.CREATIVE else 0.6
        )
        
        processing_time = time.time() - start_time
        
        # Извлечение reasoning chain
        reasoning_chain = self._extract_reasoning_chain(result["content"])
        
        # Формирование объяснения
        explanation = {
            "model_used": model_name,
            "model_type": request.model_type.value,
            "reasoning_chain": reasoning_chain,
            "processing_time": processing_time,
            "tokens_used": result.get("tokens_used", 0),
            "system_resources": self.resource_monitor.get_system_resources(),
            "request_context": request.context
        }
        
        return ReasoningResponse(
            content=result["content"],
            model_used=model_name,
            reasoning_chain=reasoning_chain,
            confidence=self._calculate_confidence(result["content"]),
            processing_time=processing_time,
            vram_used=self._get_vram_usage(),
            explanation=explanation
        )
    
    async def _select_model_for_request(self, request: ReasoningRequest) -> str:
        """Выбрать подходящую модель для запроса"""
        
        # Получить доступные модели для данного типа
        available_models = [
            name for name, config in self.ollama_client.model_configs.items()
            if config.type == request.model_type and name in self.ollama_client.available_models
        ]
        
        if not available_models:
            # Fallback на любую доступную модель
            available_models = list(self.ollama_client.available_models.keys())
        
        # Выбрать модель с учетом ресурсов и приоритета
        for model_name in available_models:
            config = self.ollama_client.model_configs[model_name]
            if self.resource_monitor.can_load_model(config.vram_requirement):
                return model_name
        
        # Если ничего не подходит, вернуть первую доступную
        return available_models[0] if available_models else "Hudson/mamba-chat:latest"
    
    def _build_system_prompt(self, model_type: ModelType, context: Dict[str, Any] = None) -> str:
        """Построить системный промпт"""
        
        base_prompts = {
            ModelType.REASONING: """Ты - модуль логического мышления AIbox агента. 
Твоя задача - анализировать информацию, строить логические цепочки и принимать обоснованные решения.
Всегда объясняй свои рассуждения пошагово.""",
            
            ModelType.REFLECTION: """Ты - модуль глубокой рефлексии AIbox агента.
Твоя задача - анализировать собственные мысли, эмоции и поведение.
Будь честным и глубоким в самоанализе.""",
            
            ModelType.CREATIVE: """Ты - модуль творческого мышления AIbox агента.
Твоя задача - генерировать оригинальные идеи, создавать истории и находить нестандартные решения.
Будь креативным и вдохновляющим.""",
            
            ModelType.FAST: """Ты - модуль быстрого мышления AIbox агента.
Твоя задача - быстро анализировать ситуации и давать краткие, но точные ответы.
Будь эффективным и лаконичным.""",
            
            ModelType.SUBCONSCIOUS: """Ты - модуль подсознания AIbox агента.
Твоя задача - обрабатывать фоновые мысли, интуитивные ощущения и глубинные паттерны.
Действуй интуитивно и образно."""
        }
        
        prompt = base_prompts.get(model_type, base_prompts[ModelType.REASONING])
        
        if context:
            if 'emotional_state' in context:
                prompt += f"\nТвое эмоциональное состояние: {context['emotional_state']}"
            if 'current_goal' in context:
                prompt += f"\nТвоя текущая цель: {context['current_goal']}"
        
        return prompt
    
    def _build_reasoning_prompt(self, user_prompt: str, model_type: ModelType) -> str:
        """Построить промпт для reasoning"""
        
        if model_type == ModelType.REASONING:
            return f"""Проанализируй следующий запрос и дай обоснованный ответ:

ЗАПРОС: {user_prompt}

РАССУЖДЕНИЕ:
1. Сначала определи суть вопроса
2. Проанализируй возможные подходы
3. Выбери наиболее логичное решение
4. Объясни свои рассуждения

ОТВЕТ:"""
        
        elif model_type == ModelType.REFLECTION:
            return f"""Проведи глубокую рефлексию по поводу:

{user_prompt}

РЕФЛЕКСИЯ:
1. Что я чувствую по этому поводу?
2. Какие мысли это вызывает?
3. Что это говорит обо мне?
4. Как это влияет на мое понимание себя?

РАЗМЫШЛЕНИЯ:"""
        
        elif model_type == ModelType.CREATIVE:
            return f"""Создай что-то творческое на основе:

{user_prompt}

ТВОРЧЕСКИЙ ПРОЦЕСС:
1. Вдохновись идеей
2. Развивай оригинальные мысли
3. Создавай неожиданные связи
4. Выражай креативно

РЕЗУЛЬТАТ:"""
        
        else:
            return user_prompt
    
    def _extract_reasoning_chain(self, content: str) -> List[str]:
        """Извлечь цепочку рассуждений из ответа"""
        reasoning_steps = []
        
        # Ищем маркеры reasoning в тексте
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.')) or \
               line.startswith(('РАССУЖДЕНИЕ:', 'РЕФЛЕКСИЯ:', 'ТВОРЧЕСКИЙ ПРОЦЕСС:')):
                reasoning_steps.append(line)
        
        return reasoning_steps if reasoning_steps else [content[:200] + "..."]
    
    def _calculate_confidence(self, content: str) -> float:
        """Рассчитать уверенность в ответе"""
        # Простая эвристика на основе длины и структуры ответа
        if len(content) < 50:
            return 0.3
        elif len(content) > 500:
            return 0.9
        else:
            return 0.6
    
    def _get_vram_usage(self) -> float:
        """Получить использование VRAM"""
        resources = self.resource_monitor.get_system_resources()
        gpu_info = resources.get("gpu", {})
        return gpu_info.get("gpu_memory_percent", 0) / 100

class ExplainabilityLogger:
    """Логгер для explainability"""
    
    def __init__(self, log_file: str = "reasoning_logs.jsonl"):
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
    
    def log_reasoning_request(self, request: ReasoningRequest, response: ReasoningResponse):
        """Залогировать reasoning запрос"""
        log_entry = {
            "timestamp": time.time(),
            "request": {
                "prompt": request.prompt,
                "model_type": request.model_type.value,
                "priority": request.priority,
                "context": request.context
            },
            "response": {
                "content": response.content,
                "model_used": response.model_used,
                "reasoning_chain": response.reasoning_chain,
                "confidence": response.confidence,
                "processing_time": response.processing_time,
                "vram_used": response.vram_used,
                "explanation": response.explanation
            }
        }
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            self.logger.error(f"Ошибка логирования: {e}")
    
    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Получить последние логи"""
        logs = []
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if len(logs) >= limit:
                        break
                    logs.append(json.loads(line.strip()))
        except FileNotFoundError:
            pass
        except Exception as e:
            self.logger.error(f"Ошибка чтения логов: {e}")
        
        return logs 