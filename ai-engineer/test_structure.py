"""
Скрипт для проверки структуры проекта и импортов
(без необходимости реального OpenAI API ключа)
"""
import sys
import os

def check_imports():
    """Проверка импортов основных модулей"""
    print("Проверка структуры проекта...\n")
    
    errors = []
    
    # Проверка файлов
    required_files = [
        "main.py",
        "chat_service.py",
        "models.py",
        "database.py",
        "requirements.txt"
    ]
    
    print("Проверка наличия файлов:")
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - НЕ НАЙДЕН")
            errors.append(f"Отсутствует файл: {file}")
    
    # Проверка импортов
    print("\nПроверка импортов:")
    try:
        from models import ChatRequest, ChatResponse, Vacancy, Company
        print("  ✓ models.py - импорты работают")
    except Exception as e:
        print(f"  ✗ models.py - ошибка импорта: {e}")
        errors.append(f"Ошибка импорта models.py: {e}")
    
    try:
        from database import db, Database
        print("  ✓ database.py - импорты работают")
    except Exception as e:
        print(f"  ✗ database.py - ошибка импорта: {e}")
        errors.append(f"Ошибка импорта database.py: {e}")
    
    try:
        from chat_service import ChatBotService
        print("  ✓ chat_service.py - импорты работают")
    except Exception as e:
        print(f"  ✗ chat_service.py - ошибка импорта: {e}")
        errors.append(f"Ошибка импорта chat_service.py: {e}")
    
    try:
        import main
        print("  ✓ main.py - импорты работают")
    except Exception as e:
        print(f"  ✗ main.py - ошибка импорта: {e}")
        errors.append(f"Ошибка импорта main.py: {e}")
    
    # Проверка переменных окружения
    print("\nПроверка конфигурации:")
    if os.path.exists(".env"):
        print("  ✓ .env файл существует")
    else:
        print("  ⚠ .env файл не найден (создайте его на основе .env.example)")
    
    if os.getenv("OPENAI_API_KEY"):
        print("  ✓ OPENAI_API_KEY установлен")
    else:
        print("  ⚠ OPENAI_API_KEY не установлен (установите в .env файле)")
    
    # Итоги
    print("\n" + "="*50)
    if errors:
        print("НАЙДЕНЫ ОШИБКИ:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✓ Структура проекта в порядке!")
        print("\nСледующие шаги:")
        print("  1. Установите зависимости: pip install -r requirements.txt")
        print("  2. Создайте .env файл с OPENAI_API_KEY")
        print("  3. Запустите сервер: python main.py")
        return True

if __name__ == "__main__":
    success = check_imports()
    sys.exit(0 if success else 1)

