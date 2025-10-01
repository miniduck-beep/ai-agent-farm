# 📊 AI Agent Farm - Monitoring & Logging

Comprehensive мониторинг и логирование для AI Agent Farm с использованием современного стека технологий.

## 🏗️ Архитектура мониторинга

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   AI Agent      │───▶│   Promtail   │───▶│      Loki       │
│   Farm Apps     │    │ (Log Shipper)│    │ (Log Storage)   │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                    │
┌─────────────────┐    ┌──────────────┐            │
│    Grafana      │◀───│      n8n     │◀───────────┘
│  (Dashboard)    │    │ (Alerting)   │
└─────────────────┘    └──────────────┘
                              │
                       ┌──────────────┐
                       │   Telegram   │
                       │   Alerts     │
                       └──────────────┘
```

## 🚀 Быстрый старт

### 1. Запуск monitoring stack
```bash
# Создание сети мониторинга
docker network create monitoring

# Запуск всего стека мониторинга
./scripts/start-monitoring.sh
```

### 2. Доступ к сервисам
- **Grafana:** http://localhost:3000 (admin/admin123)
- **Loki API:** http://localhost:3100
- **Prometheus:** http://localhost:9090
- **AI Agent Farm:** http://localhost:8000

## 📊 Компоненты

### Grafana Loki - Централизованное логирование
- **Назначение:** Агрегация и хранение логов
- **Конфигурация:** `logging/loki-config.yaml`
- **Объем:** Unlimited (filesystem storage)

### Promtail - Log Shipper
- **Назначение:** Сбор логов из Docker контейнеров
- **Конфигурация:** `logging/promtail-config.yaml`
- **Источники:** Docker containers, system logs

### Grafana - Visualization
- **Назначение:** Дашборды и визуализация
- **Dashboard:** `logging/dashboards/ai-agent-farm-dashboard.json`
- **Features:** Real-time logs, metrics, alerts

### n8n - Alerting & Automation
- **Назначение:** Мониторинг health endpoints и отправка алертов
- **Workflow:** `integrations/n8n/monitoring-alerts-workflow.json`
- **Интеграции:** Telegram, email, Slack

## 🔧 Конфигурация

### Environment Variables
```bash
# .env файл
GRAFANA_PASSWORD=secure_password_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### Telegram Bot Setup
1. Создайте бота через @BotFather
2. Получите токен бота
3. Получите chat_id через @userinfobot
4. Обновите n8n workflow с вашими данными

### Настройка алертов
1. Импортируйте workflow в n8n
2. Настройте Telegram credentials
3. Активируйте workflow
4. Тестируйте уведомления

## 📈 Мониторируемые метрики

### System Health
- ✅ API availability (health endpoint)
- 📊 Active tasks count
- 🔄 Worker status
- 💾 Redis connectivity
- 📋 Component status

### Performance Metrics
- 🕐 Response times
- 📈 Request rates
- ❌ Error rates
- 💻 Resource usage

### Business Metrics
- 🧠 Research completions
- 👥 Active users
- 📊 Crew type usage
- ⏱️ Task processing times

## 🚨 Alerting Rules

### Critical Alerts (немедленно)
- ❌ API down (health check fails)
- 🚨 Loki logging service down
- 💥 Worker crashes
- 🔴 Error rate > 10%

### Warning Alerts (в течение 5 мин)
- ⚠️ High task load (>10 active tasks)
- 📈 Response time > 5s
- 💾 Disk space < 20%
- 🔄 Worker queue backlog

### Info Notifications (1 раз в час)
- ✅ System health summary
- 📊 Usage statistics
- 🎯 Performance summary

## 🔍 Log Analysis

### Полезные Loki queries
```logql
# Все логи AI Agent Farm
{container=~".*ai-farm.*"}

# Только ошибки
{container=~".*ai-farm.*"} |~ "ERROR"

# Логи конкретной задачи
{container=~".*ai-farm.*"} | json | task_id="your-task-id"

# Rate of errors за последние 5 минут
sum(rate({container=~".*ai-farm.*"} |~ "ERROR" [5m]))

# Логи по уровню (level)
{container=~".*ai-farm.*"} | json | level="INFO"
```

### Grafana Dashboard Features
- 📊 Real-time log streaming
- 📈 Error rate graphs
- 🥧 Log level distribution
- 🔍 Searchable log history
- ⚡ Auto-refresh (30s)

## 🧰 Troubleshooting

### Общие проблемы

**🔴 Loki не запускается**
```bash
# Проверить права на папку
sudo chown -R 10001:10001 logging/loki-data/
docker compose -f docker-compose.logging.yml restart loki
```

**🔴 Promtail не собирает логи**
```bash
# Проверить доступ к Docker socket
ls -la /var/run/docker.sock
# Должно быть: srw-rw---- 1 root docker
```

**🔴 Grafana не показывает дашборд**
```bash
# Проверить datasource connection
curl http://localhost:3100/ready
# Перезагрузить дашборд в Grafana
```

### Performance Tuning

**Для high-load окружений:**
```yaml
# loki-config.yaml
ingestion_rate_mb: 64
ingestion_burst_size_mb: 128
max_query_length: 12000h
```

**Retention политики:**
```yaml
# Хранить логи 30 дней
table_manager:
  retention_deletes_enabled: true
  retention_period: 720h
```

## 📚 Полезные ресурсы

- [Loki Documentation](https://grafana.com/docs/loki/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [n8n Workflows](https://n8n.io/workflows/)
- [Promtail Configuration](https://grafana.com/docs/loki/latest/clients/promtail/)

---

**🎯 Professional-grade мониторинг для AI Agent Farm!**
