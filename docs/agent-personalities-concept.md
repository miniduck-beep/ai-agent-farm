# 🎭 AI Agent Farm - Система "Персоналий Агентов"

## 📖 Концепция

Система "Персоналий Агентов" позволяет пользователям выбирать специализированные команды агентов для решения различных типов задач. Каждая команда состоит из экспертов в своей области с уникальными ролями и специализациями.

## 🏗️ Техническая архитектура

### API Расширение

```python
class ResearchRequest(BaseModel):
    topic: str = Field(..., description="Тема для исследования")
    crew_type: str = Field(
        default="general", 
        description="Тип команды агентов",
        enum=["general", "business_analyst", "content_marketing", "tech_research", "financial_analysis"]
    )
    language: str = Field(default="ru", description="Язык отчета")
    depth: str = Field(default="standard", enum=["basic", "standard", "deep"])
```

### Фабрика Команд Агентов

```python
# app/crew_factory.py
from enum import Enum
from typing import List, Dict, Any
from crewai import Agent, Task, Crew

class CrewType(str, Enum):
    GENERAL = "general"
    BUSINESS_ANALYST = "business_analyst" 
    CONTENT_MARKETING = "content_marketing"
    TECH_RESEARCH = "tech_research"
    FINANCIAL_ANALYSIS = "financial_analysis"
    STARTUP_CONSULTANT = "startup_consultant"

class AgentPersonality:
    def __init__(self, role: str, goal: str, backstory: str, tools: List):
        self.role = role
        self.goal = goal 
        self.backstory = backstory
        self.tools = tools

class CrewFactory:
    """Фабрика для создания специализированных команд агентов"""
    
    @staticmethod
    def create_crew(crew_type: CrewType, topic: str, llm, tools: Dict) -> Crew:
        if crew_type == CrewType.BUSINESS_ANALYST:
            return CrewFactory._create_business_analyst_crew(topic, llm, tools)
        elif crew_type == CrewType.CONTENT_MARKETING:
            return CrewFactory._create_content_marketing_crew(topic, llm, tools)
        elif crew_type == CrewType.TECH_RESEARCH:
            return CrewFactory._create_tech_research_crew(topic, llm, tools)
        elif crew_type == CrewType.FINANCIAL_ANALYSIS:
            return CrewFactory._create_financial_analysis_crew(topic, llm, tools)
        elif crew_type == CrewType.STARTUP_CONSULTANT:
            return CrewFactory._create_startup_consultant_crew(topic, llm, tools)
        else:
            return CrewFactory._create_general_crew(topic, llm, tools)
```

## 🎯 Предопределенные Команды Агентов

### 1. 💼 Business Analyst Team

**Состав команды:**
- **Market Researcher** - Исследователь рынка
- **Financial Analyst** - Финансовый аналитик  
- **Strategy Consultant** - Стратегический консультант

```python
def _create_business_analyst_crew(topic: str, llm, tools: Dict) -> Crew:
    market_researcher = Agent(
        role='Senior Market Research Analyst',
        goal=f'Провести глубокое исследование рынка по теме "{topic}"',
        backstory="""Вы - ведущий аналитик рынка с 15-летним опытом в McKinsey & Company. 
                    Специализируетесь на анализе трендов, конкурентной среды и потребительского поведения.
                    Ваши отчеты используются Fortune 500 компаниями для принятия стратегических решений.""",
        tools=[tools['search_tool'], tools['market_data_tool']],
        llm=llm
    )
    
    financial_analyst = Agent(
        role='Investment Banking Analyst', 
        goal=f'Провести финансовый анализ и оценку возможностей в области "{topic}"',
        backstory="""Вы - старший аналитик Goldman Sachs с экспертизой в валуации компаний,
                    анализе финансовых показателей и инвестиционных возможностей.
                    Специализируетесь на технологических и инновационных секторах.""",
        tools=[tools['financial_data_tool'], tools['calculator_tool']],
        llm=llm
    )
    
    strategy_consultant = Agent(
        role='Strategic Business Consultant',
        goal=f'Разработать стратегические рекомендации и план действий по теме "{topic}"', 
        backstory="""Вы - партнер в Bain & Company с опытом консалтинга для крупнейших корпораций.
                    Экспертиза в разработке бизнес-стратегий, операционной оптимизации 
                    и трансформации бизнес-моделей.""",
        tools=[tools['strategy_framework_tool']],
        llm=llm
    )
    
    # Задачи для каждого агента
    tasks = [
        Task(
            description=f"""Проанализируйте рынок по теме "{topic}":
                          - Размер и динамика рынка
                          - Ключевые игроки и их доли
                          - Потребительские тренды
                          - Барьеры входа и возможности""",
            agent=market_researcher
        ),
        Task(
            description=f"""Проведите финансовый анализ по теме "{topic}":
                          - Инвестиционная привлекательность  
                          - ROI потенциал
                          - Финансовые риски
                          - Модели монетизации""",
            agent=financial_analyst  
        ),
        Task(
            description=f"""Создайте стратегический план по теме "{topic}":
                          - SWOT анализ
                          - Конкурентные преимущества
                          - План выхода на рынок
                          - KPI и метрики успеха""",
            agent=strategy_consultant
        )
    ]
    
    return Crew(agents=[market_researcher, financial_analyst, strategy_consultant], 
                tasks=tasks, verbose=True)
```

### 2. 📝 Content Marketing Team  

**Состав команды:**
- **SEO Specialist** - SEO-аналитик
- **Content Writer** - Контент-райтер
- **Social Media Manager** - SMM-менеджер

```python
def _create_content_marketing_crew(topic: str, llm, tools: Dict) -> Crew:
    seo_specialist = Agent(
        role='Senior SEO Content Strategist',
        goal=f'Провести SEO-анализ и найти ключевые слова для контента по теме "{topic}"',
        backstory="""Вы - ведущий SEO-эксперт с опытом работы в Moz и SEMrush. 
                    Помогли более 200 компаниям увеличить органический трафик на 300%+.
                    Эксперт в техническом SEO, контентной оптимизации и анализе конкурентов.""",
        tools=[tools['seo_tool'], tools['keyword_research_tool']],
        llm=llm
    )
    
    content_writer = Agent(
        role='Creative Content Writer',
        goal=f'Создать вовлекающий и SEO-оптимизированный контент по теме "{topic}"',
        backstory="""Вы - творческий копирайтер с опытом работы в ведущих digital-агентствах.
                    Создали контент для брендов уровня Nike, Apple, Google.
                    Специализируетесь на storytelling и конверсионном копирайтинге.""",
        tools=[tools['content_generator_tool']],
        llm=llm
    )
    
    smm_manager = Agent(
        role='Social Media Marketing Manager',
        goal=f'Разработать стратегию продвижения контента по теме "{topic}" в социальных сетях',
        backstory="""Вы - SMM-эксперт с опытом запуска вирусных кампаний для топовых брендов.
                    Управляли бюджетами $1M+ в Facebook, Instagram, TikTok, LinkedIn.
                    Специализируетесь на community building и влияние-маркетинге.""",
        tools=[tools['social_media_tool'], tools['trend_analysis_tool']],  
        llm=llm
    )
```

### 3. 🔬 Tech Research Team

**Состав команды:**
- **Technical Architect** - Технический архитектор
- **Innovation Researcher** - Исследователь инноваций  
- **Implementation Specialist** - Специалист по внедрению

### 4. 💰 Financial Analysis Team

**Состав команды:**
- **Quantitative Analyst** - Квант-аналитик
- **Risk Assessment Specialist** - Специалист по рискам
- **Investment Advisor** - Инвестиционный консультант

### 5. 🚀 Startup Consultant Team

**Состав команды:**
- **Business Model Designer** - Дизайнер бизнес-модели
- **Go-to-Market Strategist** - Стратег выхода на рынок
- **Fundraising Expert** - Эксперт по привлечению инвестиций

## 🛠️ Техническая реализация

### Обновленный API Endpoint

```python
@app.post("/research", response_model=TaskResponse, tags=["Research"])
async def start_research(request: ResearchRequest):
    """🚀 Запуск исследования с выбором команды агентов"""
    try:
        from app.tasks import run_research_crew
        
        # Запускаем задачу с указанием типа команды
        task = run_research_crew.delay(
            topic=request.topic,
            crew_type=request.crew_type,
            language=request.language,
            depth=request.depth
        )
        
        return TaskResponse(
            task_id=task.id,
            status="PENDING",
            message=f"Исследование '{request.topic}' запущено с командой '{request.crew_type}'"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Модифицированная Celery Task

```python
@celery_app.task(bind=True, name="run_research_crew")
def run_research_crew(self, topic: str, crew_type: str = "general", language: str = "ru", depth: str = "standard"):
    """Запуск исследования с выбранной командой агентов"""
    
    task_id = self.request.id
    
    try:
        print(f"🎭 Создание команды типа '{crew_type}' для темы '{topic}'")
        
        # Создание команды через фабрику
        crew = CrewFactory.create_crew(
            crew_type=CrewType(crew_type),
            topic=topic, 
            llm=llm,
            tools=available_tools
        )
        
        # Запуск команды
        result = crew.kickoff()
        
        return result
        
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise e
```

## 📊 Примеры использования

### Бизнес-анализ

```bash
curl -X POST "http://100.110.253.23:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Рынок электромобилей в России", 
    "crew_type": "business_analyst",
    "depth": "deep"
  }'
```

**Ожидаемый результат:**
- Детальный анализ рынка электромобилей
- Финансовые прогнозы и ROI
- SWOT-анализ основных игроков
- Стратегические рекомендации для входа

### Контент-маркетинг

```bash
curl -X POST "http://100.110.253.23:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Продвижение SaaS продукта для малого бизнеса",
    "crew_type": "content_marketing", 
    "language": "ru"
  }'
```

**Ожидаемый результат:**
- SEO-стратегия и ключевые слова
- Контент-план на 3 месяца
- Стратегия продвижения в соцсетях
- Метрики и KPI для отслеживания

## 🔄 Расширение системы

### Добавление новых команд

```python
# Новая команда "Legal Advisors"
class LegalAdvisorsTeam:
    def create_agents():
        return [
            Agent(role="Corporate Lawyer", ...),
            Agent(role="IP Specialist", ...),
            Agent(role="Compliance Expert", ...)
        ]
```

### Кастомизация агентов

```python
# Настройка через конфигурационные файлы
# config/crews/business_analyst.yaml
market_researcher:
  role: "Senior Market Research Analyst"
  experience_years: 15
  previous_companies: ["McKinsey", "BCG", "Bain"]
  specializations: ["B2B markets", "Tech sector", "Emerging markets"]
```

### Интеграция с внешними инструментами

```python
# Специализированные инструменты для каждого типа команды
CREW_TOOLS_MAPPING = {
    "business_analyst": [
        MarketDataTool(),
        CompetitorAnalysisTool(), 
        FinancialModelingTool()
    ],
    "content_marketing": [
        SEOTool(),
        SocialMediaTool(),
        ContentOptimizationTool()
    ]
}
```

## 🎯 Преимущества системы

### Для пользователей
- ✅ **Специализация**: Каждая команда - эксперты в своей области
- ✅ **Качество**: Более точные и релевантные результаты
- ✅ **Эффективность**: Быстрое получение профессиональных инсайтов
- ✅ **Гибкость**: Выбор команды под конкретную задачу

### Для разработчиков  
- ✅ **Модульность**: Легко добавлять новые команды
- ✅ **Масштабируемость**: Простое расширение функциональности
- ✅ **Поддерживаемость**: Четкое разделение ответственности
- ✅ **Тестируемость**: Возможность тестировать каждую команду отдельно

## 🚀 План развития

### Фаза 1 (MVP)
- [x] Базовая архитектура с 3 командами
- [x] API для выбора команды
- [x] Фабрика агентов

### Фаза 2 (Расширение)
- [ ] 5+ специализированных команд
- [ ] Конфигурация через YAML файлы
- [ ] Метрики качества для каждой команды

### Фаза 3 (Персонализация)
- [ ] Кастомные команды пользователей
- [ ] ML-оптимизация состава команд
- [ ] A/B тестирование эффективности

---

**🎭 Результат**: Гибкая и масштабируемая система специализированных команд ИИ-агентов для решения разнообразных бизнес-задач!
