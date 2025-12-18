# Описание реализации AI Chat Bot для веб-сайта с вакансиями

## Оглавление

1. [Архитектура системы](#архитектура-системы)
2. [Компоненты системы](#компоненты-системы)
3. [Модели данных](#модели-данных)
4. [Сервис чат-бота](#сервис-чат-бота)
5. [API эндпоинты](#api-эндпоинты)
6. [Работа с OpenAI](#работа-с-openai)
7. [Поток обработки запросов](#поток-обработки-запросов)
8. [Интеграция с фронтендом](#интеграция-с-фронтендом)
9. [Расширение функциональности](#расширение-функциональности)

---

## Архитектура системы

Система построена на основе **микросервисной архитектуры** с разделением на слои:

```
┌─────────────────────────────────────────┐
│         Frontend (React/Vue/etc)       │
└─────────────────┬───────────────────────┘
                  │ HTTP/REST API
┌─────────────────▼───────────────────────┐
│         FastAPI Application             │
│  ┌───────────────────────────────────┐  │
│  │      API Endpoints (main.py)      │  │
│  └───────────┬───────────────────────┘  │
│              │                           │
│  ┌───────────▼───────────────────────┐  │
│  │   ChatBotService (chat_service)   │  │
│  └───────────┬───────────────────────┘  │
│              │                           │
│  ┌───────────▼───────────────────────┐  │
│  │      Database Layer (database)     │  │
│  └───────────────────────────────────┘  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         OpenAI API                      │
└─────────────────────────────────────────┘
```

### Принципы проектирования:

- **Разделение ответственности**: каждый модуль отвечает за свою область
- **RESTful API**: стандартизированные HTTP эндпоинты
- **Асинхронность**: использование async/await для эффективной обработки запросов
- **Типизация**: использование Pydantic для валидации данных
- **Расширяемость**: легко заменить мок-данные на реальную БД

---

## Компоненты системы

### 1. `main.py` - FastAPI приложение

**Назначение**: Точка входа приложения, определение API эндпоинтов

**Основные функции**:
- Инициализация FastAPI приложения
- Настройка CORS для работы с фронтендом
- Определение REST API эндпоинтов
- Обработка HTTP запросов и ответов
- Интеграция с ChatBotService и Database

**Ключевые особенности**:
```python
# CORS настройка для кросс-доменных запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. `chat_service.py` - Сервис чат-бота

**Назначение**: Логика взаимодействия с OpenAI API

**Основные классы и методы**:

#### `ChatBotService`
- `__init__(api_key)`: Инициализация с API ключом OpenAI
- `_build_system_prompt(vacancies_data)`: Создание системного промпта
- `_prepare_messages(...)`: Подготовка сообщений для OpenAI
- `get_chat_response(request, vacancies_data)`: Получение ответа от бота
- `get_structured_recommendations(...)`: Структурированные рекомендации

**Особенности реализации**:
- Использование контекста вакансий в промпте
- Обработка истории разговора
- Извлечение структурированных данных из ответов
- Обработка ошибок

### 3. `models.py` - Модели данных

**Назначение**: Определение структуры данных с помощью Pydantic

**Основные модели**:

- `Company`: Информация о компании
- `Vacancy`: Информация о вакансии
- `ChatMessage`: Сообщение в чате
- `ChatRequest`: Запрос к чат-боту
- `ChatResponse`: Ответ от чат-бота

**Преимущества Pydantic**:
- Автоматическая валидация данных
- Сериализация/десериализация JSON
- Автогенерация документации API
- Type hints для IDE

### 4. `database.py` - Слой данных

**Назначение**: Абстракция для работы с данными о вакансиях и компаниях

**Класс `Database`**:
- `get_all_vacancies()`: Получить все вакансии
- `get_vacancy_by_id(id)`: Получить вакансию по ID
- `get_vacancies_by_skills(skills)`: Фильтрация по навыкам
- `get_vacancies_data_for_chat()`: Данные для чат-бота

**Текущая реализация**: Мок-данные в памяти

**Для продакшена**: Заменить на подключение к PostgreSQL/MongoDB/etc.

---

## Модели данных

### Vacancy (Вакансия)

```python
class Vacancy(BaseModel):
    id: int                          # Уникальный идентификатор
    title: str                       # Название вакансии
    description: str                 # Описание
    company_id: int                  # ID компании
    company: Optional[Company]       # Объект компании
    location: Optional[str]          # Локация
    salary_min: Optional[float]      # Минимальная зарплата
    salary_max: Optional[float]      # Максимальная зарплата
    job_type: Optional[JobType]      # Тип работы (full_time, part_time, etc.)
    experience_level: Optional[ExperienceLevel]  # Уровень опыта
    required_skills: List[str]       # Обязательные навыки
    preferred_skills: List[str]      # Предпочтительные навыки
    posted_date: Optional[datetime]  # Дата публикации
```

### ChatRequest (Запрос к чат-боту)

```python
class ChatRequest(BaseModel):
    message: str                     # Сообщение пользователя
    conversation_history: Optional[List[ChatMessage]]  # История разговора
    user_skills: Optional[List[str]] # Навыки пользователя
    user_experience: Optional[str]   # Уровень опыта
```

### ChatResponse (Ответ чат-бота)

```python
class ChatResponse(BaseModel):
    response: str                    # Текстовый ответ бота
    suggested_vacancies: Optional[List[int]]  # ID рекомендованных вакансий
    skill_recommendations: Optional[List[str]]  # Рекомендации по навыкам
```

---

## Сервис чат-бота

### Системный промпт

Системный промпт определяет поведение чат-бота:

```python
"""Ты - полезный AI-ассистент для веб-сайта с вакансиями и компаниями. 
Твоя задача:
1. Помогать пользователям подобрать подходящие вакансии
2. Отвечать на вопросы о вакансиях, компаниях, требованиях
3. Давать рекомендации по навыкам, которые стоит подтянуть
"""
```

### Обработка контекста

Чат-бот получает контекст о:
- Доступных вакансиях (название, навыки, уровень)
- Навыках пользователя
- Уровне опыта пользователя
- Истории разговора (последние 10 сообщений)

### Извлечение структурированных данных

Из текстового ответа бота извлекаются:
- **ID вакансий**: через регулярные выражения
- **Рекомендации по навыкам**: через анализ текста

**Пример улучшения**: Использовать структурированный вывод OpenAI (JSON mode)

---

## API эндпоинты

### POST `/api/chat`

**Назначение**: Основной эндпоинт для общения с чат-ботом

**Тело запроса**:
```json
{
  "message": "Помоги найти вакансию Python разработчика",
  "conversation_history": [
    {"role": "user", "content": "Привет"},
    {"role": "assistant", "content": "Привет! Чем могу помочь?"}
  ],
  "user_skills": ["Python", "Django", "PostgreSQL"],
  "user_experience": "middle"
}
```

**Ответ**:
```json
{
  "response": "На основе ваших навыков рекомендую...",
  "suggested_vacancies": [1, 4],
  "skill_recommendations": ["Docker", "Kubernetes"]
}
```

**Обработка**:
1. Валидация запроса через Pydantic
2. Получение данных о вакансиях из БД
3. Вызов ChatBotService.get_chat_response()
4. Возврат ответа пользователю

### POST `/api/recommendations`

**Назначение**: Получить структурированные рекомендации

**Параметры**:
- `user_skills`: List[str] - навыки пользователя
- `user_experience`: Optional[str] - уровень опыта

**Ответ**:
```json
{
  "recommended_vacancies": [...],  // Полные объекты вакансий
  "skill_recommendations": ["Python", "Docker"],
  "analysis": {...}  // Дополнительный анализ
}
```

**Особенности**:
- Использует JSON mode OpenAI для структурированного ответа
- Возвращает полные объекты вакансий, а не только ID

### GET `/api/vacancies`

**Назначение**: Получить список вакансий с фильтрацией

**Параметры запроса**:
- `skills`: str (через запятую) - фильтр по навыкам
- `experience_level`: str - фильтр по уровню опыта

**Пример**:
```
GET /api/vacancies?skills=Python,React&experience_level=middle
```

### GET `/api/vacancies/{vacancy_id}`

**Назначение**: Получить детальную информацию о вакансии

### GET `/api/companies`

**Назначение**: Получить список всех компаний

### GET `/api/companies/{company_id}`

**Назначение**: Получить информацию о компании

### GET `/api/health`

**Назначение**: Проверка здоровья сервиса

---

## Работа с OpenAI

### Модель

По умолчанию используется `gpt-4-turbo-preview`:
- Высокое качество ответов
- Поддержка структурированного вывода
- Более высокая стоимость

**Альтернатива**: `gpt-3.5-turbo` для экономии средств

### Параметры запроса

```python
response = self.client.chat.completions.create(
    model=self.model,
    messages=messages,
    temperature=0.7,      # Креативность (0-1)
    max_tokens=1000        # Максимальная длина ответа
)
```

### Структурированный вывод

Для получения JSON ответов:
```python
response = self.client.chat.completions.create(
    model=self.model,
    messages=messages,
    response_format={"type": "json_object"}  # JSON mode
)
```

### Обработка ошибок

- Проверка наличия API ключа при инициализации
- Try-catch блоки для обработки ошибок API
- Возврат понятных сообщений об ошибках пользователю

---

## Поток обработки запросов

### Сценарий 1: Подбор вакансий

```
1. Пользователь: "Помоги найти вакансию Python разработчика"
   ↓
2. Frontend → POST /api/chat
   {
     "message": "...",
     "user_skills": ["Python", "Django"],
     "user_experience": "middle"
   }
   ↓
3. FastAPI валидирует запрос (Pydantic)
   ↓
4. Получение данных о вакансиях из БД
   ↓
5. ChatBotService:
   - Создает системный промпт с контекстом вакансий
   - Подготавливает сообщения для OpenAI
   - Отправляет запрос в OpenAI API
   ↓
6. OpenAI возвращает ответ
   ↓
7. Извлечение структурированных данных (ID вакансий, навыки)
   ↓
8. Возврат ответа пользователю:
   {
     "response": "Рекомендую следующие вакансии...",
     "suggested_vacancies": [1, 4],
     "skill_recommendations": ["Docker"]
   }
   ↓
9. Frontend отображает ответ и рекомендации
```

### Сценарий 2: Вопрос о вакансии

```
1. Пользователь: "Какие навыки нужны для Data Scientist?"
   ↓
2. ChatBotService получает контекст о вакансиях Data Scientist
   ↓
3. OpenAI анализирует требования и формирует ответ
   ↓
4. Возврат ответа с рекомендациями
```

### Сценарий 3: Рекомендации по навыкам

```
1. Пользователь: "Что мне подтянуть для работы Python разработчиком?"
   ↓
2. ChatBotService анализирует:
   - Навыки пользователя
   - Требования вакансий Python разработчика
   - Разницу между навыками пользователя и требованиями
   ↓
3. Формирование рекомендаций
   ↓
4. Возврат списка навыков для изучения
```

---

## Интеграция с фронтендом

### CORS настройка

API настроен для работы с любым фронтендом через CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене: конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Пример интеграции (React)

```javascript
const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  
  const sendMessage = async () => {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: input,
        conversation_history: messages,
        user_skills: ['Python', 'React'],
        user_experience: 'middle'
      })
    });
    
    const data = await response.json();
    setMessages([...messages, 
      { role: 'user', content: input },
      { role: 'assistant', content: data.response }
    ]);
  };
  
  return (/* UI компонента */);
};
```

### Пример интеграции (Vue.js)

```javascript
export default {
  data() {
    return {
      messages: [],
      input: '',
      apiUrl: 'http://localhost:8000'
    }
  },
  methods: {
    async sendMessage() {
      const response = await fetch(`${this.apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: this.input,
          conversation_history: this.messages,
          user_skills: ['Python'],
          user_experience: 'middle'
        })
      });
      
      const data = await response.json();
      this.messages.push(
        { role: 'user', content: this.input },
        { role: 'assistant', content: data.response }
      );
    }
  }
}
```

### Тестовая HTML страница

Файл `test_frontend.html` содержит готовую HTML страницу для тестирования:
- Интерфейс чата
- Настройка API URL
- Настройка навыков и опыта пользователя
- Отображение ответов и рекомендаций

---

## Расширение функциональности

### 1. Подключение реальной БД

Заменить `database.py` на подключение к PostgreSQL:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://user:pass@localhost/db")
Session = sessionmaker(bind=engine)

class Database:
    def __init__(self):
        self.session = Session()
    
    def get_all_vacancies(self):
        return self.session.query(Vacancy).all()
```

### 2. Кэширование ответов

Добавить кэширование частых запросов:

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_cached_response(message_hash):
    # Кэширование ответов OpenAI
    pass
```

### 3. Логирование

Добавить логирование запросов и ответов:

```python
import logging

logger = logging.getLogger(__name__)

async def chat(request: ChatRequest):
    logger.info(f"Chat request: {request.message}")
    # ...
    logger.info(f"Chat response: {response.response}")
```

### 4. Аутентификация

Добавить JWT токены для защиты API:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    # Проверка токена
    pass

@app.post("/api/chat", dependencies=[Depends(verify_token)])
async def chat(request: ChatRequest):
    # ...
```

### 5. Rate Limiting

Ограничение количества запросов:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: ChatRequest):
    # ...
```

### 6. Улучшение извлечения данных

Использовать структурированный вывод OpenAI:

```python
response = self.client.chat.completions.create(
    model=self.model,
    messages=messages,
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "chat_response",
            "schema": {
                "type": "object",
                "properties": {
                    "suggested_vacancies": {
                        "type": "array",
                        "items": {"type": "integer"}
                    },
                    "skill_recommendations": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        }
    }
)
```

### 7. Поддержка нескольких языков

Добавить определение языка и переключение промптов:

```python
def detect_language(text: str) -> str:
    # Определение языка текста
    return "ru"  # или "en"

def get_system_prompt(language: str) -> str:
    prompts = {
        "ru": "Ты - полезный AI-ассистент...",
        "en": "You are a helpful AI assistant..."
    }
    return prompts.get(language, prompts["ru"])
```

### 8. Аналитика и метрики

Добавить сбор метрик:

```python
from prometheus_client import Counter, Histogram

chat_requests = Counter('chat_requests_total', 'Total chat requests')
response_time = Histogram('chat_response_time', 'Chat response time')

@app.post("/api/chat")
async def chat(request: ChatRequest):
    chat_requests.inc()
    with response_time.time():
        response = await chat_service.get_chat_response(request)
    return response
```

---

## Безопасность

### Рекомендации для продакшена:

1. **API ключи**: Хранить в переменных окружения, не коммитить в репозиторий
2. **CORS**: Ограничить `allow_origins` конкретными доменами
3. **Валидация**: Все входные данные валидируются через Pydantic
4. **Rate Limiting**: Ограничить количество запросов от одного пользователя
5. **Аутентификация**: Добавить JWT токены или API ключи
6. **Логирование**: Логировать запросы без чувствительных данных
7. **HTTPS**: Использовать HTTPS в продакшене

---

## Производительность

### Оптимизации:

1. **Асинхронность**: Использование async/await для неблокирующих операций
2. **Кэширование**: Кэширование частых запросов и данных о вакансиях
3. **Пакетная обработка**: Группировка запросов к OpenAI
4. **Connection pooling**: Для подключений к БД
5. **Ограничение истории**: Хранение только последних N сообщений

### Мониторинг:

- Время ответа API
- Количество запросов
- Ошибки OpenAI API
- Использование токенов OpenAI

---

## Тестирование

### Unit тесты

```python
import pytest
from chat_service import ChatBotService

def test_chat_service_initialization():
    service = ChatBotService(api_key="test_key")
    assert service.client is not None

def test_system_prompt_generation():
    service = ChatBotService(api_key="test_key")
    prompt = service._build_system_prompt([])
    assert "AI-ассистент" in prompt
```

### Integration тесты

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/api/chat", json={
        "message": "Привет",
        "user_skills": ["Python"]
    })
    assert response.status_code == 200
    assert "response" in response.json()
```

---

## Заключение

Реализация представляет собой масштабируемую систему для AI чат-бота с вакансиями:

- ✅ Модульная архитектура
- ✅ RESTful API
- ✅ Интеграция с OpenAI
- ✅ Готовность к интеграции с фронтендом
- ✅ Возможность расширения функциональности
- ✅ Документированный код

Система готова к использованию и может быть легко расширена для продакшена.

