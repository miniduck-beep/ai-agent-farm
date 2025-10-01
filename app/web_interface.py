"""
AI Agent Farm - Web Interface
============================
MVP пользовательский портал на Streamlit
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any
import asyncio
import logging

# Настройка страницы
st.set_page_config(
    page_title="AI Agent Farm",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Конфигурация API
API_BASE_URL = "http://localhost:8000"  # Можно вынести в переменные окружения

class AIAgentFarmClient:
    """Клиент для взаимодействия с AI Agent Farm API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        
    def start_research(self, topic: str, crew_type: str = "business_analysis", 
                      language: str = "ru", depth: str = "standard") -> Dict[str, Any]:
        """Запускает новое исследование"""
        try:
            response = requests.post(
                f"{self.base_url}/research",
                json={
                    "topic": topic,
                    "crew_type": crew_type,
                    "language": language,
                    "depth": depth
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Ошибка при запуске исследования: {str(e)}")
            return {"error": str(e)}
    
    def get_result(self, task_id: str) -> Dict[str, Any]:
        """Получает результат исследования"""
        try:
            response = requests.get(f"{self.base_url}/result/{task_id}", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_health(self) -> Dict[str, Any]:
        """Проверяет здоровье системы"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except:
            return {"status": "unhealthy"}

def main():
    """Основная функция веб-интерфейса"""
    
    # Инициализация клиента
    client = AIAgentFarmClient()
    
    # Заголовок
    st.title("🤖 AI Agent Farm")
    st.subheader("Мощная многоагентная система для исследований и аналитики")
    
    # Проверка состояния системы
    with st.spinner("Проверка состояния системы..."):
        health = client.get_health()
    
    if health.get("status") == "unhealthy":
        st.error("⚠️ AI Agent Farm недоступен. Проверьте, что система запущена.")
        st.code(f"docker compose up -d", language="bash")
        return
    else:
        st.success("✅ AI Agent Farm онлайн и готов к работе!")
    
    # Сайдбар с настройками
    with st.sidebar:
        st.header("⚙️ Настройки исследования")
        
        # Тип команды агентов
        crew_type = st.selectbox(
            "Команда агентов",
            ["business_analysis", "seo_content", "tech_research", "financial_analysis"],
            help="Выберите специализированную команду для вашей задачи"
        )
        
        crew_descriptions = {
            "business_analysis": "💼 Бизнес-анализ и исследования рынка",
            "seo_content": "📝 SEO и контент-стратегии",
            "tech_research": "🔬 Технические исследования", 
            "financial_analysis": "💰 Финансовый анализ"
        }
        
        st.info(crew_descriptions.get(crew_type, "Универсальная команда"))
        
        # Язык отчета
        language = st.selectbox("Язык отчета", ["ru", "en"], index=0)
        
        # Глубина анализа
        depth = st.selectbox(
            "Глубина анализа",
            ["basic", "standard", "comprehensive"],
            index=1,
            help="basic: быстрый обзор, standard: детальный анализ, comprehensive: исчерпывающее исследование"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Статистика системы")
        if health.get("status") == "healthy":
            st.metric("Статус", "🟢 Онлайн")
            # Можно добавить больше метрик из health endpoint
    
    # Основная форма
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🚀 Запуск исследования")
        
        # Поле для темы исследования
        topic = st.text_area(
            "Тема исследования",
            placeholder="Введите тему для исследования, например:\n• Анализ рынка электромобилей в России\n• SEO стратегия для IT-стартапа\n• Технические тренды в машинном обучении",
            height=100,
            help="Опишите, что вы хотите исследовать. Чем подробнее, тем лучше результат."
        )
        
        # Кнопка запуска
        if st.button("🔍 Начать исследование", type="primary", disabled=not topic.strip()):
            if topic.strip():
                with st.spinner("Запускаем исследование..."):
                    result = client.start_research(topic, crew_type, language, depth)
                
                if "error" not in result:
                    st.session_state.task_id = result.get("task_id")
                    st.session_state.start_time = datetime.now()
                    st.success(f"✅ Исследование запущено! Task ID: `{result.get('task_id')}`")
                    st.info("Процесс может занять 3-10 минут в зависимости от сложности темы.")
                    st.rerun()
    
    with col2:
        st.header("💡 Примеры тем")
        
        example_topics = [
            "Анализ конкурентов на рынке доставки еды",
            "SEO стратегия для интернет-магазина",
            "Технологические тренды в блокчейне", 
            "Инвестиционная привлекательность IT-сектора"
        ]
        
        for i, example in enumerate(example_topics):
            if st.button(f"📋 {example}", key=f"example_{i}"):
                st.session_state.selected_topic = example
                st.rerun()
        
        if hasattr(st.session_state, 'selected_topic'):
            st.text_area("", value=st.session_state.selected_topic, key="topic_from_example")
    
    # Отслеживание прогресса
    if hasattr(st.session_state, 'task_id') and st.session_state.task_id:
        st.markdown("---")
        st.header("📊 Прогресс исследования")
        
        # Контейнер для обновления статуса
        status_container = st.container()
        result_container = st.container()
        
        # Автообновление статуса
        placeholder = st.empty()
        
        with placeholder:
            with st.spinner("Получаем статус исследования..."):
                status_result = client.get_result(st.session_state.task_id)
        
        if "error" not in status_result:
            status = status_result.get("status", "UNKNOWN")
            progress = status_result.get("progress", 0)
            
            # Отображение прогресса
            with status_container:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Статус", status)
                
                with col2:
                    elapsed = datetime.now() - st.session_state.start_time
                    st.metric("Время выполнения", f"{elapsed.seconds}s")
                
                with col3:
                    st.metric("Прогресс", f"{progress}%")
                
                # Прогресс-бар
                st.progress(progress / 100)
                
                # Статус-сообщения
                status_messages = {
                    "PENDING": "⏳ Исследование ожидает обработки...",
                    "PROCESSING": "🔄 Агенты работают над исследованием...", 
                    "SUCCESS": "✅ Исследование завершено успешно!",
                    "FAILURE": "❌ Произошла ошибка при выполнении исследования"
                }
                
                st.info(status_messages.get(status, f"Статус: {status}"))
            
            # Отображение результата
            if status == "SUCCESS":
                with result_container:
                    st.header("📄 Результат исследования")
                    
                    research_result = status_result.get("result", {})
                    
                    if isinstance(research_result, dict):
                        result_text = research_result.get("result", "")
                    else:
                        result_text = str(research_result)
                    
                    # Красивое отображение результата
                    st.markdown(result_text)
                    
                    # Метаданные
                    with st.expander("📊 Детали выполнения"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.json({
                                "task_id": st.session_state.task_id,
                                "processing_time": status_result.get("processing_time", 0),
                                "crew_type": crew_type,
                                "language": language,
                                "depth": depth
                            })
                        
                        with col2:
                            st.download_button(
                                "📥 Скачать результат", 
                                data=result_text,
                                file_name=f"research_{st.session_state.task_id}.md",
                                mime="text/markdown"
                            )
                    
                    # Опция запуска нового исследования
                    if st.button("🔄 Запустить новое исследование"):
                        if 'task_id' in st.session_state:
                            del st.session_state.task_id
                        if 'start_time' in st.session_state:
                            del st.session_state.start_time
                        st.rerun()
            
            elif status in ["PENDING", "PROCESSING"]:
                # Автообновление каждые 10 секунд
                time.sleep(10)
                st.rerun()
            
            elif status == "FAILURE":
                st.error("Произошла ошибка при выполнении исследования")
                error_msg = status_result.get("error", "Неизвестная ошибка")
                st.code(error_msg)
                
                if st.button("🔄 Попробовать снова"):
                    if 'task_id' in st.session_state:
                        del st.session_state.task_id
                    st.rerun()
        
        else:
            st.error("Не удалось получить статус исследования")
            if st.button("🔄 Обновить"):
                st.rerun()
    
    # Футер
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🤖 Powered by AI Agent Farm | 
            <a href='https://github.com/miniduck-beep/ai-agent-farm'>GitHub</a> | 
            <a href='http://localhost:8000/docs'>API Docs</a></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
