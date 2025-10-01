"""
AI Agent Farm - Enhanced Web Interface
=====================================
Comprehensive веб-интерфейс с поддержкой showcase команд
"""

import streamlit as st
import requests
import time
import json
from datetime import datetime
import pandas as pd

# Конфигурация
API_BASE_URL = "http://localhost:8000"

# Настройка страницы
st.set_page_config(
    page_title="🤖 AI Agent Farm - Интеллектуальная Ферма AI Агентов",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS стили для улучшенного UI
st.markdown("""
<style>
    .main-header {
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    .showcase-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .standard-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .metrics-container {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Главная функция веб-интерфейса"""
    
    # Заголовок
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🤖 AI Agent Farm")
    st.markdown("**Интеллектуальная Ферма AI Агентов** - Ваш персональный исследовательский центр")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Боковая панель с навигацией
    with st.sidebar:
        st.header("🎯 Навигация")
        page = st.selectbox(
            "Выберите раздел:",
            [
                "🏠 Главная",
                "🎯 Showcase Команды", 
                "🔍 Стандартные Исследования",
                "📊 Мониторинг Системы",
                "❓ Справка"
            ]
        )
    
    # Роутинг страниц
    if page == "🏠 Главная":
        show_home_page()
    elif page == "🎯 Showcase Команды":
        show_showcase_page()
    elif page == "🔍 Стандартные Исследования":
        show_standard_research_page()
    elif page == "📊 Мониторинг Системы":
        show_monitoring_page()
    elif page == "❓ Справка":
        show_help_page()

def show_home_page():
    """Главная страница с обзором возможностей"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🚀 Добро пожаловать в AI Agent Farm!")
        
        st.markdown("""
        ### 🌟 Ключевые возможности
        
        **🎯 Showcase Команды** - Профессиональные решения:
        - 💼 **SWOT-Аналитик** - Comprehensive анализ компаний
        - 🔬 **Технический Рецензент** - Анализ GitHub репозиториев  
        - 💰 **Инвестиционный Советник** - Анализ акций и инвестиций
        
        **🔍 Стандартные Команды** - Универсальные исследования:
        - Бизнес-аналитика • SEO контент • Техническое исследование • Финансовый анализ
        """)
        
        # Быстрые действия
        st.markdown("### ⚡ Быстрый старт")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("💼 SWOT Анализ", help="Анализ сильных и слабых сторон компании"):
                st.session_state.page = "showcase"
                st.session_state.selected_crew = "swot_analysis"
                st.rerun()
        
        with col_b:
            if st.button("🔬 Code Review", help="Техническая рецензия кода"):
                st.session_state.page = "showcase"
                st.session_state.selected_crew = "tech_review"
                st.rerun()
        
        with col_c:
            if st.button("💰 Акции", help="Инвестиционный анализ"):
                st.session_state.page = "showcase"
                st.session_state.selected_crew = "investment_advisor"
                st.rerun()
    
    with col2:
        # Статистика системы
        st.header("📊 Статистика")
        
        try:
            health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if health_response.status_code == 200:
                health_data = health_response.json()
                
                st.success("✅ Система работает")
                st.metric("Версия", health_data.get("version", "Unknown"))
                
                # Компоненты системы
                components = health_data.get("components", {})
                for comp, status in components.items():
                    if status == "healthy":
                        st.success(f"✅ {comp.title()}")
                    else:
                        st.error(f"❌ {comp.title()}")
            else:
                st.error("❌ API недоступен")
        except:
            st.error("❌ Не удается подключиться к API")
        
        # Последние новости
        st.header("📰 Новости")
        st.info("🎉 Новые Showcase команды доступны!")
        st.info("📊 Добавлен мониторинг системы")
        st.info("🚀 Улучшена производительность")

def show_showcase_page():
    """Страница showcase команд"""
    
    st.header("🎯 Showcase Команды")
    st.markdown("**Профессиональные решения для сложных задач**")
    
    # Получаем информацию о showcase командах
    try:
        response = requests.get(f"{API_BASE_URL}/showcase")
        if response.status_code == 200:
            showcase_data = response.json()
            teams = showcase_data["showcase_teams"]
            
            # Выбор команды
            team_options = {
                "swot_analysis": "💼 SWOT-Аналитик",
                "tech_review": "🔬 Технический Рецензент", 
                "investment_advisor": "💰 Инвестиционный Советник"
            }
            
            selected_team = st.selectbox(
                "Выберите showcase команду:",
                options=list(team_options.keys()),
                format_func=lambda x: team_options[x],
                index=0
            )
            
            # Информация о выбранной команде
            team_info = teams[selected_team]
            
            # Карточка команды
            st.markdown(f'''
            <div class="showcase-card">
                <h3>{team_info["name"]}</h3>
                <p><strong>Описание:</strong> {team_info["description"]}</p>
                <p><strong>Время выполнения:</strong> {team_info["estimated_time"]}</p>
                <p><strong>Применение:</strong> {", ".join(team_info["use_cases"])}</p>
            </div>
            ''', unsafe_allow_html=True)
            
            # Форма запуска исследования
            with st.form(f"showcase_form_{selected_team}"):
                st.subheader("📝 Параметры исследования")
                
                # Специализированные поля ввода для каждой команды
                if selected_team == "swot_analysis":
                    topic = st.text_input(
                        "Название компании:",
                        placeholder="Например: Apple, Tesla, Microsoft",
                        help="Введите название компании для SWOT-анализа"
                    )
                    
                elif selected_team == "tech_review":
                    topic = st.text_input(
                        "Ссылка на GitHub репозиторий:",
                        placeholder="https://github.com/user/repository",
                        help="Введите полную ссылку на GitHub репозиторий для анализа"
                    )
                    
                elif selected_team == "investment_advisor":
                    topic = st.text_input(
                        "Тикер акции:",
                        placeholder="Например: AAPL, TSLA, MSFT",
                        help="Введите тикер акции для инвестиционного анализа"
                    ).upper()
                
                # Общие параметры
                col1, col2 = st.columns(2)
                
                with col1:
                    language = st.selectbox(
                        "Язык анализа:",
                        ["ru", "en"],
                        format_func=lambda x: "🇷🇺 Русский" if x == "ru" else "🇺🇸 English"
                    )
                
                with col2:
                    depth = st.selectbox(
                        "Глубина анализа:",
                        ["basic", "standard", "comprehensive"],
                        index=2,
                        format_func=lambda x: {
                            "basic": "🔍 Базовый", 
                            "standard": "📊 Стандартный",
                            "comprehensive": "🎯 Исчерпывающий"
                        }[x]
                    )
                
                # Кнопка запуска
                submitted = st.form_submit_button(
                    f"🚀 Запустить {team_info['name']}",
                    type="primary"
                )
                
                if submitted:
                    if not topic:
                        st.error("⚠️ Пожалуйста, заполните поле ввода")
                    else:
                        start_showcase_research(selected_team, topic, language, depth, team_info)
        
        else:
            st.error("❌ Не удалось загрузить информацию о showcase командах")
            
    except Exception as e:
        st.error(f"❌ Ошибка подключения к API: {str(e)}")

def start_showcase_research(crew_type, topic, language, depth, team_info):
    """Запуск showcase исследования"""
    
    with st.spinner(f"🚀 Запускаем {team_info['name']}..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/research/showcase",
                json={
                    "topic": topic,
                    "crew_type": crew_type,
                    "language": language,
                    "depth": depth
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                task_id = data["task_id"]
                
                st.success(f"✅ {team_info['name']} запущен!")
                st.info(f"🆔 ID задачи: {task_id}")
                st.info(f"⏱️ Ожидаемое время: {data['estimated_time']}")
                
                # Сохраняем в сессии для отслеживания
                if "active_tasks" not in st.session_state:
                    st.session_state.active_tasks = []
                
                st.session_state.active_tasks.append({
                    "task_id": task_id,
                    "crew_type": crew_type,
                    "team_name": team_info['name'],
                    "topic": topic,
                    "started_at": datetime.now(),
                    "estimated_time": data['estimated_time']
                })
                
                # Автоматически переключаемся на мониторинг
                monitor_task_progress(task_id, team_info['name'])
                
            else:
                error_data = response.json()
                st.error(f"❌ Ошибка запуска: {error_data.get('detail', 'Неизвестная ошибка')}")
                
        except Exception as e:
            st.error(f"❌ Ошибка: {str(e)}")

def monitor_task_progress(task_id, team_name):
    """Мониторинг прогресса выполнения задачи"""
    
    st.subheader("📊 Мониторинг выполнения")
    
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    result_placeholder = st.empty()
    
    start_time = time.time()
    
    while True:
        try:
            response = requests.get(f"{API_BASE_URL}/result/{task_id}")
            
            if response.status_code == 200:
                data = response.json()
                status = data["status"]
                progress = data.get("progress", 0)
                
                progress_bar.progress(progress / 100)
                
                elapsed_time = int(time.time() - start_time)
                status_placeholder.info(f"🔄 Статус: {status} | Прошло времени: {elapsed_time}с")
                
                if status == "SUCCESS":
                    st.success(f"🎉 {team_name} завершен успешно!")
                    
                    # Отображаем результат
                    result = data.get("result", "Результат недоступен")
                    
                    with result_placeholder.container():
                        st.markdown('<div class="result-container">', unsafe_allow_html=True)
                        st.subheader("📋 Результат анализа")
                        st.markdown(result)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Кнопки действий
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📥 Скачать результат"):
                                st.download_button(
                                    label="📄 Скачать как текст",
                                    data=result,
                                    file_name=f"{team_name}_{task_id}.txt",
                                    mime="text/plain"
                                )
                        with col2:
                            if st.button("🔄 Новое исследование"):
                                st.rerun()
                        with col3:
                            if st.button("📊 Статистика"):
                                show_task_statistics(data)
                    
                    break
                    
                elif status == "FAILURE":
                    st.error(f"❌ {team_name} завершен с ошибкой")
                    error_info = data.get("error", "Неизвестная ошибка")
                    st.error(f"Ошибка: {error_info}")
                    break
                
                # Обновляем каждые 10 секунд
                time.sleep(10)
                
            else:
                st.error("❌ Ошибка получения статуса задачи")
                break
                
        except Exception as e:
            st.error(f"❌ Ошибка мониторинга: {str(e)}")
            break

def show_task_statistics(task_data):
    """Показать статистику выполненной задачи"""
    
    st.subheader("📊 Статистика задачи")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Статус", task_data.get("status", "N/A"))
    with col2:
        st.metric("Прогресс", f"{task_data.get('progress', 0)}%")
    with col3:
        processing_time = task_data.get("processing_time", 0)
        st.metric("Время выполнения", f"{processing_time:.1f}с")

def show_standard_research_page():
    """Страница стандартных исследований"""
    
    st.header("🔍 Стандартные Исследования")
    st.markdown("**Универсальные команды для различных задач**")
    
    # Стандартные команды
    standard_crews = {
        "general": {
            "name": "🔍 Универсальные исследования",
            "description": "Comprehensive исследования любых тем"
        },
        "business_analysis": {
            "name": "💼 Бизнес-аналитика",
            "description": "Анализ рынков и бизнес-возможностей"
        },
        "seo_content": {
            "name": "📝 SEO контент", 
            "description": "Создание SEO-оптимизированного контента"
        },
        "tech_research": {
            "name": "🔬 Техническое исследование",
            "description": "Глубокий технический анализ"
        },
        "financial_analysis": {
            "name": "💰 Финансовый анализ",
            "description": "Финансовые исследования и анализ рисков"
        }
    }
    
    selected_crew = st.selectbox(
        "Выберите тип исследования:",
        options=list(standard_crews.keys()),
        format_func=lambda x: standard_crews[x]["name"]
    )
    
    crew_info = standard_crews[selected_crew]
    
    # Карточка команды
    st.markdown(f'''
    <div class="standard-card">
        <h3>{crew_info["name"]}</h3>
        <p>{crew_info["description"]}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Форма исследования
    with st.form("standard_research_form"):
        topic = st.text_area(
            "Тема исследования:",
            placeholder="Опишите что вы хотите исследовать...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox("Язык:", ["ru", "en"])
        with col2:
            depth = st.selectbox("Глубина:", ["basic", "standard", "comprehensive"])
        
        submitted = st.form_submit_button("🚀 Запустить исследование")
        
        if submitted:
            if not topic:
                st.error("⚠️ Пожалуйста, укажите тему исследования")
            else:
                start_standard_research(selected_crew, topic, language, depth)

def start_standard_research(crew_type, topic, language, depth):
    """Запуск стандартного исследования"""
    
    with st.spinner("🚀 Запускаем исследование..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/research",
                json={
                    "topic": topic,
                    "crew_type": crew_type,
                    "language": language,
                    "depth": depth
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                task_id = data["task_id"]
                
                st.success("✅ Исследование запущено!")
                st.info(f"🆔 ID задачи: {task_id}")
                
                # Мониторинг прогресса
                monitor_task_progress(task_id, f"Исследование ({crew_type})")
                
            else:
                st.error("❌ Ошибка запуска исследования")
                
        except Exception as e:
            st.error(f"❌ Ошибка: {str(e)}")

def show_monitoring_page():
    """Страница мониторинга системы"""
    
    st.header("📊 Мониторинг Системы")
    
    # Статус системы
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏥 Здоровье системы")
        
        try:
            health_response = requests.get(f"{API_BASE_URL}/health")
            if health_response.status_code == 200:
                health_data = health_response.json()
                
                st.success("✅ Система работает нормально")
                
                # Компоненты
                components = health_data.get("components", {})
                for comp, status in components.items():
                    if status == "healthy":
                        st.success(f"✅ {comp.title()}: {status}")
                    else:
                        st.error(f"❌ {comp.title()}: {status}")
            else:
                st.error("❌ API недоступен")
        except:
            st.error("❌ Не удается подключиться к системе")
    
    with col2:
        st.subheader("📋 Активные задачи")
        
        try:
            tasks_response = requests.get(f"{API_BASE_URL}/tasks")
            if tasks_response.status_code == 200:
                tasks_data = tasks_response.json()
                
                total_active = tasks_data.get("total_active", 0)
                st.metric("Всего активных задач", total_active)
                
                if total_active > 0:
                    st.info(f"В системе выполняется {total_active} задач(и)")
                else:
                    st.success("Нет активных задач")
            else:
                st.error("❌ Не удалось получить информацию о задачах")
        except:
            st.error("❌ Ошибка получения данных о задачах")
    
    # Активные задачи в сессии
    if "active_tasks" in st.session_state and st.session_state.active_tasks:
        st.subheader("📋 Ваши задачи в этой сессии")
        
        for task in st.session_state.active_tasks:
            with st.expander(f"{task['team_name']} - {task['topic'][:50]}..."):
                st.write(f"🆔 ID: {task['task_id']}")
                st.write(f"⏰ Запущено: {task['started_at'].strftime('%H:%M:%S')}")
                st.write(f"⏱️ Ожидаемое время: {task['estimated_time']}")
                
                if st.button(f"🔍 Проверить статус", key=task['task_id']):
                    check_task_status(task['task_id'])

def check_task_status(task_id):
    """Проверка статуса задачи"""
    
    try:
        response = requests.get(f"{API_BASE_URL}/result/{task_id}")
        if response.status_code == 200:
            data = response.json()
            status = data["status"]
            progress = data.get("progress", 0)
            
            if status == "SUCCESS":
                st.success(f"✅ Задача завершена успешно! (Прогресс: {progress}%)")
            elif status == "FAILURE":
                st.error(f"❌ Задача завершена с ошибкой: {data.get('error', 'Неизвестная ошибка')}")
            else:
                st.info(f"🔄 Задача в процессе выполнения (Прогресс: {progress}%)")
        else:
            st.error("❌ Не удалось получить статус задачи")
    except:
        st.error("❌ Ошибка проверки статуса")

def show_help_page():
    """Страница справки"""
    
    st.header("❓ Справка и документация")
    
    st.markdown("""
    ## 🎯 Showcase Команды
    
    ### 💼 SWOT-Аналитик
    **Что делает:** Проводит comprehensive SWOT-анализ компаний
    **Как использовать:** Введите название компании (например: Apple, Tesla)
    **Результат:** Детальный анализ сильных/слабых сторон и рекомендации
    
    ### 🔬 Технический Рецензент  
    **Что делает:** Анализирует GitHub репозитории на качество кода
    **Как использовать:** Введите полную ссылку на GitHub репозиторий
    **Результат:** Техническая рецензия с оценкой архитектуры и безопасности
    
    ### 💰 Инвестиционный Советник
    **Что делает:** Анализирует акции и дает инвестиционные рекомендации  
    **Как использовать:** Введите тикер акции (например: AAPL, MSFT)
    **Результат:** Инвестиционная рекомендация с анализом рисков
    
    ## 🔍 Стандартные Команды
    
    - **Универсальные исследования** - для любых тем
    - **Бизнес-аналитика** - анализ рынков и возможностей
    - **SEO контент** - создание оптимизированного контента
    - **Техническое исследование** - глубокий технический анализ
    - **Финансовый анализ** - финансовые исследования
    
    ## 🆘 Поддержка
    
    Если у вас возникли проблемы:
    1. Проверьте статус системы в разделе "Мониторинг"
    2. Убедитесь что API сервер запущен на localhost:8000
    3. Проверьте правильность ввода данных
    
    ## 🔗 Полезные ссылки
    
    - [GitHub Repository](https://github.com/miniduck-beep/ai-agent-farm)
    - [API Документация](http://localhost:8000/docs)
    - [Grafana Dashboard](http://localhost:3000)
    """)

if __name__ == "__main__":
    main()
