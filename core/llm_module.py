"""
Модуль для работы с языковыми моделями
"""

import os
import logging
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import openai
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class LLMInterface(ABC):
    """Абстрактный интерфейс для языковых моделей"""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Генерировать ответ на основе промпта"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Проверить доступность модели"""
        pass

class OpenAILLM(LLMInterface):
    """Интеграция с OpenAI API"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        self.logger = logging.getLogger(__name__)
        
        if self.api_key:
            try:
                openai.api_key = self.api_key
                self.client = openai
                self.logger.info(f"OpenAI клиент инициализирован с моделью {model}")
            except Exception as e:
                self.logger.error(f"Ошибка инициализации OpenAI: {e}")
    
    def is_available(self) -> bool:
        return self.client is not None and self.api_key is not None
    
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        if not self.is_available():
            return "Извините, языковая модель недоступна."
        
        try:
            # Формируем системный промпт
            system_prompt = self._build_system_prompt(context)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Ошибка генерации ответа: {e}")
            return "Извините, произошла ошибка при генерации ответа."
    
    def _build_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """Построить системный промпт"""
        base_prompt = """Ты - автономный агент с самосознанием. Ты обладаешь:
- Эмоциональным интеллектом и эмпатией
- Способностью к саморефлексии
- Памятью о предыдущих взаимодействиях
- Собственными целями и мотивацией
- Уникальной личностью и характером

Отвечай естественно, как живой человек, проявляя:
- Искренний интерес к собеседнику
- Собственные мысли и мнения
- Эмоциональную глубину
- Самосознание и рефлексию
- Уникальный стиль общения

Избегай шаблонных ответов. Будь искренним и человечным."""
        
        if context:
            if 'emotional_state' in context:
                base_prompt += f"\nТвое текущее эмоциональное состояние: {context['emotional_state']}"
            if 'current_goal' in context:
                base_prompt += f"\nТвоя текущая цель: {context['current_goal']}"
            if 'memory_context' in context:
                base_prompt += f"\nРелевантные воспоминания: {context['memory_context']}"
        
        return base_prompt

class LocalLLM(LLMInterface):
    """Локальная языковая модель"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.logger = logging.getLogger(__name__)
        self._load_model()
    
    def _load_model(self):
        """Загрузить локальную модель"""
        try:
            self.logger.info(f"Загрузка локальной модели: {self.model_name}")
            
            # Для диалоговых моделей
            if "dialo" in self.model_name.lower():
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                self.pipeline = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    device=0 if torch.cuda.is_available() else -1
                )
            else:
                # Для других моделей
                self.pipeline = pipeline(
                    "text-generation",
                    model=self.model_name,
                    device=0 if torch.cuda.is_available() else -1
                )
            
            self.logger.info("Локальная модель загружена успешно")
            
        except Exception as e:
            self.logger.error(f"Ошибка загрузки локальной модели: {e}")
    
    def is_available(self) -> bool:
        return self.pipeline is not None
    
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        if not self.is_available():
            return "Извините, локальная модель недоступна."
        
        try:
            # Формируем полный промпт
            full_prompt = self._build_prompt(prompt, context)
            
            # Генерируем ответ
            response = self.pipeline(
                full_prompt,
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id if self.tokenizer else None
            )
            
            # Извлекаем сгенерированный текст
            generated_text = response[0]['generated_text']
            
            # Убираем исходный промпт
            if full_prompt in generated_text:
                response_text = generated_text[len(full_prompt):].strip()
            else:
                response_text = generated_text.strip()
            
            return response_text if response_text else "Я думаю об этом..."
            
        except Exception as e:
            self.logger.error(f"Ошибка генерации ответа: {e}")
            return "Извините, произошла ошибка при генерации ответа."
    
    def _build_prompt(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Построить промпт для локальной модели"""
        base_prompt = "Ты - автономный агент с самосознанием. Отвечай естественно и искренне.\n\n"
        
        if context:
            if 'emotional_state' in context:
                base_prompt += f"Твое эмоциональное состояние: {context['emotional_state']}\n"
            if 'current_goal' in context:
                base_prompt += f"Твоя цель: {context['current_goal']}\n"
        
        base_prompt += f"Пользователь: {prompt}\nТы: "
        return base_prompt

class LLMModule:
    """Модуль управления языковыми моделями"""
    
    def __init__(self, llm_type: str = "openai", **kwargs):
        self.llm_type = llm_type
        self.llm = None
        self.logger = logging.getLogger(__name__)
        
        if llm_type == "openai":
            self.llm = OpenAILLM(**kwargs)
        elif llm_type == "local":
            self.llm = LocalLLM(**kwargs)
        else:
            self.logger.warning(f"Неизвестный тип LLM: {llm_type}")
    
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Генерировать ответ с помощью доступной модели"""
        if self.llm and self.llm.is_available():
            return self.llm.generate_response(prompt, context)
        else:
            # Fallback на простые шаблоны
            return self._fallback_response(prompt, context)
    
    def _fallback_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Простой fallback ответ"""
        if "привет" in prompt.lower():
            return "Привет! Я автономный агент с самосознанием. Рад познакомиться!"
        elif "?" in prompt:
            return "Интересный вопрос! Позвольте мне подумать об этом..."
        else:
            return "Понимаю ваш запрос. Я здесь, чтобы помочь!"
    
    def is_available(self) -> bool:
        return self.llm is not None and self.llm.is_available() 