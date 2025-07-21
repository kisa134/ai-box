#!/usr/bin/env python3
"""
Постоянный запуск AIbox агента в фоновом режиме
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

class PersistentAgentRunner:
    """Постоянный запуск агента"""
    
    def __init__(self):
        self.agent = None
        self.running = False
        self.consciousness_task = None
        self.monitoring_task = None
        
    async def start(self):
        """Запустить агента в постоянном режиме"""
        print("🤖 AIbox Persistent Agent")
        print("=" * 60)
        
        try:
            # Создать агента
            print("📋 Создание агента...")
            self.agent = AutonomousAgent("Persistent AIbox Agent", "agent_data")
            
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
            
            # Запустить задачи
            self.consciousness_task = asyncio.create_task(
                self.agent.run_consciousness_cycle()
            )
            
            self.monitoring_task = asyncio.create_task(
                self._monitor_system()
            )
            
            # Ожидание завершения
            await asyncio.gather(
                self.consciousness_task,
                self.monitoring_task,
                return_exceptions=True
            )
            
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
    
    async def _monitor_system(self):
        """Мониторинг системы"""
        cycle_count = 0
        
        while self.running:
            try:
                # Получить статус агента
                status = self.agent.get_status_report()
                
                # Получить ресурсы системы
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                # GPU информация
                gpu_info = ""
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu = gpus[0]
                        gpu_info = f"GPU: {gpu.memoryUsed}MB/{gpu.memoryTotal}MB ({gpu.load*100:.1f}%)"
                except:
                    gpu_info = "GPU: недоступно"
                
                # Вывести статус
                timestamp = datetime.now().strftime("%H:%M:%S")
                cycles = status.get('consciousness_cycles', 0)
                goals = status.get('active_goals', 0)
                memories = status.get('episodes_in_memory', 0)
                thoughts = status.get('active_thoughts', 0)
                
                print(f"[{timestamp}] 🧠 Циклы: {cycles} | 🎯 Цели: {goals} | 💾 Память: {memories} | 🌳 Мысли: {thoughts} | CPU: {cpu_percent:.1f}% | RAM: {memory.percent:.1f}% | {gpu_info}")
                
                cycle_count += 1
                
                # Каждые 10 циклов показывать детальную статистику
                if cycle_count % 10 == 0:
                    await self._show_detailed_stats()
                
                await asyncio.sleep(30)  # Обновление каждые 30 секунд
                
            except Exception as e:
                print(f"❌ Ошибка мониторинга: {e}")
                await asyncio.sleep(5)
    
    async def _show_detailed_stats(self):
        """Показать детальную статистику"""
        print("\n📊 Детальная статистика:")
        print("-" * 40)
        
        try:
            # Статус модулей
            status = self.agent.get_status_report()
            if 'modules' in status:
                modules = status['modules']
                active_modules = sum(1 for active in modules.values() if active)
                total_modules = len(modules)
                print(f"🔧 Модули: {active_modules}/{total_modules} активны")
            
            # Информация о памяти
            if hasattr(self.agent, 'memory'):
                try:
                    episodes = self.agent.memory.get_recent_episodes(1000)
                    print(f"💾 Эпизоды в памяти: {len(episodes)}")
                    
                    # Типы эпизодов
                    types = {}
                    for episode in episodes:
                        ep_type = episode.get('type', 'unknown')
                        types[ep_type] = types.get(ep_type, 0) + 1
                    
                    if types:
                        print("📈 Распределение типов:")
                        for ep_type, count in types.items():
                            print(f"   {ep_type}: {count}")
                except Exception as e:
                    print(f"⚠️ Ошибка анализа памяти: {e}")
            
            # Информация о целях
            if hasattr(self.agent, 'goals'):
                try:
                    active_goals = self.agent.goals.get_active_goals()
                    print(f"🎯 Активных целей: {len(active_goals)}")
                    
                    for goal in active_goals[:3]:  # Показать первые 3
                        print(f"   - {goal.description} (прогресс: {goal.progress:.1f}%)")
                except Exception as e:
                    print(f"⚠️ Ошибка анализа целей: {e}")
            
            print("-" * 40)
            
        except Exception as e:
            print(f"❌ Ошибка детальной статистики: {e}")
    
    def stop(self):
        """Остановить агента"""
        self.running = False
        print("\n🛑 Сигнал остановки отправлен...")
        
        if self.consciousness_task:
            self.consciousness_task.cancel()
        
        if self.monitoring_task:
            self.monitoring_task.cancel()
        
        if self.agent:
            self.agent.stop()

async def main():
    """Основная функция"""
    runner = PersistentAgentRunner()
    
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