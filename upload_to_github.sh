#!/bin/bash

echo "🚀 Загружаем AI Agent Farm на GitHub..."

# Тестируем SSH соединение
echo "🔍 Проверяем SSH соединение с GitHub..."
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "✅ SSH соединение установлено!"
    
    # Загружаем проект
    echo "📦 Загружаем код на GitHub..."
    git push -u origin main
    
    echo ""
    echo "🎉 AI Agent Farm успешно загружен на GitHub!"
    echo "📍 Репозиторий: https://github.com/miniduck-beep/ai-agent-farm"
    echo ""
    echo "🚀 Что делать дальше:"
    echo "1. Настройте описание и теги репозитория"
    echo "2. Включите Issues и Discussions"
    echo "3. Настройте GitHub Pages для документации"
    echo "4. Создайте первый release (v1.0.0)"
    
else
    echo "❌ SSH ключ не добавлен на GitHub"
    echo ""
    echo "🔑 Скопируйте и добавьте SSH ключ:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "📍 Добавить здесь: https://github.com/settings/ssh"
    echo "🔄 После добавления запустите: ./upload_to_github.sh"
fi
