"""
Запуск веб-интерфейса AI Agent Farm
==================================
"""

import subprocess
import sys
import os

def main():
    """Запускает Streamlit веб-интерфейс"""
    
    print("🚀 Запуск AI Agent Farm Web Interface...")
    print("📍 Интерфейс будет доступен по адресу: http://localhost:8501")
    print("⏹️  Для остановки используйте Ctrl+C")
    print("-" * 50)
    
    try:
        # Запуск Streamlit приложения
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app/web_interface.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--theme.primaryColor=#FF6B6B",
            "--theme.backgroundColor=#FFFFFF", 
            "--theme.secondaryBackgroundColor=#F0F2F6"
        ])
    except KeyboardInterrupt:
        print("\n👋 Веб-интерфейс остановлен")
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")

if __name__ == "__main__":
    main()
