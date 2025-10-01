#!/usr/bin/env python3
"""
Тест мультиагентной системы AI Farm
"""
import os
import sys
sys.path.append('/home/su/ai-farm')

from app.main_crew import create_research_crew

def main():
    print("🧪 Тестирование мультиагентной системы AI Farm")
    print("=" * 60)
    
    # Проверка переменных окружения
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ОШИБКА: GOOGLE_API_KEY не найден в переменных окружения")
        return
    
    print(f"✅ GOOGLE_API_KEY настроен: {api_key[:20]}...")
    
    # Запуск тестового исследования
    test_topic = "Искусственный интеллект в медицине"
    
    try:
        print(f"🚀 Запуск исследования по теме: '{test_topic}'")
        result = create_research_crew(test_topic)
        
        print("\n" + "=" * 60)
        print("🎉 РЕЗУЛЬТАТ МУЛЬТИАГЕНТНОГО ИССЛЕДОВАНИЯ:")
        print("=" * 60)
        print(result)
        print("=" * 60)
        print("✅ Тест завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {str(e)}")

if __name__ == "__main__":
    main()
