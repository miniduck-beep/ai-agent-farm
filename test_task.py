from app.tasks import run_research_crew

# Простая тестовая задача
print("🧪 Запуск тестовой задачи...")
print("Тема: Искусственный интеллект в медицине")

try:
    # Запускаем задачу синхронно для тестирования
    task = run_research_crew.delay("Искусственный интеллект в медицине")
    print(f"✅ Задача успешно отправлена! ID: {task.id}")
    print("🔄 Задача выполняется в фоновом режиме...")
    print("Проверьте логи командой: docker compose logs -f worker")
except Exception as e:
    print(f"❌ Ошибка при отправке задачи: {e}")
