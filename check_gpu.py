#!/usr/bin/env python3
"""
Проверка GPU и использования видеокарты
"""

import torch
import GPUtil
import psutil
import subprocess
import sys

def check_gpu():
    """Проверить GPU"""
    print("🎮 Проверка GPU")
    print("=" * 40)
    
    # 1. PyTorch GPU
    print("📊 PyTorch GPU:")
    if torch.cuda.is_available():
        print(f"✅ CUDA доступна")
        print(f"   Версия CUDA: {torch.version.cuda}")
        print(f"   Количество GPU: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
            print(f"   GPU {i}: {gpu_name} ({gpu_memory:.1f}GB)")
        
        # Текущий GPU
        current_device = torch.cuda.current_device()
        print(f"   Текущий GPU: {current_device}")
        
        # Использование памяти
        allocated = torch.cuda.memory_allocated() / 1024**3
        cached = torch.cuda.memory_reserved() / 1024**3
        print(f"   Использовано VRAM: {allocated:.2f}GB")
        print(f"   Зарезервировано VRAM: {cached:.2f}GB")
        
    else:
        print("❌ CUDA недоступна")
    
    print()
    
    # 2. GPUtil
    print("📊 GPUtil GPU:")
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"   GPU {i}: {gpu.name}")
                print(f"   VRAM: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB")
                print(f"   Загрузка: {gpu.load * 100:.1f}%")
                print(f"   Температура: {gpu.temperature}°C")
        else:
            print("❌ GPU не обнаружены")
    except Exception as e:
        print(f"❌ Ошибка GPUtil: {e}")
    
    print()
    
    # 3. nvidia-smi
    print("📊 nvidia-smi:")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ nvidia-smi работает")
            lines = result.stdout.split('\n')
            for line in lines[:10]:  # Первые 10 строк
                if line.strip():
                    print(f"   {line}")
        else:
            print("❌ nvidia-smi не работает")
    except Exception as e:
        print(f"❌ Ошибка nvidia-smi: {e}")
    
    print()
    
    # 4. Системные ресурсы
    print("📊 Системные ресурсы:")
    memory = psutil.virtual_memory()
    print(f"   RAM: {memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB ({memory.percent:.1f}%)")
    
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"   CPU: {cpu_percent:.1f}%")
    
    print()
    
    # 5. Тест GPU
    print("🧪 Тест GPU:")
    if torch.cuda.is_available():
        try:
            # Создать тензор на GPU
            device = torch.device('cuda')
            x = torch.randn(1000, 1000).to(device)
            y = torch.randn(1000, 1000).to(device)
            
            # Матричное умножение
            start_time = torch.cuda.Event(enable_timing=True)
            end_time = torch.cuda.Event(enable_timing=True)
            
            start_time.record()
            z = torch.mm(x, y)
            end_time.record()
            
            torch.cuda.synchronize()
            elapsed_time = start_time.elapsed_time(end_time)
            
            print(f"✅ GPU тест пройден")
            print(f"   Время матричного умножения: {elapsed_time:.2f}ms")
            print(f"   Результат: {z.shape}")
            
            # Очистить память
            del x, y, z
            torch.cuda.empty_cache()
            
        except Exception as e:
            print(f"❌ Ошибка GPU теста: {e}")
    else:
        print("❌ GPU недоступна для тестирования")

def check_ollama_gpu():
    """Проверить использование GPU в Ollama"""
    print("\n🔧 Проверка Ollama GPU:")
    print("=" * 40)
    
    try:
        # Проверить статус Ollama
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama работает")
            
            # Проверить процессы Ollama
            ollama_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'ollama' in proc.info['name'].lower():
                        ollama_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if ollama_processes:
                print(f"📋 Найдено процессов Ollama: {len(ollama_processes)}")
                for proc in ollama_processes:
                    print(f"   PID {proc['pid']}: {proc['name']}")
            else:
                print("⚠️ Процессы Ollama не найдены")
                
        else:
            print("❌ Ollama не отвечает")
            
    except Exception as e:
        print(f"❌ Ошибка проверки Ollama: {e}")

def main():
    """Основная функция"""
    print("🚀 Проверка GPU и использования видеокарты")
    print("=" * 60)
    
    check_gpu()
    check_ollama_gpu()
    
    print("\n✅ Проверка завершена!")

if __name__ == "__main__":
    main() 