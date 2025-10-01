import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_google_genai import ChatGoogleGenerativeAI

def create_research_crew(topic):
    """
    Создает и настраивает команду агентов для исследования заданной темы.
    """
    print(f"🚀 [СТАРТ] Инициализация исследования темы: '{topic}'")
    
    # Инициализация LLM с использованием Gemini 2.5 Flash (стабильная версия)
    print("🤖 [LLM] Инициализация Gemini 2.5 Flash...")
    try:
        # Используем стабильную модель без beta API
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        print("✅ [LLM] Gemini 2.5 Flash успешно инициализирован")
    except Exception as e:
        print(f"❌ [LLM] Ошибка инициализации Gemini 2.5 Flash: {e}")
        print("🔄 [LLM] Попытка использования текстовой модели...")
        try:
            llm = ChatGoogleGenerativeAI(
                model="text-bison-001",
                temperature=0.7,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
            print("✅ [LLM] Fallback модель успешно инициализирована")
        except Exception as e2:
            print(f"❌ [LLM] Критическая ошибка: {e2}")
            raise e2

    # Инициализация инструментов
    print("🔧 [TOOLS] Инициализация инструментов поиска...")
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    print("✅ [TOOLS] Инструменты готовы")

    # Агент 1: Старший исследователь
    print("👨‍🔬 [AGENT] Создание агента-исследователя...")
    researcher = Agent(
        role='Старший научный сотрудник',
        goal=f'Найти и проанализировать самую свежую и важную информацию по теме: {topic}',
        backstory=(
            'Вы - опытный исследователь с многолетним стажем в анализе технологических трендов. '
            'Ваша задача - копать глубоко, находить скрытые жемчужины информации и '
            'отделять факты от шума.'
        ),
        verbose=True,
        allow_delegation=False,
        tools=[search_tool, scrape_tool],
        llm=llm
    )

    # Агент 2: Писатель-аналитик
    print("✍️ [AGENT] Создание агента-писателя...")
    writer = Agent(
        role='Профессиональный технический писатель',
        goal=f'Написать увлекательный и информативный отчет по теме: {topic}',
        backstory=(
            'Вы - писатель, который умеет превращать сложные технические данные в понятный '
            'и структурированный текст. Ваша цель - создать отчет, который будет легко '
            'читаться и содержать все ключевые выводы исследования.'
        ),
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    # Задача для исследователя
    print("📋 [TASK] Создание задачи для исследователя...")
    task_research = Task(
        description=(
            f'Провести всестороннее исследование темы "{topic}". '
            'Найди ключевые тренды, главных игроков, потенциальные риски и возможности. '
            'Собери ссылки на самые авторитетные источники.'
        ),
        expected_output='Подробный отчет с анализом и ссылками на источники.',
        agent=researcher
    )

    # Задача для писателя
    print("📋 [TASK] Создание задачи для писателя...")
    task_write = Task(
        description=(
            'На основе отчета исследователя напиши финальный структурированный отчет. '
            'Отчет должен включать введение, основные тезисы (3-5 пунктов), '
            'детальный анализ по каждому тезису и заключение с прогнозом.'
        ),
        expected_output=f'Хорошо отформатированный итоговый отчет по теме {topic}.',
        agent=writer
    )

    # Сборка команды
    print("⚡ [CREW] Создание команды агентов...")
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task_research, task_write],
        process=Process.sequential
    )

    # Запуск работы
    print("🎯 [START] Запуск работы команды...")
    print("=" * 60)
    result = crew.kickoff()
    print("=" * 60)
    print("🏁 [FINISH] Работа команды завершена!")
    return result
