# 🤖 AI Agent Farm

> **Production-Ready Multi-Agent Research & Content Generation Platform**

[![Version](https://img.shields.io/badge/version-v1.0.0--beta-blue)](https://github.com/miniduck-beep/ai-agent-farm/releases)
[![Python](https://img.shields.io/badge/python-3.11+-brightgreen)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://docker.com)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

AI Agent Farm transforms complex research tasks into structured insights through intelligent multi-agent collaboration. Built for production environments with enterprise-grade security and scalability.

---

## 🎯 **What Problems Does It Solve?**

- **Manual Research Overload**: Eliminates hours of manual information gathering
- **Inconsistent Analysis**: Ensures structured, repeatable research methodology  
- **Scale Limitations**: Handles multiple research projects simultaneously
- **Integration Challenges**: Provides API-first architecture for easy integration
- **Quality Control**: Built-in validation and review through multi-agent oversight

---

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🌐 Client     │    │   🚀 FastAPI    │    │  🤖 AI Agents  │
│                 │───▶│     Server      │───▶│   (CrewAI)     │
│ • REST API      │    │                 │    │                │
│ • n8n Workflows│    │ • Authentication│    │ • Researcher   │
│ • Web Interface │    │ • Rate Limiting │    │ • Writer       │
└─────────────────┘    │ • Input Valid.  │    │ • Supervisor   │
                       └─────────────────┘    └─────────────────┘
                                 │                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │  ⚙️ Task Queue  │    │  🧠 LLM APIs   │
                       │                 │    │                │
                       │ • Celery Worker │    │ • Gemini Pro   │
                       │ • Redis Backend │    │ • OpenAI (opt) │
                       │ • Progress Track│    │ • Serper Search│
                       └─────────────────┘    └─────────────────┘
```

### **Component Overview**
- **FastAPI Server**: High-performance async API with automatic documentation
- **Celery Workers**: Distributed task processing for heavy research workloads
- **Redis**: Message broker and results storage with persistence
- **CrewAI Agents**: Specialized AI agents with defined roles and responsibilities
- **LLM Integration**: Multiple AI model support with fallback strategies

---

## 🛠️ **Technology Stack**

### **Core Framework**
- **Python 3.11+**: Latest features and performance improvements
- **FastAPI 0.111.0**: Modern async web framework with automatic OpenAPI
- **CrewAI 0.28.0**: Multi-agent orchestration framework
- **Celery 5.3.0**: Distributed task queue for scalable processing

### **Data & Storage**
- **Redis 7+**: In-memory data structure store for caching and queues
- **Pydantic 2.5+**: Data validation and serialization
- **JSON**: Structured data exchange format

### **AI & ML**
- **Google Gemini Pro**: Primary language model for reasoning
- **LangChain**: LLM integration and chaining framework
- **Serper API**: Real-time search and information retrieval

### **Infrastructure**
- **Docker & Docker Compose**: Containerization and orchestration
- **Gunicorn**: Production WSGI server
- **GitHub Actions**: CI/CD pipeline automation

---

## 🚀 **Quick Start**

### **Prerequisites**
- Docker 20.10+ and Docker Compose
- API Keys: [Gemini API](https://makersuite.google.com/app/apikey), [Serper API](https://serper.dev)

### **1. Clone & Setup**
```bash
git clone https://github.com/miniduck-beep/ai-agent-farm.git
cd ai-agent-farm

# Create environment file from template
cp .env.example .env
```

### **2. Configure Environment**
Edit `.env` file with your API keys:
```env
# AI API Keys (REQUIRED)
GOOGLE_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_search_key_here

# System Configuration
DEBUG=false
LOG_LEVEL=INFO
REDIS_URL=redis://redis:6379/0

# Optional: OpenAI as backup
OPENAI_API_KEY=your_openai_key_here
```

### **3. Launch Platform**
```bash
# Build and start all services
docker compose up --build -d

# Verify system health
curl http://localhost:8000/health
```

### **4. First Research Request**
```bash
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Future of AI in Healthcare",
    "research_depth": "comprehensive",
    "language": "en"
  }'
```

**Response:**
```json
{
  "task_id": "research_abc123def456",
  "status": "PENDING",
  "estimated_time": "5-10 minutes",
  "message": "Research task initiated successfully"
}
```

### **5. Retrieve Results**
```bash
curl "http://localhost:8000/result/research_abc123def456"
```

---

## 📚 **API Reference**

### **Core Endpoints**

#### `POST /research` - Initiate Research
Creates a new research task with specified parameters.

**Request Body:**
```json
{
  "topic": "string (required)",
  "research_depth": "basic|standard|comprehensive",
  "language": "en|ru",
  "agent_team": "general|business|tech|marketing",
  "deadline": "2024-01-01T12:00:00Z (optional)"
}
```

**Response:**
```json
{
  "task_id": "string",
  "status": "PENDING|PROCESSING|COMPLETED|FAILED",
  "estimated_time": "string",
  "created_at": "timestamp"
}
```

#### `GET /result/{task_id}` - Get Research Results
Retrieves the results of a completed research task.

**Response:**
```json
{
  "task_id": "string",
  "status": "COMPLETED",
  "progress": 100,
  "result": {
    "title": "Research Title",
    "executive_summary": "Brief overview...",
    "key_findings": ["Finding 1", "Finding 2"],
    "detailed_analysis": "Full analysis...",
    "sources": ["Source 1", "Source 2"],
    "generated_at": "timestamp"
  },
  "processing_time": 456.78
}
```

#### `GET /health` - System Health Check
Returns the current system status and component health.

#### `GET /tasks/{task_id}/progress` - Real-time Progress
WebSocket endpoint for live progress updates.

### **Interactive API Documentation**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔧 **Configuration Options**

### **Environment Variables**
```env
# Core API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Redis Configuration
REDIS_URL=redis://redis:6379/0
REDIS_MAX_CONNECTIONS=50

# Celery Settings
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_TASK_TIMEOUT=3600

# AI Model Configuration
GEMINI_MODEL=gemini-pro
GEMINI_TEMPERATURE=0.1
GEMINI_MAX_TOKENS=8192

# Security Settings
API_KEY_REQUIRED=false
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Monitoring & Logging
LOG_LEVEL=INFO
ENABLE_METRICS=true
SENTRY_DSN=your_sentry_dsn_here
```

### **Production Deployment**
```bash
# Production with Gunicorn
docker compose -f docker-compose.prod.yml up -d

# Scale workers
docker compose up --scale worker=4 -d

# Health monitoring
docker compose logs -f api worker
```

---

## 🔒 **Security Features**

### **Built-in Security**
- ✅ **Non-root Container Execution**: All services run with minimal privileges
- ✅ **Environment Variable Protection**: API keys never exposed in code
- ✅ **Input Validation**: Comprehensive Pydantic schemas
- ✅ **Rate Limiting**: Configurable request throttling
- ✅ **CORS Protection**: Controlled cross-origin access

### **Production Hardening**
```bash
# Enable additional security layers
export API_KEY_REQUIRED=true
export ENABLE_HTTPS=true
export CORS_ORIGINS="https://yourdomain.com"

# Deploy with secrets management
docker compose --env-file .env.production up -d
```

---

## 🧪 **Development & Testing**

### **Local Development**
```bash
# Create development environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=app

# Start development server
uvicorn app.api:app --reload --port 8000
```

### **Code Quality**
```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

---

## 🐳 **Docker Commands**

### **Basic Operations**
```bash
# Build and start
docker compose up --build

# Background mode
docker compose up -d

# View logs
docker compose logs -f

# Scale services
docker compose up --scale worker=3 -d

# Stop all services
docker compose down

# Clean restart
docker compose down -v && docker compose up --build
```

### **Production Commands**
```bash
# Production deployment
docker compose -f docker-compose.prod.yml up -d

# Update running containers
docker compose pull && docker compose up -d

# Backup Redis data
docker exec ai-farm-redis redis-cli SAVE
```

---

## 📊 **Monitoring & Observability**

### **Health Endpoints**
- `GET /health` - Overall system health
- `GET /health/redis` - Redis connectivity
- `GET /health/celery` - Worker status
- `GET /metrics` - Prometheus metrics

### **Logging**
```bash
# View application logs
docker compose logs -f api

# View worker logs  
docker compose logs -f worker

# View Redis logs
docker compose logs -f redis
```

---

## 🚀 **Roadmap**

### **v1.0.0 (Current Beta)**
- ✅ Core multi-agent research functionality
- ✅ REST API with async processing
- ✅ Docker containerization
- ✅ Production security hardening

### **v1.1.0 (Planned)**
- 🔄 Advanced agent specializations
- 🔄 WebSocket real-time updates
- 🔄 Result caching and optimization
- 🔄 Enhanced error handling

### **v1.2.0 (Future)**
- 🔄 Web dashboard interface
- 🔄 Multiple LLM provider support
- 🔄 Advanced analytics and reporting
- 🔄 Enterprise SSO integration

---

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Quick Contribution Setup**
```bash
# Fork and clone your fork
git clone https://github.com/yourusername/ai-agent-farm.git

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes, test, and commit
pytest && git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/amazing-feature
```

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 **Support & Community**

- 📖 **Documentation**: [GitHub Wiki](https://github.com/miniduck-beep/ai-agent-farm/wiki)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/miniduck-beep/ai-agent-farm/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/miniduck-beep/ai-agent-farm/discussions)
- 📧 **Email Support**: support@ai-agent-farm.dev

---

**Built with ❤️ for the AI research community**

*Transform your research workflows with intelligent automation.*
