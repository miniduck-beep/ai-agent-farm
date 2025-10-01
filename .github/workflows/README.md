# 🤖 AI Agent Farm - CI/CD Workflows

Автоматизированные workflow для continuous integration и deployment.

## 📋 Workflows

### 🧪 test.yml - Continuous Integration
**Триггеры:** Push в main/develop, Pull Requests, Schedule (daily)

**Этапы:**
1. **Линтинг** - Black, flake8, mypy
2. **Unit тесты** - pytest на Python 3.11, 3.12
3. **Integration тесты** - с реальным Redis
4. **E2E тесты** - полный Docker setup
5. **Security сканирование** - safety, bandit

### 🚀 deploy.yml - Continuous Deployment
**Триггеры:** Release creation, Manual dispatch

**Этапы:**
1. **Сборка Docker образов** - multi-platform
2. **Security сканирование образов** - Trivy
3. **Production деплой** - SSH + Docker Compose
4. **Health проверки** - автоматическая валидация

### 📦 release.yml - Release Management
**Триггеры:** Git tags, Manual dispatch

**Возможности:**
- Автоматическая генерация Release Notes
- Создание GitHub Releases
- Docker образы в GitHub Container Registry

## ⚙️ Настройка

### GitHub Secrets
Добавьте следующие секреты в Settings → Secrets:

```bash
# Production Deployment
DEPLOY_SSH_KEY=<your-ssh-private-key>
DEPLOY_HOST=<your-server-ip-or-domain>
DEPLOY_USER=<ssh-username>

# API Keys для тестирования (опционально)
GOOGLE_API_KEY_TEST=<test-google-api-key>
SERPER_API_KEY_TEST=<test-serper-api-key>
```

### Server Setup
На продакшн сервере создайте:

```bash
# Создайте пользователя для деплоя
sudo useradd -m -s /bin/bash deploy
sudo usermod -aG docker deploy

# Настройте SSH ключи
mkdir -p /home/deploy/.ssh
echo "your-public-key" > /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys

# Подготовьте директорию проекта
sudo mkdir -p /opt/ai-agent-farm
sudo chown deploy:deploy /opt/ai-agent-farm

# Клонируйте репозиторий
cd /opt/ai-agent-farm
git clone https://github.com/your-username/ai-agent-farm.git .
```

## 🎯 Использование

### Автоматическое тестирование
Тесты запускаются автоматически при каждом push в main/develop.

### Создание релиза
```bash
# Создайте тег
git tag -a v2.1.0 -m "Release v2.1.0"
git push origin --tags

# Или используйте GitHub UI:
# Releases → Create a new release
```

### Ручной деплой
```bash
# В GitHub Actions:
# Actions → Deploy → Run workflow
# Выберите environment: production/staging
```

## 📊 Мониторинг

- **Test результаты:** Actions tab в GitHub
- **Coverage:** Codecov integration
- **Security:** Security tab в GitHub
- **Production health:** автоматические проверки после деплоя

## 🔧 Кастомизация

### Добавление новых тестов
Создайте тесты в `tests/` с соответствующими маркерами:
```python
@pytest.mark.unit
def test_new_feature():
    pass
```

### Изменение deployment процесса
Отредактируйте `deploy.yml` под ваши требования:
- Добавьте staging environment
- Настройте blue-green deployment
- Добавьте rollback механизм

### Настройка уведомлений
Добавьте Slack/Discord/Telegram уведомления:
```yaml
- name: 📬 Notify on deployment
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

**🎯 Fully automated DevOps pipeline для AI Agent Farm!**
