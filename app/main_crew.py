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

# ===============================
# 🎯 ВИТРИНА РЕШЕНИЙ - Advanced Specialized Teams
# ===============================

class CrewShowcase:
    """Showcase команды для демонстрации возможностей AI Agent Farm"""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def create_swot_analyst_crew(self):
        """
        💼 SWOT-Аналитик - Команда для проведения SWOT-анализа компаний
        
        Принимает: Название компании
        Выдает: Детальный SWOT-анализ с рекомендациями
        """
        
        # 🔍 Исследователь рынка
        market_researcher = Agent(
            role='Market Research Analyst',
            goal='Провести comprehensive исследование рынка и позиции компании',
            backstory="""Вы опытный аналитик рынка с 15+ лет опыта в исследовании компаний 
            различных отраслей. Специализируетесь на анализе конкурентного окружения, 
            рыночных трендов и позиционировании компаний. Ваши исследования используются 
            для принятия стратегических решений.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )
        
        # 💰 Финансовый аналитик
        financial_analyst = Agent(
            role='Financial Analyst',
            goal='Анализ финансового состояния и перспектив компании',
            backstory="""Вы senior финансовый аналитик с экспертизой в области 
            корпоративных финансов, оценки активов и анализа финансовой отчетности. 
            Специализируетесь на выявлении финансовых рисков и возможностей. 
            Ваши анализы помогают инвесторам принимать обоснованные решения.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )
        
        # 🎯 Стратегический консультант
        strategy_consultant = Agent(
            role='Strategic Business Consultant',
            goal='Синтез SWOT-анализа и разработка стратегических рекомендаций',
            backstory="""Вы ведущий стратегический консультант McKinsey с опытом 
            работы с Fortune 500 компаниями. Специализируетесь на разработке 
            бизнес-стратегий, цифровой трансформации и операционной эффективности. 
            Ваши рекомендации помогают компаниям достигать устойчивого роста.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=self.tools
        )
        
        return Crew(
            agents=[market_researcher, financial_analyst, strategy_consultant],
            tasks=[],  # Задачи будут созданы динамически
            verbose=2,
            process=Process.sequential
        )
    
    def create_tech_reviewer_crew(self):
        """
        🔬 Технический Рецензент - Команда для анализа GitHub репозиториев
        
        Принимает: Ссылку на GitHub репозиторий
        Выдает: Техническую рецензию на код с рекомендациями
        """
        
        # 👨‍💻 Архитектор ПО
        software_architect = Agent(
            role='Senior Software Architect',
            goal='Анализ архитектуры и структуры кодовой базы',
            backstory="""Вы senior software architect с 20+ лет опыта в разработке 
            enterprise систем. Эксперт в области системного дизайна, паттернов 
            проектирования и best practices. Специализируетесь на анализе 
            масштабируемости, maintainability и технического долга.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )
        
        # 🛡️ Security-эксперт
        security_expert = Agent(
            role='Cybersecurity Expert',
            goal='Анализ безопасности кода и выявление уязвимостей',
            backstory="""Вы certified ethical hacker (CEH) и security consultant 
            с глубокой экспертизой в области application security. Специализируетесь 
            на статическом анализе кода, OWASP Top 10, и secure coding practices. 
            Ваши аудиты предотвращают критические security инциденты.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )
        
        # 📊 Code Quality Analyst
        quality_analyst = Agent(
            role='Code Quality & DevOps Analyst',
            goal='Оценка качества кода, тестирования и DevOps практик',
            backstory="""Вы DevOps engineer и code quality advocate с expertise в области 
            CI/CD, automated testing, и code review processes. Специализируетесь на 
            анализе test coverage, code complexity, и deployment practices. 
            Помогаете командам достигать high-quality deliverables.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=self.tools
        )
        
        return Crew(
            agents=[software_architect, security_expert, quality_analyst],
            tasks=[],
            verbose=2,
            process=Process.sequential
        )
    
    def create_investment_advisor_crew(self):
        """
        💰 Инвестиционный Советник - Команда для анализа инвестиций
        
        Принимает: Тикер акции (например, AAPL, TSLA)
        Выдает: Инвестиционный анализ с рекомендациями
        """
        
        # 📰 Аналитик новостей
        news_analyst = Agent(
            role='Financial News & Sentiment Analyst',
            goal='Анализ новостей, настроений рынка и медиа-активности',
            backstory="""Вы expert в области financial journalism и sentiment analysis 
            с background в data science. Специализируетесь на анализе новостных потоков, 
            social media sentiment, и их влияния на цены акций. Ваши инсайты используются 
            hedge funds для принятия торговых решений.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )
        
        # 📊 Фундаментальный аналитик
        fundamental_analyst = Agent(
            role='Fundamental Analysis Specialist',
            goal='Фундаментальный анализ финансовых показателей компании',
            backstory="""Вы CFA charterholder и senior equity research analyst 
            с опытом работы в Goldman Sachs. Специализируетесь на фундаментальном 
            анализе, financial modeling, и equity valuation. Ваши отчеты влияют 
            на инвестиционные решения institutional investors.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )
        
        # 📈 Технический аналитик
        technical_analyst = Agent(
            role='Technical Analysis & Risk Assessment Expert',
            goal='Технический анализ и оценка рисков инвестиций',
            backstory="""Вы professional trader и CMT (Chartered Market Technician) 
            с 12+ лет опыта в техническом анализе финансовых рынков. Эксперт в области 
            chart patterns, technical indicators, и risk management. Ваши прогнозы 
            помогают optimize entry/exit points для инвестиций.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=self.tools
        )
        
        return Crew(
            agents=[news_analyst, fundamental_analyst, technical_analyst],
            tasks=[],
            verbose=2,
            process=Process.sequential
        )

# Добавляем showcase команды в фабрику
def create_showcase_dynamic_tasks(crew, topic, crew_type, language="ru", depth="standard"):
    """Создает динамические задачи для showcase команд"""
    
    agents = crew.agents
    tasks = []
    
    if crew_type == "swot_analysis":
        # Задачи для SWOT-анализа
        company_name = topic  # topic содержит название компании
        
        # Задача 1: Исследование рынка
        market_task = Task(
            description=f"""
            Проведите comprehensive исследование компании "{company_name}" и её рыночного окружения:
            
            🎯 ЦЕЛИ АНАЛИЗА:
            1. Изучить отрасль и рыночную позицию компании
            2. Проанализировать основных конкурентов  
            3. Выявить рыночные тренды и драйверы роста
            4. Оценить размер рынка и долю компании
            
            📊 ТРЕБУЕМЫЙ АНАЛИЗ:
            - История и бизнес-модель компании
            - Ключевые продукты/сервисы и их позиционирование
            - Анализ конкурентного ландшафта (топ-5 конкурентов)
            - Рыночные тренды и их влияние на компанию
            - Regulatory environment и compliance требования
            - Технологические изменения в отрасли
            
            Язык анализа: {language}
            Глубина: {depth} анализ с конкретными данными и примерами.
            """,
            agent=agents[0],
            expected_output="""
            Structured отчет с разделами:
            1. Executive Summary компании
            2. Market Analysis & Industry Overview  
            3. Competitive Landscape Analysis
            4. Market Trends & Opportunities
            5. Key Success Factors в отрасли
            """
        )
        
        # Задача 2: Финансовый анализ
        financial_task = Task(
            description=f"""
            Проведите детальный финансовый анализ компании "{company_name}":
            
            💰 ФИНАНСОВЫЕ МЕТРИКИ:
            1. Анализ финансовой отчетности (последние 3 года)
            2. Ключевые финансовые коэффициенты и их динамика
            3. Cash flow analysis и working capital management
            4. Debt analysis и capital structure
            5. Profitability analysis и efficiency ratios
            6. Сравнение с industry benchmarks
            
            📈 АНАЛИЗ ПЕРСПЕКТИВ:
            - Revenue growth trends и их sustainability  
            - Cost structure analysis и operational leverage
            - Investment в R&D, CapEx priorities
            - Dividend policy и shareholder returns
            - Financial risks и их mitigation
            
            Используйте доступные финансовые данные и отраслевые сравнения.
            Язык: {language}, глубина: {depth}
            """,
            agent=agents[1],
            expected_output="""
            Comprehensive финансовый отчет:
            1. Financial Performance Summary (3 года)
            2. Key Financial Ratios Analysis
            3. Cash Flow & Capital Analysis  
            4. Industry Benchmarking
            5. Financial Strengths & Weaknesses
            6. Financial Risk Assessment
            """
        )
        
        # Задача 3: SWOT-синтез
        swot_task = Task(
            description=f"""
            На основе проведенного исследования создайте comprehensive SWOT-анализ компании "{company_name}" и разработайте стратегические рекомендации:
            
            🎯 SWOT FRAMEWORK:
            
            💪 STRENGTHS (Сильные стороны):
            - Анализируйте внутренние преимущества компании
            - Core competencies и unique value propositions  
            - Strong assets, capabilities, resources
            - Brand strength, customer loyalty, market position
            
            ⚠️ WEAKNESSES (Слабые стороны):
            - Внутренние ограничения и области для улучшения
            - Resource constraints, skill gaps
            - Operational inefficiencies 
            - Product/service limitations
            
            🚀 OPPORTUNITIES (Возможности):
            - Внешние факторы для роста и развития
            - Market expansion possibilities
            - Technology trends, regulatory changes
            - Partnership и M&A opportunities
            
            ⚡ THREATS (Угрозы):
            - Внешние риски и challenges
            - Competitive threats, market disruption
            - Economic, regulatory, technological risks
            - Supply chain, operational risks
            
            🎯 СТРАТЕГИЧЕСКИЕ РЕКОМЕНДАЦИИ:
            1. SO Strategies (Strength-Opportunity)
            2. WO Strategies (Weakness-Opportunity)  
            3. ST Strategies (Strength-Threat)
            4. WT Strategies (Weakness-Threat)
            
            Приоритизируйте рекомендации по impact/feasibility matrix.
            Язык: {language}, формат: executive-ready презентация
            """,
            agent=agents[2],
            expected_output="""
            Executive SWOT Analysis Report:
            1. Executive Summary & Key Insights
            2. Detailed SWOT Matrix с examples
            3. Strategic Recommendations (приоритизированные)
            4. Implementation Roadmap  
            5. Success Metrics & KPIs
            6. Risk Mitigation Strategies
            
            Формат: Ready for C-level presentation
            """
        )
        
        tasks = [market_task, financial_task, swot_task]
    
    elif crew_type == "tech_review":
        # Задачи для технической рецензии
        repo_url = topic  # topic содержит ссылку на GitHub repo
        
        # Задача 1: Архитектурный анализ
        arch_task = Task(
            description=f"""
            Проведите comprehensive архитектурный анализ GitHub репозитория: {repo_url}
            
            🏗️ АРХИТЕКТУРНЫЙ АНАЛИЗ:
            1. Overall system architecture & design patterns
            2. Code organization & module structure
            3. Dependencies analysis & third-party libraries
            4. Scalability & maintainability assessment
            5. Performance implications анализ
            6. Database design & data flow (если применимо)
            
            📊 TECHNICAL DEBT ASSESSMENT:
            - Code complexity metrics
            - Architectural inconsistencies  
            - Legacy code patterns
            - Refactoring opportunities
            - Technical debt quantification
            
            🔍 DESIGN PATTERNS & BEST PRACTICES:
            - Используемые design patterns
            - SOLID principles compliance
            - Clean architecture adherence
            - Microservices/monolith trade-offs
            
            Анализируйте README, code structure, и documentation.
            Язык: {language}, глубина: {depth}
            """,
            agent=agents[0],
            expected_output="""
            Technical Architecture Report:
            1. System Architecture Overview
            2. Code Structure Analysis  
            3. Design Patterns Usage
            4. Technical Debt Assessment
            5. Scalability & Maintainability Score
            6. Architecture Recommendations
            """
        )
        
        # Задача 2: Security анализ
        security_task = Task(
            description=f"""
            Проведите security audit GitHub репозитория: {repo_url}
            
            🛡️ SECURITY ASSESSMENT:
            1. OWASP Top 10 vulnerabilities check
            2. Input validation & sanitization
            3. Authentication & authorization mechanisms
            4. Data encryption & secure storage
            5. API security (если REST/GraphQL APIs)
            6. Dependency vulnerabilities (security libraries)
            
            🔐 SECURE CODING PRACTICES:
            - Secure by design principles
            - Error handling & information disclosure
            - Logging security (no sensitive data exposure)  
            - Configuration security
            - Secrets management practices
            
            ⚠️ VULNERABILITY ASSESSMENT:
            - Potential security weaknesses
            - Attack vectors analysis
            - Risk severity classification (Critical/High/Medium/Low)
            - Remediation recommendations
            
            Фокусируйтесь на realistic security threats для данного типа приложения.
            Язык: {language}
            """,
            agent=agents[1],
            expected_output="""
            Security Assessment Report:
            1. Security Posture Overview
            2. Identified Vulnerabilities (с severity)
            3. OWASP Compliance Assessment
            4. Secure Coding Practices Review
            5. Risk Matrix & Prioritization
            6. Security Improvement Roadmap
            """
        )
        
        # Задача 3: Code Quality анализ
        quality_task = Task(
            description=f"""
            Проведите comprehensive code quality и DevOps practices анализ: {repo_url}
            
            📊 CODE QUALITY METRICS:
            1. Code readability & documentation coverage
            2. Test coverage & testing strategies
            3. Code complexity & maintainability index
            4. Coding standards compliance
            5. Performance optimization opportunities
            6. Error handling patterns
            
            🚀 DEVOPS & CI/CD ASSESSMENT:
            - CI/CD pipeline setup & best practices
            - Automated testing coverage (unit/integration/e2e)
            - Deployment strategies & automation
            - Monitoring & logging implementation
            - Documentation quality (README, API docs, comments)
            
            🎯 RECOMMENDATIONS SYNTHESIS:
            На основе архитектурного и security анализа:
            1. Priority improvements (High/Medium/Low impact)
            2. Quick wins vs long-term refactoring
            3. Team productivity improvements
            4. Maintainability enhancements
            5. Performance optimization suggestions
            
            Язык: {language}, формат: actionable recommendations
            """,
            agent=agents[2],
            expected_output="""
            Comprehensive Code Review Report:
            1. Code Quality Score & Metrics
            2. Testing & DevOps Assessment
            3. Prioritized Improvement Plan
            4. Best Practices Recommendations  
            5. Implementation Timeline & Effort Estimates
            6. Long-term Maintenance Strategy
            
            Format: Ready for development team action
            """
        )
        
        tasks = [arch_task, security_task, quality_task]
    
    elif crew_type == "investment_advisor":
        # Задачи для инвестиционного анализа
        ticker = topic.upper()  # topic содержит тикер акции
        
        # Задача 1: News & Sentiment анализ
        news_task = Task(
            description=f"""
            Проведите comprehensive анализ новостей и market sentiment для {ticker}:
            
            📰 NEWS ANALYSIS (последние 30 дней):
            1. Ключевые новости и события компании
            2. Industry news влияющие на сектор  
            3. Macroeconomic factors impact
            4. Management announcements & guidance
            5. Analyst upgrades/downgrades & price targets
            6. Earnings reports & financial updates
            
            📊 SENTIMENT ANALYSIS:
            - Social media sentiment (Twitter, Reddit финансовые сообщества)
            - News sentiment classification (positive/negative/neutral)
            - Institutional investor sentiment indicators
            - Analyst sentiment trends
            - Options flow & derivatives positioning
            
            🎯 MARKET IMPACT ASSESSMENT:
            - Stock price correlation с news events
            - Volume spikes и trading patterns
            - Sector comparison и relative performance
            - Beta analysis & market sensitivity
            
            Используйте актуальную информацию и финансовые данные.
            Язык: {language}, фокус на actionable insights
            """,
            agent=agents[0],
            expected_output="""
            Market Intelligence Report:
            1. News Summary & Key Events (30d)
            2. Sentiment Analysis Dashboard
            3. Market Impact Assessment
            4. Catalyst Events Calendar  
            5. Risk Events Monitoring
            6. Short-term Sentiment Forecast
            """
        )
        
        # Задача 2: Фундаментальный анализ
        fundamental_task = Task(
            description=f"""
            Проведите глубокий фундаментальный анализ компании с тикером {ticker}:
            
            💰 FINANCIAL PERFORMANCE ANALYSIS:
            1. Revenue growth trends (5+ лет истории)
            2. Profitability metrics & margins analysis
            3. Balance sheet strength & debt levels
            4. Cash flow analysis & capital allocation
            5. Return on equity/assets trends
            6. Working capital efficiency
            
            🎯 VALUATION ANALYSIS:
            - Multiple-based valuation (P/E, P/S, EV/EBITDA)
            - Discounted Cash Flow (DCF) estimation
            - Peer comparison & industry benchmarks
            - PEG ratio & growth-adjusted metrics
            - Asset-based valuation (если applicable)
            
            📈 BUSINESS MODEL ASSESSMENT:
            - Competitive advantages & moats
            - Market position & market share trends
            - Product/service differentiation  
            - Management quality & track record
            - ESG factors & sustainability metrics
            
            🔍 SECTOR & INDUSTRY ANALYSIS:
            - Industry growth prospects & headwinds
            - Regulatory environment changes
            - Technology disruption threats/opportunities
            
            Предоставьте fair value estimate с upside/downside scenarios.
            Язык: {language}
            """,
            agent=agents[1],
            expected_output="""
            Fundamental Analysis Report:
            1. Financial Performance Summary
            2. Valuation Analysis & Price Target
            3. Business Quality Assessment
            4. Competitive Position Analysis
            5. Industry Context & Outlook
            6. Risk Factors & Mitigation
            """
        )
        
        # Задача 3: Инвестиционные рекомендации
        investment_task = Task(
            description=f"""
            На основе проведенного анализа подготовьте comprehensive инвестиционную рекомендацию для {ticker}:
            
            📊 TECHNICAL ANALYSIS:
            1. Chart patterns & trend analysis
            2. Key support/resistance levels
            3. Moving averages & momentum indicators
            4. Volume analysis & money flow
            5. Relative strength vs market/sector
            6. Entry/exit timing considerations
            
            ⚖️ RISK-REWARD ASSESSMENT:
            - Upside/downside potential quantification
            - Risk factors prioritization (High/Medium/Low)
            - Correlation analysis с market factors
            - Volatility assessment & VaR estimates
            - Liquidity considerations
            - Portfolio fit analysis
            
            🎯 INVESTMENT RECOMMENDATION:
            - Buy/Hold/Sell recommendation с rationale
            - Price target с 12-month horizon
            - Position sizing recommendations
            - Time horizon considerations (short/medium/long-term)
            - Alternative investment scenarios
            
            💡 ACTIONABLE INSIGHTS:
            1. Key catalysts to watch (earnings, events, metrics)
            2. Stop-loss и profit-taking levels
            3. Monitoring plan для ongoing assessment
            4. Re-evaluation triggers
            
            Интегрируйте findings из news analysis и fundamental analysis.
            Формат: Investment committee-ready recommendation
            Язык: {language}
            """,
            agent=agents[2],
            expected_output="""
            Investment Recommendation Report:
            1. Executive Summary & Recommendation
            2. Technical Analysis & Entry Strategy
            3. Risk-Reward Assessment Matrix
            4. Price Target & Timeline  
            5. Monitoring Plan & Key Metrics
            6. Alternative Scenarios Analysis
            
            Format: Ready for portfolio implementation
            """
        )
        
        tasks = [news_task, fundamental_task, investment_task]
    
    # Назначаем задачи команде
    crew.tasks = tasks
    return tasks

# Расширяем фабрику команд
def get_showcase_crew_info():
    """Информация о showcase командах"""
    return {
        "swot_analysis": {
            "name": "SWOT-Аналитик", 
            "description": "Comprehensive SWOT-анализ компаний с стратегическими рекомендациями",
            "input": "Название компании (например: 'Apple', 'Tesla', 'Microsoft')",
            "output": "Детальный SWOT-анализ с матрицей и стратегическими рекомендациями",
            "estimated_time": "8-12 минут",
            "use_cases": ["Инвестиционный анализ", "Стратегическое планирование", "Due diligence"]
        },
        "tech_review": {
            "name": "Технический Рецензент",
            "description": "Comprehensive техническая рецензия GitHub репозиториев",
            "input": "GitHub URL (например: 'https://github.com/user/repo')",
            "output": "Техническая рецензия с анализом архитектуры, безопасности и качества",
            "estimated_time": "10-15 минут", 
            "use_cases": ["Code review", "Due diligence", "Техническая оценка", "Архитектурный аудит"]
        },
        "investment_advisor": {
            "name": "Инвестиционный Советник",
            "description": "Comprehensive инвестиционный анализ акций с рекомендациями",
            "input": "Тикер акции (например: 'AAPL', 'TSLA', 'MSFT')",
            "output": "Инвестиционная рекомендация с анализом рисков и price target",
            "estimated_time": "12-18 минут",
            "use_cases": ["Инвестиционные решения", "Portfolio анализ", "Stock screening"]
        }
    }

# Обновляем основную функцию run_research
original_run_research = run_research

def run_research_enhanced(topic: str, crew_type: str = "general", language: str = "ru", depth: str = "standard"):
    """Enhanced версия run_research с поддержкой showcase команд"""
    
    # Проверяем, является ли это showcase командой
    showcase_crews = get_showcase_crew_info()
    
    if crew_type in showcase_crews:
        # Создаем showcase команду
        showcase_factory = CrewShowcase(get_llm(), get_tools())
        
        if crew_type == "swot_analysis":
            crew = showcase_factory.create_swot_analyst_crew()
        elif crew_type == "tech_review": 
            crew = showcase_factory.create_tech_reviewer_crew()
        elif crew_type == "investment_advisor":
            crew = showcase_factory.create_investment_advisor_crew()
        else:
            # Fallback к стандартной команде
            return original_run_research(topic, crew_type, language, depth)
        
        # Создаем динамические задачи для showcase команды
        create_showcase_dynamic_tasks(crew, topic, crew_type, language, depth)
        
        # Запускаем исследование
        result = crew.kickoff()
        return result
    else:
        # Используем стандартную логику для существующих команд
        return original_run_research(topic, crew_type, language, depth)

# Заменяем функцию
run_research = run_research_enhanced

print("✅ Витрина решений добавлена в main_crew.py")
