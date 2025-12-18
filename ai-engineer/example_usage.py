"""
Пример использования API чат-бота
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def example_chat():
    """Пример общения с чат-ботом"""
    print("=== Пример общения с чат-ботом ===\n")
    
    url = f"{BASE_URL}/api/chat"
    
    # Первое сообщение
    data = {
        "message": "Привет! Помоги мне найти подходящую вакансию",
        "user_skills": ["Python", "Django", "PostgreSQL"],
        "user_experience": "middle"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Пользователь: {data['message']}")
    print(f"Бот: {result['response']}\n")
    
    # Продолжение разговора
    conversation_history = [
        {"role": "user", "content": data["message"]},
        {"role": "assistant", "content": result["response"]}
    ]
    
    data2 = {
        "message": "А какие навыки мне стоит подтянуть?",
        "conversation_history": conversation_history,
        "user_skills": ["Python", "Django", "PostgreSQL"],
        "user_experience": "middle"
    }
    
    response2 = requests.post(url, json=data2)
    result2 = response2.json()
    
    print(f"Пользователь: {data2['message']}")
    print(f"Бот: {result2['response']}\n")
    
    if result2.get("skill_recommendations"):
        print(f"Рекомендуемые навыки: {', '.join(result2['skill_recommendations'])}")


def example_recommendations():
    """Пример получения структурированных рекомендаций"""
    print("\n=== Пример получения рекомендаций ===\n")
    
    url = f"{BASE_URL}/api/recommendations"
    
    params = {
        "user_skills": ["Python", "React", "JavaScript"],
        "user_experience": "middle"
    }
    
    response = requests.post(url, json=params)
    result = response.json()
    
    print(f"Навыки пользователя: {', '.join(params['user_skills'])}")
    print(f"Уровень опыта: {params['user_experience']}\n")
    
    if result.get("recommended_vacancies"):
        print("Рекомендованные вакансии:")
        for vac in result["recommended_vacancies"]:
            print(f"  - {vac['title']} (ID: {vac['id']})")
            print(f"    Компания: {vac.get('company', {}).get('name', 'N/A')}")
            print(f"    Навыки: {', '.join(vac.get('required_skills', []))}\n")
    
    if result.get("skill_recommendations"):
        print(f"Рекомендации по навыкам: {', '.join(result['skill_recommendations'])}")


def example_get_vacancies():
    """Пример получения списка вакансий"""
    print("\n=== Пример получения вакансий ===\n")
    
    url = f"{BASE_URL}/api/vacancies"
    
    # Все вакансии
    response = requests.get(url)
    vacancies = response.json()
    
    print(f"Всего вакансий: {len(vacancies)}\n")
    
    # Фильтрация по навыкам
    response2 = requests.get(url, params={"skills": "Python,React"})
    filtered = response2.json()
    
    print(f"Вакансии с навыками Python или React: {len(filtered)}")
    for vac in filtered:
        print(f"  - {vac['title']} (ID: {vac['id']})")


def example_questions():
    """Примеры вопросов к чат-боту"""
    print("\n=== Примеры вопросов ===\n")
    
    questions = [
        "Какие вакансии есть для Python разработчика?",
        "Что нужно знать для работы Data Scientist?",
        "Какие компании ищут Frontend разработчиков?",
        "Какие навыки нужны для вакансии Full Stack Developer?",
    ]
    
    url = f"{BASE_URL}/api/chat"
    
    for question in questions:
        data = {
            "message": question,
            "user_skills": ["Python"],
            "user_experience": "middle"
        }
        
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"Вопрос: {question}")
        print(f"Ответ: {result['response'][:200]}...\n")


if __name__ == "__main__":
    print("Примеры использования AI Chat Bot API\n")
    print("=" * 50)
    
    try:
        # Проверка доступности сервера
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code != 200:
            print("Ошибка: Сервер не доступен")
            exit(1)
        
        # Запуск примеров
        example_chat()
        example_recommendations()
        example_get_vacancies()
        example_questions()
        
    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу")
        print("Убедитесь, что сервер запущен на http://localhost:8000")
    except Exception as e:
        print(f"Ошибка: {e}")

