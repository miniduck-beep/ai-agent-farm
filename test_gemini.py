import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Список возможных названий моделей для тестирования
models_to_test = [
    "gemini-2.0-flash-exp",
    "gemini-exp-1206", 
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-pro"
]

print("🧪 Тестирование доступных моделей Gemini...")
print("=" * 50)

for model_name in models_to_test:
    print(f"\n🔍 Тестирую модель: {model_name}")
    try:
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.1)
        # Попробуем простой запрос
        response = llm.invoke("Привет! Ответь кратко: как дела?")
        print(f"✅ Модель '{model_name}' работает!")
        print(f"📝 Ответ: {response.content[:100]}...")
        break  # Если модель работает, прерываем цикл
    except Exception as e:
        print(f"❌ Модель '{model_name}' недоступна: {str(e)[:150]}...")

print("\n" + "=" * 50)
print("🏁 Тестирование завершено!")
