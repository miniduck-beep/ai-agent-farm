import streamlit as st
import time
import json
import redis
from app.tasks import run_research_crew
from datetime import datetime, timedelta

# Настройка страницы
st.set_page_config(
    page_title="🤖 Ферма ИИ-агентов", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Подключение к Redis для мониторинга
@st.cache_resource
def get_redis_client():
    return redis.Redis(host='redis', port=6379, decode_responses=True)

redis_client = get_redis_client()

st.title("🤖 Ферма ИИ-агентов")
st.subheader("На базе CrewAI, Gemini 2.5 Flash и Celery")

# Боковая панель с мониторингом
with st.sidebar:
    st.header("📊 Мониторинг системы")
    
    # Статус системы
    queue_length = 0
    try:
        queue_length = redis_client.llen('celery')
    except:
        pass
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Задач в очереди", queue_length)
    with col2:
        st.metric("Статус VPN", "🟢 Активен")
    
    # Активные задачи
    st.subheader("🔄 Активные задачи")
    try:
        task_keys = redis_client.keys("celery-task-meta-*")
        if task_keys:
            for key in task_keys[-3:]:  # Показываем последние 3
                task_id = key.replace("celery-task-meta-", "")
                task_info = redis_client.get(key)
                if task_info:
                    try:
                        task_data = json.loads(task_info)
                        status = task_data.get('status', 'UNKNOWN')
                        
                        if status == 'PENDING':
                            st.write(f"⏳ {task_id[:8]}... - Ожидание")
                        elif status == 'STARTED':
                            st.write(f"🔄 {task_id[:8]}... - Выполняется")
                        elif status == 'SUCCESS':
                            st.write(f"✅ {task_id[:8]}... - Завершено")
                        elif status == 'FAILURE':
                            st.write(f"❌ {task_id[:8]}... - Ошибка")
                    except:
                        st.write(f"📋 {task_id[:8]}... - В процессе")
        else:
            st.write("Нет активных задач")
    except:
        st.write("Нет подключения к Redis")

# Основной интерфейс
col1, col2 = st.columns([2, 1])

with col1:
    with st.form("research_form"):
        st.subheader("🚀 Запуск исследования")
        
        topic = st.text_input(
            "Введите тему для глубокого исследования:",
            placeholder="Например: 'Перспективы использования графена в аккумуляторах'",
            help="ИИ-агенты проведут комплексное исследование темы с использованием поиска в интернете"
        )
        
        submitted = st.form_submit_button("🎯 Начать исследование", use_container_width=True)

with col2:
    st.subheader("ℹ️ Как это работает")
    st.info("""
    **1. Отправка задачи**
    Ваш запрос попадает в очередь
    
    **2. Агент-исследователь**
    Ищет информацию в интернете
    
    **3. Агент-писатель**
    Создает структурированный отчет
    
    **4. Готовый результат**
    Появляется ниже на странице
    """)

# Обработка отправленной формы
if submitted and topic:
    st.success(f"✅ Задача принята: **{topic}**")
    
    # Отправляем задачу в Celery
    with st.spinner("Отправка задачи в очередь..."):
        task = run_research_crew.delay(topic)
        task_id = task.id
    
    st.info(f"🆔 ID задачи: `{task_id}`")
    
    # Создаем контейнеры для обновления статуса
    status_container = st.empty()
    progress_container = st.empty()
    result_container = st.empty()
    
    # Мониторинг выполнения задачи
    start_time = time.time()
    max_wait_time = 300  # 5 минут максимум ожидания
    
    while True:
        current_time = time.time()
        elapsed = current_time - start_time
        
        # Проверяем статус задачи
        try:
            task_info = redis_client.get(f"celery-task-meta-{task_id}")
            if task_info:
                task_data = json.loads(task_info)
                status = task_data.get('status', 'PENDING')
                result = task_data.get('result', None)
                
                # Обновляем прогресс
                progress_value = min(elapsed / 120.0, 0.95)  # Предполагаем ~2 минуты на задачу
                progress_container.progress(progress_value, f"⏱️ Выполняется: {int(elapsed)}с")
                
                if status == 'SUCCESS':
                    progress_container.progress(1.0, "✅ Задача завершена!")
                    status_container.success("🎉 Исследование завершено успешно!")
                    
                    if result:
                        result_container.markdown("### 📋 Результат исследования")
                        result_container.markdown(result)
                    break
                    
                elif status == 'FAILURE':
                    progress_container.empty()
                    error_msg = task_data.get('traceback', 'Неизвестная ошибка')
                    status_container.error(f"❌ Ошибка при выполнении: {error_msg}")
                    break
                    
                elif status == 'STARTED':
                    status_container.info("🔄 Агенты работают над исследованием...")
                    
                else:  # PENDING
                    status_container.info("⏳ Задача в очереди, ожидание обработки...")
                    
        except Exception as e:
            status_container.warning(f"⚠️ Ошибка мониторинга: {str(e)}")
        
        # Таймаут
        if elapsed > max_wait_time:
            status_container.warning("⏰ Превышено время ожидания. Задача может выполняться в фоне.")
            break
            
        # Обновляем каждые 3 секунды
        time.sleep(3)

# Секция с последними результатами
st.markdown("---")
st.subheader("📚 Последние исследования")

try:
    task_keys = redis_client.keys("celery-task-meta-*")
    if task_keys:
        # Сортируем по времени (последние сначала)
        task_keys = sorted(task_keys, reverse=True)[:5]
        
        for key in task_keys:
            task_id = key.replace("celery-task-meta-", "")
            task_info = redis_client.get(key)
            
            if task_info:
                try:
                    task_data = json.loads(task_info)
                    status = task_data.get('status', 'UNKNOWN')
                    result = task_data.get('result', '')
                    
                    if status == 'SUCCESS' and result:
                        with st.expander(f"✅ Задача {task_id[:8]}... (Завершено)", expanded=False):
                            # Извлекаем тему из результата если возможно
                            lines = result.split('\n')
                            title = lines[0] if lines else f"Исследование {task_id[:8]}"
                            
                            st.markdown(f"**ID задачи:** `{task_id}`")
                            st.markdown(result[:2000] + ("..." if len(result) > 2000 else ""))
                            
                except json.JSONDecodeError:
                    continue
    else:
        st.info("Пока нет завершенных исследований. Создайте первое!")
        
except Exception as e:
    st.warning(f"Не удалось загрузить историю: {str(e)}")

# Нижняя панель с информацией
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🔧 Технологии:**
    - Gemini 2.5 Flash
    - CrewAI Agents  
    - VLESS VPN
    """)

with col2:
    st.markdown("""
    **⚡ Возможности:**
    - Интернет поиск
    - Анализ источников
    - Структурированные отчеты
    """)

with col3:
    st.markdown("""
    **📊 Мониторинг:**
    - Статус в реальном времени
    - История задач
    - Системные метрики
    """)
