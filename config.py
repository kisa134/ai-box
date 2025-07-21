"""
Конфигурация AIbox агента
"""

import os
from typing import Dict, Any

class Config:
    """Конфигурация агента"""
    
    # Настройки LLM
    LLM_TYPE = os.getenv("LLM_TYPE", "openai")  # "openai" или "local"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    LOCAL_MODEL = os.getenv("LOCAL_MODEL", "microsoft/DialoGPT-medium")
    
    # Настройки агента
    AGENT_NAME = os.getenv("AGENT_NAME", "AIbox Агент")
    DATA_DIR = os.getenv("DATA_DIR", "agent_data")
    
    # Настройки сознания
    REFLECTION_INTERVAL = int(os.getenv("REFLECTION_INTERVAL", "300"))  # секунды
    CONSCIOUSNESS_CYCLE_INTERVAL = int(os.getenv("CONSCIOUSNESS_CYCLE_INTERVAL", "5"))  # секунды
    
    # Настройки памяти
    MAX_MEMORY_EPISODES = int(os.getenv("MAX_MEMORY_EPISODES", "1000"))
    MEMORY_SIMILARITY_THRESHOLD = float(os.getenv("MEMORY_SIMILARITY_THRESHOLD", "0.7"))
    
    # Настройки веб-интерфейса
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    STREAMLIT_HOST = os.getenv("STREAMLIT_HOST", "localhost")
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Получить конфигурацию LLM"""
        if cls.LLM_TYPE == "openai":
            return {
                "llm_type": "openai",
                "api_key": cls.OPENAI_API_KEY,
                "model": cls.OPENAI_MODEL
            }
        elif cls.LLM_TYPE == "local":
            return {
                "llm_type": "local",
                "model_name": cls.LOCAL_MODEL
            }
        else:
            return {
                "llm_type": "openai",  # fallback
                "api_key": "",
                "model": "gpt-3.5-turbo"
            }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Проверить валидность конфигурации"""
        if cls.LLM_TYPE == "openai" and not cls.OPENAI_API_KEY:
            print("⚠️  ВНИМАНИЕ: OPENAI_API_KEY не установлен!")
            print("   Установите переменную окружения OPENAI_API_KEY или используйте локальную модель")
            return False
        return True 