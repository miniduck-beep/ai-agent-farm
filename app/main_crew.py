"""
AI Agent Farm - Dynamic Crew Factory
====================================
Интеллектуальная фабрика для создания специализированных команд агентов
"""

import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool
from app.config import settings
import logging

# Настройка логирования
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Инициализация LLM
def get_llm():
    """Создает и возвращает настроенную LLM"""
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=settings.gemini_temperature,
        google_api_key=settings.google_api_key
    )

# Инициализация инструментов
def get_tools():
    """Создает и возвращает набор инструментов для агентов"""
    tools = []
    
    if settings.serper_api_key:
        search_tool = SerperDevTool(api_key=settings.serper_api_key)
        tools.append(search_tool)
        
    return tools

class CrewFactory:
    """Фабрика для создания специализированных команд агентов"""
    
    def __init__(self):
        self.llm = get_llm()
        self.tools = get_tools()
        
    def create_business_analysis_crew(self) -> Crew:
        """Создает команду для бизнес-анализа и исследований рынка"""
        
        # Аналитик рынка
        market_analyst = Agent(
            role='Старший аналитик рынка',
            goal='Провести глубокий анализ рынка и конкурентной среды',
            backstory="""Вы - опытный аналитик с 15-летним стажем в исследовании рынков. 
            Специализируетесь на анализе конкурентов, рыночных трендов и потребительского поведения. 
            Умеете находить скрытые возможности и риски.""",
            verbose=True,
            allow_delegation=True,
            tools=self.tools,
            llm=self.llm
        )
        
        # Финансовый аналитик
        financial_analyst = Agent(
            role='Финансовый аналитик',
            goal='Провести финансовый анализ и оценку инвестиционной привлекательности',
            backstory="""Вы - сертифицированный финансовый аналитик (CFA) с глубокими знаниями 
            в области корпоративных финансов, оценки бизнеса и инвестиционного анализа. 
            Специализируетесь на анализе рентабельности и рисков.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        # Стратегический консультант
        strategy_consultant = Agent(
            role='Стратегический консультант',
            goal='Разработать стратегические рекомендации и план действий',
            backstory="""Вы - старший партнер консалтинговой компании с опытом работы 
            с Fortune 500 компаниями. Специализируетесь на разработке бизнес-стратегий, 
            организационных изменениях и цифровой трансформации.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        return Crew(
            agents=[market_analyst, financial_analyst, strategy_consultant],
            tasks=[],  # Задачи будут созданы динамически
            process=Process.sequential,
            verbose=True
        )
    
    def create_seo_content_crew(self) -> Crew:
        """Создает команду для SEO и контент-стратегии"""
        
        # SEO специалист
        seo_specialist = Agent(
            role='SEO-эксперт',
            goal='Провести SEO-анализ и разработать стратегию продвижения',
            backstory="""Вы - сертифицированный SEO-эксперт с 10-летним опытом. 
            Специализируетесь на техническом SEO, анализе ключевых слов и конкурентном анализе. 
            Отлично знаете алгоритмы Google и современные тренды в поисковой оптимизации.""",
            verbose=True,
            allow_delegation=True,
            tools=self.tools,
            llm=self.llm
        )
        
        # Контент-стратег
        content_strategist = Agent(
            role='Контент-стратег',
            goal='Разработать контент-стратегию и план создания контента',
            backstory="""Вы - опытный контент-стратег с опытом работы в digital-агентствах. 
            Специализируетесь на создании контент-планов, editorial календарей и стратегий 
            для различных каналов продвижения.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        # Digital-маркетолог
        digital_marketer = Agent(
            role='Digital-маркетолог',
            goal='Разработать комплексную digital-стратегию продвижения',
            backstory="""Вы - performance-маркетолог с опытом запуска и оптимизации 
            рекламных кампаний в Google Ads, Yandex Direct, социальных сетях. 
            Специализируетесь на conversion optimization и аналитике.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        return Crew(
            agents=[seo_specialist, content_strategist, digital_marketer],
            tasks=[],
            process=Process.sequential,
            verbose=True
        )
    
    def create_tech_research_crew(self) -> Crew:
        """Создает команду для технических исследований"""
        
        # Технический исследователь
        tech_researcher = Agent(
            role='Старший технический исследователь',
            goal='Провести исследование технологических трендов и решений',
            backstory="""Вы - ведущий технический эксперт с PhD в Computer Science. 
            Специализируетесь на анализе emerging technologies, архитектурных решений 
            и технологических трендов. Имеете опыт в AI/ML, blockchain, cloud computing.""",
            verbose=True,
            allow_delegation=True,
            tools=self.tools,
            llm=self.llm
        )
        
        # Архитектор решений
        solution_architect = Agent(
            role='Архитектор решений',
            goal='Разработать техническую архитектуру и рекомендации по реализации',
            backstory="""Вы - enterprise архитектор с 15+ лет опыта проектирования 
            масштабируемых систем. Специализируетесь на микросервисной архитектуре, 
            cloud-native решениях и DevOps практиках.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        # DevOps инженер
        devops_engineer = Agent(
            role='DevOps инженер',
            goal='Разработать план внедрения и эксплуатации решения',
            backstory="""Вы - senior DevOps инженер с опытом автоматизации CI/CD, 
            контейнеризации и оркестрации. Специализируетесь на Kubernetes, Docker, 
            мониторинге и обеспечении высокой доступности систем.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        return Crew(
            agents=[tech_researcher, solution_architect, devops_engineer],
            tasks=[],
            process=Process.sequential,
            verbose=True
        )
    
    def create_financial_analysis_crew(self) -> Crew:
        """Создает команду для финансового анализа"""
        
        # Финансовый аналитик
        financial_analyst = Agent(
            role='Старший финансовый аналитик',
            goal='Провести комплексный финансовый анализ и оценку',
            backstory="""Вы - CFA с MBA в Finance, имеете 12+ лет опыта в инвестиционном 
            банкинге и корпоративных финансах. Специализируетесь на DCF моделировании, 
            comparable analysis и оценке рисков.""",
            verbose=True,
            allow_delegation=True,
            tools=self.tools,
            llm=self.llm
        )
        
        # Аналитик рисков
        risk_analyst = Agent(
            role='Аналитик рисков',
            goal='Оценить финансовые и операционные риски',
            backstory="""Вы - сертифицированный риск-менеджер (FRM) с опытом работы 
            в крупных банках и страховых компаниях. Специализируетесь на credit risk, 
            market risk и operational risk management.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        # Инвестиционный советник
        investment_advisor = Agent(
            role='Инвестиционный советник',
            goal='Дать рекомендации по инвестиционным решениям',
            backstory="""Вы - портфельный менеджер с опытом управления активами 
            на $500M+. Специализируетесь на asset allocation, alternative investments 
            и ESG investing.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        return Crew(
            agents=[financial_analyst, risk_analyst, investment_advisor],
            tasks=[],
            process=Process.sequential,
            verbose=True
        )
    
    def create_general_crew(self) -> Crew:
        """Создает универсальную команду (по умолчанию)"""
        
        # Исследователь
        researcher = Agent(
            role='Старший исследователь',
            goal='Найти и проанализировать актуальную информацию по теме',
            backstory="""Вы опытный исследователь с навыками работы в различных областях. 
            Умеете быстро находить релевантную информацию, анализировать данные и 
            делать обоснованные выводы.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        # Писатель
        writer = Agent(
            role='Технический писатель',
            goal='Создать структурированный и понятный отчет',
            backstory="""Вы профессиональный технический писатель с опытом создания 
            аналитических отчетов, документации и презентаций. Умеете излагать сложные 
            концепции простым и понятным языком.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
        
        return Crew(
            agents=[researcher, writer],
            tasks=[],
            process=Process.sequential,
            verbose=True
        )

# Глобальная фабрика
crew_factory = CrewFactory()

def create_dynamic_tasks(crew: Crew, topic: str, crew_type: str, language: str = "ru", depth: str = "standard") -> list:
    """Создает динамические задачи для команды в зависимости от типа"""
    
    tasks = []
    agents = crew.agents
    
    # Определяем глубину анализа
    depth_instructions = {
        "basic": "Проведите краткий анализ основных аспектов",
        "standard": "Проведите детальное исследование с анализом ключевых факторов", 
        "comprehensive": "Проведите исчерпывающий анализ со всеми важными деталями"
    }
    
    depth_instruction = depth_instructions.get(depth, depth_instructions["standard"])
    
    if crew_type == "business_analysis":
        # Задачи для бизнес-анализа
        tasks = [
            Task(
                description=f"""
                {depth_instruction} рынка по теме: {topic}
                
                Ваша задача:
                1. Проанализируйте размер и динамику рынка
                2. Определите ключевых игроков и их позиции
                3. Выявите основные тренды и драйверы роста
                4. Оцените барьеры входа и конкурентную среду
                5. Проанализируйте целевую аудиторию и потребности
                
                Результат на языке: {language}
                """,
                agent=agents[0],
                expected_output="Детальный анализ рынка с ключевыми инсайтами"
            ),
            Task(
                description=f"""
                Проведите финансовый анализ по теме: {topic}
                
                На основе рыночного анализа:
                1. Оцените финансовую привлекательность направления
                2. Проанализируйте структуру затрат и источники дохода
                3. Рассчитайте ключевые финансовые метрики
                4. Оцените инвестиционные риски и возможности
                5. Определите точки безубыточности и ROI
                
                Результат на языке: {language}
                """,
                agent=agents[1],
                expected_output="Финансовый анализ с метриками и рекомендациями"
            ),
            Task(
                description=f"""
                Разработайте стратегические рекомендации по теме: {topic}
                
                На основе рыночного и финансового анализа:
                1. Сформулируйте стратегические возможности
                2. Предложите план действий с приоритетами
                3. Определите ключевые факторы успеха
                4. Разработайте roadmap внедрения
                5. Предложите метрики для отслеживания прогресса
                
                Результат на языке: {language}
                """,
                agent=agents[2],
                expected_output="Стратегические рекомендации и план действий"
            )
        ]
        
    elif crew_type == "seo_content":
        # Задачи для SEO и контента
        tasks = [
            Task(
                description=f"""
                {depth_instruction} SEO-возможностей по теме: {topic}
                
                Ваша задача:
                1. Проанализируйте ключевые слова и поисковые запросы
                2. Оцените конкуренцию в поисковой выдаче
                3. Найдите gaps в контенте конкурентов
                4. Определите возможности для featured snippets
                5. Предложите техническую SEO-стратегию
                
                Результат на языке: {language}
                """,
                agent=agents[0],
                expected_output="SEO-анализ с рекомендациями по оптимизации"
            ),
            Task(
                description=f"""
                Разработайте контент-стратегию по теме: {topic}
                
                На основе SEO-анализа:
                1. Создайте контент-план на 3 месяца
                2. Определите форматы контента и каналы
                3. Разработайте editorial календарь
                4. Предложите темы для статей и материалов
                5. Создайте guidelines для создания контента
                
                Результат на языке: {language}
                """,
                agent=agents[1],
                expected_output="Контент-стратегия с планом и календарем"
            ),
            Task(
                description=f"""
                Создайте digital-стратегию продвижения по теме: {topic}
                
                На основе SEO и контент-анализа:
                1. Предложите каналы digital-продвижения
                2. Разработайте стратегию социальных сетей
                3. Создайте план рекламных кампаний
                4. Определите KPI и метрики эффективности
                5. Рассчитайте бюджеты и ROI прогнозы
                
                Результат на языке: {language}
                """,
                agent=agents[2],
                expected_output="Digital-стратегия с планом продвижения"
            )
        ]
        
    elif crew_type == "tech_research":
        # Задачи для технических исследований
        tasks = [
            Task(
                description=f"""
                {depth_instruction} технологических решений по теме: {topic}
                
                Ваша задача:
                1. Исследуйте современные технологии в области
                2. Проанализируйте emerging trends и инновации
                3. Сравните альтернативные подходы и решения
                4. Оцените зрелость технологий и готовность к внедрению
                5. Определите технологические риски и ограничения
                
                Результат на языке: {language}
                """,
                agent=agents[0],
                expected_output="Технологический обзор с анализом решений"
            ),
            Task(
                description=f"""
                Спроектируйте техническую архитектуру для: {topic}
                
                На основе технологического исследования:
                1. Предложите архитектурный подход и паттерны
                2. Определите компоненты системы и их взаимодействие
                3. Выберите технологический стек
                4. Спроектируйте масштабируемость и отказоустойчивость
                5. Создайте диаграммы архитектуры
                
                Результат на языке: {language}
                """,
                agent=agents[1],
                expected_output="Техническая архитектура с диаграммами"
            ),
            Task(
                description=f"""
                Разработайте план внедрения и эксплуатации для: {topic}
                
                На основе архитектурного решения:
                1. Создайте план поэтапного внедрения
                2. Определите требования к инфраструктуре
                3. Спроектируйте CI/CD pipeline
                4. Разработайте стратегию мониторинга и логирования
                5. Создайте план disaster recovery
                
                Результат на языке: {language}
                """,
                agent=agents[2],
                expected_output="План внедрения и эксплуатации"
            )
        ]
        
    elif crew_type == "financial_analysis":
        # Задачи для финансового анализа
        tasks = [
            Task(
                description=f"""
                {depth_instruction} финансовых аспектов по теме: {topic}
                
                Ваша задача:
                1. Проанализируйте финансовые показатели и метрики
                2. Проведите сравнительный анализ с benchmarks
                3. Создайте финансовую модель и прогнозы
                4. Рассчитайте стоимость и оценку
                5. Определите ключевые value drivers
                
                Результат на языке: {language}
                """,
                agent=agents[0],
                expected_output="Финансовый анализ с моделью и оценкой"
            ),
            Task(
                description=f"""
                Оцените риски по теме: {topic}
                
                На основе финансового анализа:
                1. Идентифицируйте финансовые и операционные риски
                2. Проведите количественную оценку рисков
                3. Создайте risk-reward профиль
                4. Предложите методы хеджирования рисков
                5. Разработайте план управления рисками
                
                Результат на языке: {language}
                """,
                agent=agents[1],
                expected_output="Анализ рисков с планом управления"
            ),
            Task(
                description=f"""
                Дайте инвестиционные рекомендации по теме: {topic}
                
                На основе финансового анализа и оценки рисков:
                1. Сформулируйте инвестиционный тезис
                2. Определите оптимальную структуру инвестиций
                3. Рассчитайте ожидаемую доходность и риски
                4. Предложите exit стратегии
                5. Создайте рекомендации по portfolio allocation
                
                Результат на языке: {language}
                """,
                agent=agents[2],
                expected_output="Инвестиционные рекомендации с обоснованием"
            )
        ]
    
    else:  # general crew
        # Универсальные задачи
        tasks = [
            Task(
                description=f"""
                {depth_instruction} по теме: {topic}
                
                Проведите комплексное исследование:
                1. Найдите и проанализируйте актуальную информацию
                2. Выделите ключевые факты и тренды
                3. Проанализируйте различные точки зрения
                4. Сделайте обоснованные выводы
                5. Определите практические рекомендации
                
                Результат на языке: {language}
                """,
                agent=agents[0],
                expected_output="Исследовательский анализ с ключевыми инсайтами"
            ),
            Task(
                description=f"""
                Создайте структурированный отчет по теме: {topic}
                
                На основе проведенного исследования:
                1. Структурируйте информацию логично и понятно
                2. Создайте executive summary
                3. Добавьте графики и визуализации (текстовые)
                4. Сформулируйте actionable рекомендации
                5. Добавьте заключение с следующими шагами
                
                Результат на языке: {language}
                """,
                agent=agents[1],
                expected_output="Структурированный отчет с рекомендациями"
            )
        ]
    
    # Добавляем задачи к команде
    crew.tasks = tasks
    return tasks

def run_research(topic: str, crew_type: str = "general", language: str = "ru", depth: str = "standard") -> str:
    """Запускает исследование с выбранной командой агентов"""
    
    try:
        logger.info(f"🚀 Запуск исследования: {topic} (тип: {crew_type}, язык: {language}, глубина: {depth})")
        
        # Создаем команду нужного типа
        if crew_type == "business_analysis":
            crew = crew_factory.create_business_analysis_crew()
        elif crew_type == "seo_content":
            crew = crew_factory.create_seo_content_crew()
        elif crew_type == "tech_research":
            crew = crew_factory.create_tech_research_crew()
        elif crew_type == "financial_analysis":
            crew = crew_factory.create_financial_analysis_crew()
        else:
            crew = crew_factory.create_general_crew()
            
        # Создаем динамические задачи
        create_dynamic_tasks(crew, topic, crew_type, language, depth)
        
        logger.info(f"📋 Создана команда {crew_type} с {len(crew.tasks)} задачами")
        
        # Запускаем исследование
        result = crew.kickoff()
        
        logger.info(f"✅ Исследование завершено успешно")
        return str(result)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при выполнении исследования: {str(e)}")
        raise e

# Для обратной совместимости
def main_research(topic: str) -> str:
    """Совместимость со старым API"""
    return run_research(topic, "general", "ru", "standard")

if __name__ == "__main__":
    # Тестирование фабрики команд
    test_topic = "Анализ рынка электромобилей"
    result = run_research(test_topic, "business_analysis", "ru", "comprehensive")
    print(result)
