import os
import requests

# Настройка прокси
proxies = {
    'http': 'http://172.17.0.1:10809',
    'https': 'http://172.17.0.1:10809'
}

api_key = "AIzaSyDfWoolnlVFWAJ4Phu__t7AQFGeIEzmm6I"
url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"

print("🧪 Тестирование Google Gemini API через VPN...")

try:
    response = requests.get(url, proxies=proxies, timeout=15)
    print(f"✅ Статус ответа: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"🎉 API доступен! Найдено моделей: {len(data.get('models', []))}")
        
        # Показываем несколько доступных моделей
        models = data.get('models', [])
        print("📋 Доступные модели:")
        for model in models[:5]:
            print(f"  - {model['name']}")
    else:
        print(f"❌ Ошибка API: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Ошибка подключения: {e}")
