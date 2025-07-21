#!/usr/bin/env python3
"""
Постоянный запуск AIbox агента
"""

import asyncio
import signal
import sys
import os
import time
import psutil
import GPUtil
from datetime import datetime
from autonomous_agent import AutonomousAgent

class ForeverAgentRunner:
    """Постоянный запуск агента"""
    
    def __init__(self):
        self.agent = None
        self.running = False
        
    async def start(self):
        """Запустить агента в постоянном режиме"""
        print("🤖 AIbox Forever Agent")
        print("=" * 60)
        
        try:
            # Создать агента
            print("📋 Создание агента...")
            self.agent = AutonomousAgent("Forever AIbox Agent", "agent_data")
            
            # Инициализация модулей
            print("🔧 Инициализация модулей...")
            self.agent.initialize_modules()
            
            # Инициализация агента
            print("🎯 Инициализация агента...")
            self.agent.initialize_agent()
            
            print("✅ Агент успешно инициализирован!")
            
            # Проверить GPU
            await self._check_gpu_usage()
            
            # Запуск цикла сознания
            self.running = True
            print("🧠 Запуск цикла сознания...")
            print("💡 Агент работает в фоновом режиме.")
            print("📊 Мониторинг ресурсов активен.")
            print("🛑 Для остановки нажмите Ctrl+C")
            print("-" * 60)
            
            # Запустить цикл сознания
            await self.agent.run_consciousness_cycle()
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            import traceback
            traceback.print_exc()
    
    async def _check_gpu_usage(self):
        """Проверить использование GPU"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                print("🎮 GPU обнаружена:")
                for i, gpu in enumerate(gpus):
                    print(f"   GPU {i}: {gpu.name}")
                    print(f"   VRAM: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB")
                    print(f"   Загрузка: {gpu.load * 100:.1f}%")
                    print(f"   Температура: {gpu.temperature}°C")
            else:
                print("⚠️ GPU не обнаружена")
        except Exception as e:
            print(f"⚠️ Ошибка проверки GPU: {e}")
    
    def stop(self):
        """Остановить агента"""
        self.running = False
        print("\n🛑 Сигнал остановки отправлен...")
        
        if self.agent:
            self.agent.stop()

async def main():
    """Основная функция"""
    runner = ForeverAgentRunner()
    
    # Обработка сигналов
    def signal_handler(signum, frame):
        print(f"\n📡 Получен сигнал {signum}")
        runner.stop()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await runner.start()
    except KeyboardInterrupt:
        print("\n👋 Завершение работы...")
    finally:
        print("✅ Агент остановлен")

if __name__ == "__main__":
    print("🚀 Запуск AIbox агента в постоянном режиме")
    print("=" * 60)
    
    # Проверить Ollama
    print("🔍 Проверка Ollama...")
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama доступен")
            lines = result.stdout.strip().split('\n')[1:]
            print(f"📋 Доступно моделей: {len([l for l in lines if l.strip()])}")
        else:
            print("❌ Ollama недоступен")
    except Exception as e:
        print(f"❌ Ошибка проверки Ollama: {e}")
    
    print("\n🎯 Запуск агента...")
    asyncio.run(main()) 