#!/bin/bash
# AI Agent Farm - Start Full Monitoring Stack
# ===========================================

set -e

echo "🚀 Starting AI Agent Farm with full monitoring stack..."

# Создаем сеть для мониторинга
docker network create monitoring 2>/dev/null || echo "Network monitoring already exists"

echo "📊 Starting logging stack..."
docker compose -f docker-compose.logging.yml up -d

echo "🤖 Starting AI Agent Farm..."
docker compose -f docker-compose.prod.yml up -d

echo "⏳ Waiting for services to start..."
sleep 30

echo "🏥 Health checking services..."

# Проверяем AI Agent Farm API
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ AI Agent Farm API is healthy"
else
    echo "❌ AI Agent Farm API is not responding"
fi

# Проверяем Grafana
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Grafana is healthy"
else
    echo "❌ Grafana is not responding"  
fi

# Проверяем Loki
if curl -f http://localhost:3100/ready > /dev/null 2>&1; then
    echo "✅ Loki is healthy"
else
    echo "❌ Loki is not responding"
fi

echo ""
echo "🎉 Full monitoring stack started successfully!"
echo ""
echo "📊 Access points:"
echo "• AI Agent Farm API: http://localhost:8000"
echo "• AI Agent Farm Docs: http://localhost:8000/docs"
echo "• Grafana Dashboard: http://localhost:3000 (admin/admin123)"
echo "• Loki Logs: http://localhost:3100"
echo "• Prometheus: http://localhost:9090"
echo ""
echo "📈 Grafana Dashboard: Import the AI Agent Farm dashboard from logging/dashboards/"
