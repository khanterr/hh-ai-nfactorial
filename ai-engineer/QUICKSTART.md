# Быстрый старт

## Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 2: Настройка OpenAI API Key

1. Получите API ключ на https://platform.openai.com/api-keys
2. Создайте файл `.env` в корне проекта:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Шаг 3: Запуск сервера

```bash
python main.py
```

Или:
```bash
uvicorn main:app --reload
```

Сервер запустится на `http://localhost:8000`

## Шаг 4: Проверка работы

Откройте в браузере:
- Документация API: http://localhost:8000/docs
- Проверка здоровья: http://localhost:8000/api/health

## Шаг 5: Тестирование

Запустите примеры:
```bash
python example_usage.py
```

Или протестируйте через curl:

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Привет! Помоги найти вакансию Python разработчика",
    "user_skills": ["Python", "Django"],
    "user_experience": "middle"
  }'
```

## Интеграция с фронтендом

API готов к использованию. Пример запроса из JavaScript:

```javascript
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Помоги найти вакансию',
    user_skills: ['Python', 'React'],
    user_experience: 'middle'
  })
});

const data = await response.json();
console.log(data.response); // Ответ чат-бота
```

## Основные эндпоинты

- `POST /api/chat` - общение с чат-ботом
- `POST /api/recommendations` - структурированные рекомендации
- `GET /api/vacancies` - список вакансий
- `GET /api/vacancies/{id}` - детали вакансии
- `GET /api/companies` - список компаний

Подробнее в README.md

