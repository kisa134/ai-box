#!/usr/bin/env python3
"""
AIbox Desktop Application
Полноценное десктопное приложение для управления автономным агентом
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import asyncio
import json
import time
import psutil
import GPUtil
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Импорт наших модулей
from autonomous_agent import AutonomousAgent
from core.goal_module import GoalPriority

# Настройка CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AIboxDesktopApp:
    """Главное приложение AIbox"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 AIbox - Автономный Агент с Самосознанием")
        self.root.geometry("1400x900")
        
        # Агент
        self.agent = None
        self.agent_running = False
        self.auto_update = False
        
        # Создание интерфейса
        self.setup_ui()
        
        # Запуск автообновления
        self.start_auto_update()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Главный контейнер
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🤖 AIbox - Автономный Агент с Самосознанием",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Панель управления
        self.setup_control_panel(main_frame)
        
        # Вкладки
        self.setup_tabs(main_frame)
    
    def setup_control_panel(self, parent):
        """Настройка панели управления"""
        control_frame = ctk.CTkFrame(parent)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # Кнопки управления
        button_frame = ctk.CTkFrame(control_frame)
        button_frame.pack(side="left", padx=10, pady=5)
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="🚀 Запустить Агента",
            command=self.start_agent,
            fg_color="green"
        )
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="🛑 Остановить Агента",
            command=self.stop_agent,
            fg_color="red"
        )
        self.stop_button.pack(side="left", padx=5)
        
        # Статус
        status_frame = ctk.CTkFrame(control_frame)
        status_frame.pack(side="right", padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="❌ Агент остановлен",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack()
        
        # Автообновление
        self.auto_update_var = tk.BooleanVar()
        auto_update_checkbox = ctk.CTkCheckBox(
            control_frame,
            text="🔄 Автообновление",
            variable=self.auto_update_var,
            command=self.toggle_auto_update
        )
        auto_update_checkbox.pack(side="right", padx=10)
    
    def setup_tabs(self, parent):
        """Настройка вкладок"""
        # Создание notebook
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Вкладка 1: Главный дашборд
        self.dashboard_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="📊 Главный Дашборд")
        self.setup_dashboard()
        
        # Вкладка 2: Диалог с агентом
        self.chat_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.chat_tab, text="💬 Диалог с Агентом")
        self.setup_chat()
        
        # Вкладка 3: Поток сознания
        self.consciousness_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.consciousness_tab, text="🧠 Поток Сознания")
        self.setup_consciousness()
        
        # Вкладка 4: Дерево мыслей
        self.thoughts_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.thoughts_tab, text="🌳 Дерево Мыслей")
        self.setup_thoughts()
        
        # Вкладка 5: Память и цели
        self.memory_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.memory_tab, text="💾 Память и Цели")
        self.setup_memory()
        
        # Вкладка 6: Self-модель
        self.self_model_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.self_model_tab, text="🧠 Self-Модель")
        self.setup_self_model()
        
        # Вкладка 7: Бенчмарки
        self.benchmarks_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.benchmarks_tab, text="📊 Бенчмарки")
        self.setup_benchmarks()
        
        # Вкладка 8: Настройки
        self.settings_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.settings_tab, text="⚙️ Настройки")
        self.setup_settings()
    
    def setup_dashboard(self):
        """Настройка главного дашборда"""
        # Верхняя панель с KPI
        kpi_frame = ctk.CTkFrame(self.dashboard_tab)
        kpi_frame.pack(fill="x", padx=10, pady=5)
        
        # KPI метрики
        self.self_awareness_label = ctk.CTkLabel(kpi_frame, text="Self-Awareness: 0.0")
        self.self_awareness_label.pack(side="left", padx=10)
        
        self.explainability_label = ctk.CTkLabel(kpi_frame, text="Explainability: 0.0")
        self.explainability_label.pack(side="left", padx=10)
        
        self.cognitive_flexibility_label = ctk.CTkLabel(kpi_frame, text="Cognitive Flexibility: 0.0")
        self.cognitive_flexibility_label.pack(side="left", padx=10)
        
        # Графики ресурсов
        charts_frame = ctk.CTkFrame(self.dashboard_tab)
        charts_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Создание графиков
        self.create_resource_charts(charts_frame)
    
    def setup_chat(self):
        """Настройка чата с агентом"""
        # Поле ввода
        input_frame = ctk.CTkFrame(self.chat_tab)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.chat_input = ctk.CTkTextbox(input_frame, height=100)
        self.chat_input.pack(side="left", fill="x", expand=True, padx=5)
        
        send_button = ctk.CTkButton(
            input_frame,
            text="📤 Отправить",
            command=self.send_message
        )
        send_button.pack(side="right", padx=5)
        
        # История чата
        chat_history_frame = ctk.CTkFrame(self.chat_tab)
        chat_history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.chat_history = ctk.CTkTextbox(chat_history_frame, wrap="word")
        self.chat_history.pack(fill="both", expand=True, padx=5, pady=5)
    
    def setup_consciousness(self):
        """Настройка потока сознания"""
        # Фильтры
        filter_frame = ctk.CTkFrame(self.consciousness_tab)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(filter_frame, text="Фильтр событий:").pack(side="left", padx=5)
        
        self.event_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Все события", "Мысли", "Эмоции", "Память", "Цели"]
        )
        self.event_filter.pack(side="left", padx=5)
        
        # Поток событий
        events_frame = ctk.CTkFrame(self.consciousness_tab)
        events_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.events_list = ctk.CTkTextbox(events_frame, wrap="word")
        self.events_list.pack(fill="both", expand=True, padx=5, pady=5)
    
    def setup_thoughts(self):
        """Настройка дерева мыслей"""
        # Контролы
        controls_frame = ctk.CTkFrame(self.thoughts_tab)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="🔄 Обновить",
            command=self.refresh_thoughts
        )
        refresh_button.pack(side="left", padx=5)
        
        # Область для графа
        graph_frame = ctk.CTkFrame(self.thoughts_tab)
        graph_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.thoughts_canvas = tk.Canvas(graph_frame, bg="white")
        self.thoughts_canvas.pack(fill="both", expand=True)
    
    def setup_memory(self):
        """Настройка памяти и целей"""
        # Панели
        panels_frame = ctk.CTkFrame(self.memory_tab)
        panels_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Левая панель - Память
        memory_frame = ctk.CTkFrame(panels_frame)
        memory_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(memory_frame, text="💾 Память", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        # Поиск в памяти
        search_frame = ctk.CTkFrame(memory_frame)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        self.memory_search = ctk.CTkEntry(search_frame, placeholder_text="Поиск в памяти...")
        self.memory_search.pack(side="left", fill="x", expand=True, padx=5)
        
        search_button = ctk.CTkButton(search_frame, text="🔍", command=self.search_memory)
        search_button.pack(side="right", padx=5)
        
        # Результаты поиска
        self.memory_results = ctk.CTkTextbox(memory_frame, wrap="word")
        self.memory_results.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Правая панель - Цели
        goals_frame = ctk.CTkFrame(panels_frame)
        goals_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(goals_frame, text="🎯 Цели", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.goals_list = ctk.CTkTextbox(goals_frame, wrap="word")
        self.goals_list.pack(fill="both", expand=True, padx=5, pady=5)
    
    def setup_self_model(self):
        """Настройка Self-модели"""
        # Панели
        panels_frame = ctk.CTkFrame(self.self_model_tab)
        panels_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Левая панель - Профиль личности
        profile_frame = ctk.CTkFrame(panels_frame)
        profile_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(profile_frame, text="👤 Профиль Личности", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.personality_text = ctk.CTkTextbox(profile_frame, wrap="word")
        self.personality_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Правая панель - Метапознание
        metacognition_frame = ctk.CTkFrame(panels_frame)
        metacognition_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(metacognition_frame, text="🧠 Метапознание", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.metacognition_text = ctk.CTkTextbox(metacognition_frame, wrap="word")
        self.metacognition_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def setup_benchmarks(self):
        """Настройка бенчмарков"""
        # Кнопки запуска тестов
        buttons_frame = ctk.CTkFrame(self.benchmarks_tab)
        buttons_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🧪 Тест Самоузнавания",
            command=self.run_self_recognition_test
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🧠 Тест Метапознания",
            command=self.run_metacognition_test
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="⏰ Тест Временной Непрерывности",
            command=self.run_temporal_test
        ).pack(side="left", padx=5)
        
        # Область для результатов
        results_frame = ctk.CTkFrame(self.benchmarks_tab)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.benchmarks_text = ctk.CTkTextbox(results_frame, wrap="word")
        self.benchmarks_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def setup_settings(self):
        """Настройка настроек"""
        # Модели Ollama
        models_frame = ctk.CTkFrame(self.settings_tab)
        models_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(models_frame, text="🔧 Модели Ollama", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        # Список моделей
        self.models_list = ctk.CTkTextbox(models_frame, height=200)
        self.models_list.pack(fill="x", padx=5, pady=5)
        
        # Настройки агента
        agent_frame = ctk.CTkFrame(self.settings_tab)
        agent_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(agent_frame, text="⚙️ Настройки Агента", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        # Частота цикла сознания
        cycle_frame = ctk.CTkFrame(agent_frame)
        cycle_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(cycle_frame, text="Частота цикла сознания (сек):").pack(side="left", padx=5)
        
        self.cycle_frequency = ctk.CTkEntry(cycle_frame, width=100)
        self.cycle_frequency.pack(side="left", padx=5)
        self.cycle_frequency.insert(0, "30")
    
    def create_resource_charts(self, parent):
        """Создание графиков ресурсов"""
        # Создание фигуры matplotlib
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        fig.patch.set_facecolor('#2b2b2b')
        
        # График CPU и RAM
        ax1.set_facecolor('#2b2b2b')
        ax1.set_title('CPU и RAM', color='white')
        ax1.set_ylabel('Использование (%)', color='white')
        ax1.tick_params(colors='white')
        
        # График GPU
        ax2.set_facecolor('#2b2b2b')
        ax2.set_title('GPU VRAM', color='white')
        ax2.set_ylabel('Использование (MB)', color='white')
        ax2.tick_params(colors='white')
        
        # Встраивание в tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.resource_canvas = canvas
        self.resource_fig = fig
        self.resource_ax1 = ax1
        self.resource_ax2 = ax2
    
    def start_agent(self):
        """Запуск агента"""
        try:
            if self.agent is None:
                self.status_label.configure(text="🔄 Инициализация агента...")
                
                # Запуск в отдельном потоке
                thread = threading.Thread(target=self._initialize_agent)
                thread.start()
            else:
                messagebox.showinfo("Информация", "Агент уже запущен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка запуска агента: {e}")
    
    def _initialize_agent(self):
        """Инициализация агента в отдельном потоке"""
        try:
            self.agent = AutonomousAgent("Desktop AIbox Agent", "agent_data")
            self.agent.initialize_modules()
            self.agent.initialize_agent()
            
            self.agent_running = True
            
            # Обновление UI в главном потоке
            self.root.after(0, self._update_status_after_start)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка инициализации: {e}"))
    
    def _update_status_after_start(self):
        """Обновление статуса после запуска"""
        self.status_label.configure(text="✅ Агент работает", text_color="green")
        messagebox.showinfo("Успех", "Агент успешно запущен!")
    
    def stop_agent(self):
        """Остановка агента"""
        try:
            if self.agent:
                self.agent.stop()
                self.agent = None
                self.agent_running = False
                self.status_label.configure(text="❌ Агент остановлен", text_color="red")
                messagebox.showinfo("Информация", "Агент остановлен")
            else:
                messagebox.showinfo("Информация", "Агент не запущен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка остановки агента: {e}")
    
    def toggle_auto_update(self):
        """Переключение автообновления"""
        self.auto_update = self.auto_update_var.get()
    
    def start_auto_update(self):
        """Запуск автообновления"""
        if self.auto_update:
            self.update_dashboard()
        
        # Повтор через 1 секунду
        self.root.after(1000, self.start_auto_update)
    
    def update_dashboard(self):
        """Обновление дашборда"""
        try:
            if self.agent and self.agent_running:
                # Получение статуса
                status = self.agent.get_status_report()
                
                # Обновление KPI
                if 'consciousness_cycles' in status:
                    cycles = status['consciousness_cycles']
                    # Здесь можно добавить расчет метрик
                
                # Обновление графиков ресурсов
                self.update_resource_charts()
                
        except Exception as e:
            print(f"Ошибка обновления дашборда: {e}")
    
    def update_resource_charts(self):
        """Обновление графиков ресурсов"""
        try:
            # Получение данных о ресурсах
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            
            # Обновление графиков
            self.resource_ax1.clear()
            self.resource_ax1.set_facecolor('#2b2b2b')
            self.resource_ax1.set_title('CPU и RAM', color='white')
            self.resource_ax1.set_ylabel('Использование (%)', color='white')
            self.resource_ax1.tick_params(colors='white')
            
            # Добавление данных
            self.resource_ax1.bar(['CPU', 'RAM'], [cpu_percent, memory.percent])
            
            # GPU данные
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    self.resource_ax2.clear()
                    self.resource_ax2.set_facecolor('#2b2b2b')
                    self.resource_ax2.set_title('GPU VRAM', color='white')
                    self.resource_ax2.set_ylabel('Использование (MB)', color='white')
                    self.resource_ax2.tick_params(colors='white')
                    
                    self.resource_ax2.bar(['VRAM'], [gpu.memoryUsed])
            except:
                pass
            
            self.resource_canvas.draw()
            
        except Exception as e:
            print(f"Ошибка обновления графиков: {e}")
    
    def send_message(self):
        """Отправка сообщения агенту"""
        if not self.agent or not self.agent_running:
            messagebox.showwarning("Предупреждение", "Агент не запущен")
            return
        
        message = self.chat_input.get("1.0", "end-1c")
        if not message.strip():
            return
        
        # Добавление сообщения пользователя в историю
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_history.insert("end", f"[{timestamp}] 👤 Вы: {message}\n")
        
        # Очистка поля ввода
        self.chat_input.delete("1.0", "end")
        
        # Отправка сообщения агенту в отдельном потоке
        thread = threading.Thread(target=self._process_message, args=(message,))
        thread.start()
    
    def _process_message(self, message):
        """Обработка сообщения в отдельном потоке"""
        try:
            # Асинхронный вызов
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.agent.process_input(message))
            loop.close()
            
            # Обновление UI в главном потоке
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.root.after(0, lambda: self.chat_history.insert("end", f"[{timestamp}] 🤖 Агент: {response}\n\n"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка обработки сообщения: {e}"))
    
    def refresh_thoughts(self):
        """Обновление дерева мыслей"""
        if not self.agent or not self.agent_running:
            messagebox.showwarning("Предупреждение", "Агент не запущен")
            return
        
        try:
            # Получение дерева мыслей
            if hasattr(self.agent, 'thought_tree'):
                thoughts = self.agent.thought_tree.thoughts
                
                # Создание графа
                G = nx.DiGraph()
                
                for thought_id, thought in thoughts.items():
                    G.add_node(thought_id, content=thought.content[:50])
                    
                    # Добавление связей (если есть)
                    if hasattr(thought, 'parent_id') and thought.parent_id:
                        G.add_edge(thought.parent_id, thought_id)
                
                # Очистка canvas
                self.thoughts_canvas.delete("all")
                
                # Рисование графа
                pos = nx.spring_layout(G)
                
                # Рисование узлов
                for node, (x, y) in pos.items():
                    x_canvas = (x + 1) * 200 + 100
                    y_canvas = (y + 1) * 100 + 100
                    
                    self.thoughts_canvas.create_oval(
                        x_canvas-20, y_canvas-20, x_canvas+20, y_canvas+20,
                        fill="lightblue", outline="blue"
                    )
                    
                    content = G.nodes[node]['content']
                    self.thoughts_canvas.create_text(
                        x_canvas, y_canvas, text=content, font=("Arial", 8)
                    )
                
                # Рисование рёбер
                for edge in G.edges():
                    start_pos = pos[edge[0]]
                    end_pos = pos[edge[1]]
                    
                    x1 = (start_pos[0] + 1) * 200 + 100
                    y1 = (start_pos[1] + 1) * 100 + 100
                    x2 = (end_pos[0] + 1) * 200 + 100
                    y2 = (end_pos[1] + 1) * 100 + 100
                    
                    self.thoughts_canvas.create_line(x1, y1, x2, y2, fill="gray", arrow="last")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обновления дерева мыслей: {e}")
    
    def search_memory(self):
        """Поиск в памяти"""
        if not self.agent or not self.agent_running:
            messagebox.showwarning("Предупреждение", "Агент не запущен")
            return
        
        query = self.memory_search.get()
        if not query.strip():
            return
        
        try:
            if hasattr(self.agent, 'memory'):
                results = self.agent.memory.retrieve_similar(query, 5)
                
                # Очистка результатов
                self.memory_results.delete("1.0", "end")
                
                if results:
                    for i, result in enumerate(results, 1):
                        content = result.get('content', 'Нет данных')
                        result_type = result.get('type', 'unknown')
                        
                        self.memory_results.insert("end", f"Результат {i}:\n")
                        self.memory_results.insert("end", f"Тип: {result_type}\n")
                        self.memory_results.insert("end", f"Содержание: {content}\n")
                        self.memory_results.insert("end", "-" * 50 + "\n")
                else:
                    self.memory_results.insert("end", "Ничего не найдено")
                    
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска в памяти: {e}")
    
    def run_self_recognition_test(self):
        """Запуск теста самоузнавания"""
        if not self.agent or not self.agent_running:
            messagebox.showwarning("Предупреждение", "Агент не запущен")
            return
        
        try:
            diagnostic = self.agent.get_consciousness_diagnostic()
            score = diagnostic.get('self_recognition', 0.0)
            
            self.benchmarks_text.insert("end", f"🧪 Тест Самоузнавания: {score:.2f}\n")
            self.benchmarks_text.insert("end", f"Время: {datetime.now().strftime('%H:%M:%S')}\n")
            self.benchmarks_text.insert("end", "-" * 50 + "\n")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка теста самоузнавания: {e}")
    
    def run_metacognition_test(self):
        """Запуск теста метапознания"""
        if not self.agent or not self.agent_running:
            messagebox.showwarning("Предупреждение", "Агент не запущен")
            return
        
        try:
            diagnostic = self.agent.get_consciousness_diagnostic()
            score = diagnostic.get('metacognitive_awareness', 0.0)
            
            self.benchmarks_text.insert("end", f"🧠 Тест Метапознания: {score:.2f}\n")
            self.benchmarks_text.insert("end", f"Время: {datetime.now().strftime('%H:%M:%S')}\n")
            self.benchmarks_text.insert("end", "-" * 50 + "\n")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка теста метапознания: {e}")
    
    def run_temporal_test(self):
        """Запуск теста временной непрерывности"""
        if not self.agent or not self.agent_running:
            messagebox.showwarning("Предупреждение", "Агент не запущен")
            return
        
        try:
            diagnostic = self.agent.get_consciousness_diagnostic()
            score = diagnostic.get('temporal_continuity', 0.0)
            
            self.benchmarks_text.insert("end", f"⏰ Тест Временной Непрерывности: {score:.2f}\n")
            self.benchmarks_text.insert("end", f"Время: {datetime.now().strftime('%H:%M:%S')}\n")
            self.benchmarks_text.insert("end", "-" * 50 + "\n")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка теста временной непрерывности: {e}")
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

def main():
    """Главная функция"""
    app = AIboxDesktopApp()
    app.run()

if __name__ == "__main__":
    main() 