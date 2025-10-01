#!/usr/bin/env python3
"""
AI Agent Farm - Integration Test Suite
=====================================
Быстрый тест всей инфраструктуры
"""

import requests
import time
import sys

API_BASE = "http://localhost:8000"

def test_api_health():
    """Тест здоровья API"""
    print("🏥 Тестируем health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API здоров: {data['status']}")
            return True
        else:
            print(f"❌ API нездоров: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
        return False

def test_showcase_endpoints():
    """Тест showcase endpoints"""
    print("🎯 Тестируем showcase endpoints...")
    
    # Тест /showcase
    try:
        response = requests.get(f"{API_BASE}/showcase")
        if response.status_code == 200:
            data = response.json()
            teams = data.get("showcase_teams", {})
            print(f"✅ Showcase teams доступны: {len(teams)} команд")
            return True
        else:
            print("❌ Showcase endpoint недоступен")
            return False
    except Exception as e:
        print(f"❌ Ошибка showcase endpoint: {e}")
        return False

def test_crews_enhanced():
    """Тест расширенного crews endpoint"""
    print("🔍 Тестируем enhanced crews endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/crews/enhanced")
        if response.status_code == 200:
            data = response.json()
            total = data.get("total_crews", 0)
            categories = data.get("categories", {})
            print(f"✅ Enhanced crews: {total} команд ({categories})")
            return True
        else:
            print("❌ Enhanced crews endpoint недоступен")
            return False
    except Exception as e:
        print(f"❌ Ошибка enhanced crews: {e}")
        return False

def test_create_sample_research():
    """Тест создания простого исследования"""
    print("📝 Тестируем создание исследования...")
    
    try:
        response = requests.post(f"{API_BASE}/research", json={
            "topic": "Integration test",
            "crew_type": "general",
            "language": "ru", 
            "depth": "basic"
        })
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get("task_id")
            print(f"✅ Исследование создано: {task_id}")
            return task_id
        else:
            print(f"❌ Не удалось создать исследование: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ошибка создания исследования: {e}")
        return None

def test_task_status(task_id):
    """Тест проверки статуса задачи"""
    if not task_id:
        return False
        
    print("📊 Тестируем статус задачи...")
    
    try:
        response = requests.get(f"{API_BASE}/result/{task_id}")
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "UNKNOWN")
            print(f"✅ Статус задачи: {status}")
            return True
        else:
            print("❌ Не удалось получить статус")
            return False
    except Exception as e:
        print(f"❌ Ошибка статуса задачи: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 AI Agent Farm - Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_api_health,
        test_showcase_endpoints, 
        test_crews_enhanced
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    # Дополнительный тест создания задачи
    task_id = test_create_sample_research()
    if task_id:
        passed += 1
        time.sleep(2)  # Ждем 2 секунды
        if test_task_status(task_id):
            passed += 1
        total += 2
    else:
        total += 2
    
    print()
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"   Пройдено: {passed}/{total}")
    print(f"   Процент успеха: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Система готова к использованию.")
        return 0
    else:
        print("⚠️ Некоторые тесты провалились. Проверьте систему.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
