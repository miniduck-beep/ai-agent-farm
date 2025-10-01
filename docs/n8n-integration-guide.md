# 🤖 AI Agent Farm + n8n Integration Guide

Полное руководство по интеграции AI Agent Farm с n8n для автоматизации исследований

## 📖 Обзор

Этот гайд покажет, как создать полностью автоматизированный workflow в n8n, который:
1. Запускает исследование на AI Agent Farm
2. Отслеживает статус выполнения  
3. Получает готовый отчет
4. Отправляет результат в Telegram

## 🔧 Предварительные требования

- ✅ AI Agent Farm развернута и доступна по адресу `http://100.110.253.23:8000`
- ✅ n8n установлен и настроен
- ✅ Telegram бот создан (опционально для финального действия)

## 🏗️ Архитектура Workflow

```
[Trigger] → [POST Request] → [Wait] → [GET Request] → [IF Check] → [Final Action]
    ↓             ↓            ↓           ↓            ↓            ↓
  Webhook      Запуск     Пауза 15с   Проверка    Если готов   Telegram
   /Cron    исследования              статуса      → выход      или Email
                                                 Если нет →  
                                                     ↑ Цикл
```

## 📝 Пошаговая инструкция

### Шаг 1: Создание нового Workflow

1. Откройте n8n интерфейс
2. Нажмите **"New Workflow"**  
3. Назовите workflow: `"AI Farm Research Pipeline"`

### Шаг 2: Настройка Триггера

**Опция A: Manual Trigger (для тестирования)**
```json
{
  "node": "Manual Trigger",
  "settings": {
    "description": "Запуск исследования вручную"
  }
}
```

**Опция B: Webhook Trigger (для автоматизации)**  
```json
{
  "node": "Webhook",
  "settings": {
    "httpMethod": "POST",
    "path": "start-research",
    "responseMode": "responseNode"
  }
}
```

**Опция C: Cron Trigger (по расписанию)**
```json  
{
  "node": "Cron",
  "settings": {
    "rule": "0 9 * * *",
    "description": "Ежедневно в 9:00"
  }
}
```

### Шаг 3: Настройка HTTP Request (POST) - Запуск исследования

```yaml
Node Name: "Start Research"
Method: POST
URL: http://100.110.253.23:8000/research
Headers:
  Content-Type: application/json
Body (JSON):
  {
    "topic": "{{ $node['Manual Trigger'].json.topic || 'Искусственный интеллект в медицине' }}"
  }
```

**Детальные настройки POST ноды:**
- **HTTP Request Method**: `POST`
- **URL**: `http://100.110.253.23:8000/research`  
- **Send Body**: `Yes`
- **Body Content Type**: `JSON`
- **Specify Body**: `Using Fields Below`
- **Body Parameters**:
  - **Name**: `topic`
  - **Value**: `{{ $node['Manual Trigger'].json.topic || "Блокчейн в образовании" }}`

**Ожидаемый ответ:**
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "PENDING",
  "message": "Исследование темы 'Блокчейн в образовании' принято в работу..."
}
```

### Шаг 4: Настройка Wait Node - Пауза

```yaml
Node Name: "Wait for Processing"
Wait Time: 15 seconds
Description: "Даем время на обработку задачи агентами"
```

**Настройки Wait ноды:**
- **Resume**: `After Time Interval`
- **Wait Time**: `15` 
- **Time Unit**: `seconds`

### Шаг 5: Настройка HTTP Request (GET) - Проверка статуса

```yaml
Node Name: "Check Status"  
Method: GET
URL: http://100.110.253.23:8000/result/{{ $node['Start Research'].json.task_id }}
```

**Детальные настройки GET ноды:**
- **HTTP Request Method**: `GET`
- **URL**: `http://100.110.253.23:8000/result/{{ $node['Start Research'].json.task_id }}`
- **Headers**: (не требуются)

**Возможные ответы:**

*Задача еще выполняется:*
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "PROGRESS", 
  "progress": 45,
  "message": "Агент-писатель создает отчет..."
}
```

*Задача завершена:*
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "SUCCESS",
  "progress": 100,
  "message": "Исследование завершено успешно!",
  "result": "# Исследование: Блокчейн в образовании\n\n## Краткое резюме..."
}
```

### Шаг 6: Настройка IF Node - Проверка готовности

```yaml
Node Name: "Is Research Complete?"
Condition: "{{ $node['Check Status'].json.status === 'SUCCESS' }}"
```

**Детальные настройки IF ноды:**
- **Conditions**: `Boolean`  
- **Value 1**: `{{ $node['Check Status'].json.status }}`
- **Operation**: `Equal`
- **Value 2**: `SUCCESS`

**Логика ветвления:**
- **TRUE** → Исследование готово, переходим к финальному действию
- **FALSE** → Возвращаемся к ожиданию (создать цикл)

### Шаг 7: Настройка цикла для ожидания

**Для FALSE ветви IF ноды:**
1. Добавьте еще одну **Wait** ноду (30 секунд)
2. Подключите ее обратно к **"Check Status"** ноде
3. Это создаст цикл проверки каждые 30 секунд

### Шаг 8: Финальное действие - Отправка в Telegram

```yaml
Node Name: "Send to Telegram"
API Token: YOUR_BOT_TOKEN
Chat ID: YOUR_CHAT_ID
Message: "🎉 Исследование готово!\n\nТема: {{ $node['Start Research'].json.topic }}\n\nРезультат:\n{{ $node['Check Status'].json.result }}"
```

**Детальные настройки Telegram ноды:**
- **Chat ID**: `YOUR_CHAT_ID` (например: `123456789`)
- **Text**: 
```
🎉 Новое исследование готово!

📋 Тема: {{ $json.topic }}
⏱️ Task ID: {{ $node['Start Research'].json.task_id }}
📊 Статус: {{ $node['Check Status'].json.status }}

📑 Результат:
{{ $node['Check Status'].json.result }}
```

## 🔄 Полный JSON Workflow для импорта

<details>
<summary>Нажмите для просмотра готового workflow JSON</summary>

```json
{
  "name": "AI Farm Research Pipeline",
  "nodes": [
    {
      "parameters": {},
      "id": "manual-trigger",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [240, 300]
    },
    {
      "parameters": {
        "url": "http://100.110.253.23:8000/research",
        "options": {
          "bodyContentType": "json",
          "jsonBody": {
            "topic": "={{ $node['Manual Trigger'].json.topic || 'Искусственный интеллект в финансах' }}"
          }
        }
      },
      "id": "start-research",
      "name": "Start Research",
      "type": "n8n-nodes-base.httpRequest",
      "position": [460, 300]
    },
    {
      "parameters": {
        "amount": 15,
        "unit": "seconds"
      },
      "id": "wait-processing",
      "name": "Wait for Processing", 
      "type": "n8n-nodes-base.wait",
      "position": [680, 300]
    },
    {
      "parameters": {
        "url": "=http://100.110.253.23:8000/result/{{ $node['Start Research'].json.task_id }}",
        "options": {}
      },
      "id": "check-status",
      "name": "Check Status",
      "type": "n8n-nodes-base.httpRequest", 
      "position": [900, 300]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $node['Check Status'].json.status }}",
              "value2": "SUCCESS"
            }
          ]
        }
      },
      "id": "is-complete",
      "name": "Is Research Complete?",
      "type": "n8n-nodes-base.if",
      "position": [1120, 300]
    },
    {
      "parameters": {
        "amount": 30,
        "unit": "seconds"
      },
      "id": "wait-retry",
      "name": "Wait Before Retry",
      "type": "n8n-nodes-base.wait",
      "position": [900, 500]
    },
    {
      "parameters": {
        "chatId": "YOUR_CHAT_ID",
        "text": "=🎉 Исследование готово!\n\n📋 Тема: {{ $node['Start Research'].json.topic }}\n⏱️ Task ID: {{ $node['Start Research'].json.task_id }}\n\n📑 Результат:\n{{ $node['Check Status'].json.result }}"
      },
      "id": "send-telegram",
      "name": "Send to Telegram",
      "type": "n8n-nodes-base.telegram",
      "position": [1340, 200]
    }
  ]
}
```
</details>

## 🧪 Тестирование

### Тест 1: Ручной запуск
1. Активируйте workflow
2. Нажмите **"Execute Workflow"**  
3. В поле `topic` введите: `"Квантовые вычисления"`
4. Наблюдайте выполнение по шагам

### Тест 2: Webhook
```bash
curl -X POST "https://your-n8n.domain.com/webhook/start-research" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Нейросети в медицинской диагностике"}'
```

### Тест 3: Проверка получения данных
```bash
# Проверьте, что n8n может достучаться до AI Farm
curl http://100.110.253.23:8000/status
```

## 🔧 Troubleshooting

### Проблема: Timeout на HTTP requests
**Решение**: Увеличьте timeout в настройках HTTP Request нод до 300 секунд

### Проблема: Бесконечный цикл в ожидании
**Решение**: Добавьте счетчик попыток или максимальное время ожидания  

### Проблема: Ошибка подключения к API
**Решение**: Проверьте доступность AI Farm:
```bash
curl http://100.110.253.23:8000/
```

## 📊 Мониторинг и логи

### Отслеживание выполнения:
1. В n8n откройте **"Executions"** 
2. Следите за статусом каждой ноды
3. Изучайте данные между нодами

### Логи AI Farm:
```bash  
docker compose logs -f api worker
```

## 🚀 Дополнительные возможности

### Пакетная обработка тем
Модифицируйте workflow для обработки массива тем:
```json
{
  "topics": [
    "ИИ в образовании",
    "Блокчейн в логистике", 
    "VR в розничной торговле"
  ]
}
```

### Интеграция с базой данных
Добавьте ноды для сохранения результатов:
- PostgreSQL
- MongoDB  
- Airtable

### Уведомления о статусе
Настройте промежуточные уведомления:
- При запуске исследования
- При достижении 50% прогресса
- При завершении

## 📋 Чек-лист готовности

- [ ] n8n настроен и доступен
- [ ] AI Farm API отвечает на `http://100.110.253.23:8000`
- [ ] Telegram бот создан (если используется)
- [ ] Workflow импортирован
- [ ] Тестовый запуск выполнен успешно
- [ ] Цикл ожидания работает корректно
- [ ] Финальное действие доставляет результаты

---

**🎯 Результат**: Полностью автоматизированный конвейер для генерации исследований от триггера до доставки готового отчета!
