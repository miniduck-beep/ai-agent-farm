# 🔗 AI Agent Farm + n8n Integration

Готовый к использованию воркфлоу для полной автоматизации исследований с AI Agent Farm.

## 🚀 Возможности воркфлоу

- **Webhook Trigger**: Запуск исследований через внешние системы
- **Асинхронная обработка**: Автоматическое отслеживание прогресса
- **Уведомления**: Отправка результатов в Telegram или webhook
- **Retry Logic**: Автоматические повторные проверки статуса
- **Форматирование**: Красивое оформление результатов

## 📋 Что включено

1. **Webhook Start Node** - принимает запросы на исследование  
2. **Research API Call** - запускает исследование в AI Agent Farm
3. **Status Polling** - проверяет готовность результатов
4. **Result Formatting** - форматирует результаты
5. **Notification Nodes** - отправляет уведомления

## 🛠️ Быстрая настройка

### 1. Импорт воркфлоу
```bash
# 1. Скопируйте содержимое ai-agent-farm-workflow.json
# 2. В n8n: Templates → Import from JSON → Paste
# 3. Нажмите Import
```

### 2. Настройка подключения к AI Farm
Найдите в воркфлоу узлы "Start Research" и "Check Status" и замените:
```
YOUR_AI_FARM_HOST → ваш адрес (например: 100.110.253.23)
```

### 3. Настройка API ключа (опционально)
Если включена авторизация:
```bash
# n8n: Credentials → Add → HTTP Header Auth
# Name: AI Agent Farm API
# Header Name: X-API-Key
# Header Value: your_api_key_here
```

### 4. Настройка Telegram (опционально)
```bash
# n8n: Credentials → Add → Telegram
# Bot Token: получите у @BotFather
# Chat ID: ваш Telegram Chat ID
```

## 🧪 Тестирование

### Тест через webhook
```bash
curl -X POST "YOUR_N8N_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Будущее искусственного интеллекта",
    "crew_type": "business_analysis",
    "language": "ru",
    "depth": "comprehensive"
  }'
```

### Ожидаемый результат
1. ✅ Воркфлоу запустится автоматически
2. 🔄 AI Agent Farm начнет исследование  
3. ⏱️ Статус будет проверяться каждые 30 секунд
4. 📨 По завершении придет уведомление в Telegram
5. 🔗 Результат отправится на webhook

## ⚙️ Настройки воркфлоу

### Параметры запроса
```json
{
  "topic": "string (обязательно)",
  "crew_type": "business_analysis|seo_content|tech_research", 
  "language": "ru|en",
  "depth": "basic|standard|comprehensive"
}
```

### Интервалы проверки
- Первая проверка: через 30 секунд
- Повторные проверки: каждые 30 секунд
- Максимум итераций: без ограничений (пока не SUCCESS)

## 🔧 Кастомизация

### Добавить email уведомления
```bash
# Добавьте Email node после Format Result
# Настройте SMTP credentials
# Подключите к выходу Format Result
```

### Изменить интервалы
```bash
# Измените параметр "amount" в узлах Wait
# Рекомендуется: 15-60 секунд
```

### Добавить обработку ошибок
```bash
# Добавьте Error Trigger node
# Настройте уведомления об ошибках
```

## 🏆 Production Tips

1. **Мониторинг**: Включите execution history в n8n
2. **Ретраи**: Настройте retry в HTTP request nodes  
3. **Таймауты**: Установите разумные timeout значения
4. **Логирование**: Используйте Console logs для отладки
5. **Безопасность**: Храните credentials в n8n Vault

## 🆘 Troubleshooting

### Воркфлоу не запускается
- ✅ Проверьте webhook URL активен
- ✅ Убедитесь что JSON валидный
- ✅ Проверьте AI Farm доступен

### Исследование не завершается  
- ✅ Проверьте логи AI Agent Farm
- ✅ Убедитесь что API ключи корректны
- ✅ Проверьте тему исследования

### Уведомления не приходят
- ✅ Проверьте Telegram credentials
- ✅ Убедитесь что bot добавлен в чат
- ✅ Проверьте Chat ID

**Готово! Ваш n8n теперь полностью интегрирован с AI Agent Farm! 🎉**
