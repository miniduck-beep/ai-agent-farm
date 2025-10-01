import streamlit as st
from app.tasks import run_research_crew

st.set_page_config(page_title="?? Ферма ИИ-агентов", layout="wide")

st.title("?? Ферма ИИ-агентов")
st.subheader("На базе CrewAI, Gemini и Celery")

with st.form("research_form"):
    topic = st.text_input(
        "Введите тему для глубокого исследования:",
        placeholder="Например: 'Перспективы использования графена в аккумуляторах'"
    )
    submitted = st.form_submit_button("?? Начать исследование")

if submitted and topic:
    st.info("Ваша задача принята в работу. Это может занять 10-20 минут.")
    st.write(f"Тема исследования: **{topic}**")

    # Отправляем задачу в Celery
    task = run_research_crew.delay(topic)

    st.success(f"Задача успешно отправлена! ID задачи: {task.id}")
    st.warning(
        "Пока что этот интерфейс только запускает задачи. "
        "Чтобы увидеть результат, вам нужно посмотреть логи Celery воркера."
    )
    st.code(f"docker compose logs -f worker", language="bash")