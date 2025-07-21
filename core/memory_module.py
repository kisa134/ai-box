import chromadb
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import uuid
import json
import threading
import queue

class SimpleMemory:
    """Простая локальная память без векторного поиска"""
    
    def __init__(self):
        self.episodes: Dict[str, Dict[str, Any]] = {}
        self.episode_list: List[str] = []  # Для хронологического порядка
        
    def store(self, episode_id: str, content: str, metadata: Dict[str, Any]):
        """Сохранить эпизод"""
        self.episodes[episode_id] = {
            "content": content,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat()
        }
        self.episode_list.append(episode_id)
        
        # Ограничить размер
        if len(self.episode_list) > 1000:
            old_id = self.episode_list.pop(0)
            if old_id in self.episodes:
                del self.episodes[old_id]
    
    def retrieve_recent(self, count: int) -> List[Dict[str, Any]]:
        """Получить последние эпизоды"""
        recent_ids = self.episode_list[-count:] if count > 0 else self.episode_list
        return [
            {
                "id": episode_id,
                "content": self.episodes[episode_id]["content"],
                "metadata": self.episodes[episode_id]["metadata"]
            }
            for episode_id in reversed(recent_ids) 
            if episode_id in self.episodes
        ]
    
    def search_simple(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Простой поиск по ключевым словам"""
        query_words = set(query.lower().split())
        results = []
        
        for episode_id, episode_data in self.episodes.items():
            content_words = set(episode_data["content"].lower().split())
            # Простая оценка релевантности
            relevance = len(query_words.intersection(content_words)) / len(query_words) if query_words else 0
            
            if relevance > 0:
                results.append({
                    "id": episode_id,
                    "content": episode_data["content"],
                    "metadata": episode_data["metadata"],
                    "relevance": relevance
                })
        
        # Сортировка по релевантности
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:limit]

class MemoryModule:
    """
    Модуль памяти агента с векторным хранением эпизодов опыта,
    стратегий, познаний и логов принятия решений
    """
    
    def __init__(self, collection_name: str = "agent_memory"):
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self.encoder = None
        self.encoder_loading = False
        self.use_fallback = False
        
        # Fallback память
        self.simple_memory = SimpleMemory()
        
        # Инициализация ChromaDB
        self._init_chromadb()
        
        # Асинхронная загрузка модели
        self._init_encoder_async()
        
    def _init_chromadb(self):
        """Инициализация ChromaDB"""
        try:
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
            print("✅ ChromaDB инициализирован")
        except Exception as e:
            print(f"⚠️  ChromaDB недоступен: {e}")
            print("🔄 Используется локальная память")
            self.use_fallback = True
    
    def _init_encoder_async(self):
        """Асинхронная инициализация энкодера"""
        def load_encoder():
            try:
                print("🔄 Загрузка модели SentenceTransformer...")
                self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
                print("✅ SentenceTransformer загружен")
            except Exception as e:
                print(f"⚠️  SentenceTransformer недоступен: {e}")
                print("🔄 Векторный поиск отключен")
            finally:
                self.encoder_loading = False
        
        if not self.use_fallback:
            self.encoder_loading = True
            # Запуск в отдельном потоке
            threading.Thread(target=load_encoder, daemon=True).start()
        
    def is_ready(self) -> bool:
        """Проверить готовность системы памяти"""
        if self.use_fallback:
            return True
        return self.collection is not None and (self.encoder is not None or not self.encoder_loading)
    
    def store_episode(self, 
                     content: str, 
                     episode_type: str,
                     metadata: Optional[Dict[str, Any]] = None) -> str:
        """Сохранить эпизод опыта"""
        episode_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        if metadata is None:
            metadata = {}
            
        # Очистить метаданные от сложных объектов
        clean_metadata = {
            "timestamp": timestamp,
            "type": episode_type,
            "episode_id": episode_id
        }
        
        # Добавить только простые типы данных
        if metadata:
            for key, value in metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    clean_metadata[key] = value
                elif isinstance(value, dict):
                    clean_metadata[f"{key}_str"] = str(value)[:100]
                else:
                    clean_metadata[f"{key}_str"] = str(value)[:100]
        
        # Сохранение в fallback память
        self.simple_memory.store(episode_id, content, clean_metadata)
        
        # Попытка сохранения в ChromaDB (если доступен)
        if not self.use_fallback and self.collection is not None:
            try:
                if self.encoder is not None:
                    # Векторизация содержимого
                    embedding = self.encoder.encode(content).tolist()
                    
                    self.collection.add(
                        embeddings=[embedding],
                        documents=[content],
                        metadatas=[clean_metadata],
                        ids=[episode_id]
                    )
                else:
                    # Сохранить без векторизации для последующей обработки
                    self.collection.add(
                        documents=[content],
                        metadatas=[clean_metadata],
                        ids=[episode_id]
                    )
            except Exception as e:
                print(f"⚠️  Ошибка сохранения в ChromaDB: {e}")
        
        return episode_id
    
    def retrieve_similar(self, 
                        query: str, 
                        n_results: int = 5) -> List[Dict[str, Any]]:
        """Найти похожие эпизоды"""
        
        # Векторный поиск (если доступен)
        if not self.use_fallback and self.collection is not None and self.encoder is not None:
            try:
                query_embedding = self.encoder.encode(query).tolist()
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results
                )
                
                similar_episodes = []
                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        similar_episodes.append({
                            'id': results['ids'][0][i],
                            'content': doc,
                            'metadata': results['metadatas'][0][i],
                            'distance': results['distances'][0][i] if 'distances' in results else 0
                        })
                
                return similar_episodes
                
            except Exception as e:
                print(f"⚠️  Ошибка векторного поиска: {e}")
        
        # Fallback: простой поиск
        return self.simple_memory.search_simple(query, n_results)
    
    def get_recent_episodes(self, count: int = 10) -> List[Dict[str, Any]]:
        """Получить последние эпизоды"""
        
        # Попытка получить из ChromaDB
        if not self.use_fallback and self.collection is not None:
            try:
                results = self.collection.get(
                    limit=count,
                    include=['documents', 'metadatas']
                )
                
                recent_episodes = []
                if results['documents']:
                    for i, doc in enumerate(results['documents']):
                        recent_episodes.append({
                            'id': results['ids'][i],
                            'content': doc,
                            'metadata': results['metadatas'][i]
                        })
                
                # Сортировка по времени
                recent_episodes.sort(
                    key=lambda x: x['metadata'].get('timestamp', ''),
                    reverse=True
                )
                
                return recent_episodes[:count]
                
            except Exception as e:
                print(f"⚠️  Ошибка получения из ChromaDB: {e}")
        
        # Fallback
        return self.simple_memory.retrieve_recent(count)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получить статистику памяти"""
        stats = {
            "mode": "fallback" if self.use_fallback else "chromadb",
            "encoder_ready": self.encoder is not None,
            "encoder_loading": self.encoder_loading,
            "local_episodes": len(self.simple_memory.episodes)
        }
        
        if not self.use_fallback and self.collection is not None:
            try:
                count_result = self.collection.count()
                stats["chromadb_episodes"] = count_result
            except:
                stats["chromadb_episodes"] = "unknown"
        
        return stats 