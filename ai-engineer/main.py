from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from dotenv import load_dotenv

from models import ChatRequest, ChatResponse, Vacancy, Company
from chat_service import ChatBotService
from database import db

# Загружаем переменные окружения
load_dotenv()

app = FastAPI(
    title="AI Chat Bot для вакансий",
    description="AI чат-бот для подбора вакансий, ответов на вопросы и рекомендаций по навыкам",
    version="1.0.0"
)

# Настройка CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация сервиса чат-бота
try:
    chat_service = ChatBotService()
except ValueError as e:
    print(f"Внимание: {e}")
    print("Установите OPENAI_API_KEY в переменных окружения или в .env файле")
    chat_service = None


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "AI Chat Bot API для вакансий",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "recommendations": "/api/recommendations",
            "vacancies": "/api/vacancies",
            "companies": "/api/companies"
        }
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Основной эндпоинт для общения с чат-ботом
    
    - **message**: Сообщение пользователя
    - **conversation_history**: История разговора (опционально)
    - **user_skills**: Навыки пользователя для контекста (опционально)
    - **user_experience**: Уровень опыта пользователя (опционально)
    """
    if not chat_service:
        raise HTTPException(
            status_code=500,
            detail="Chat service не инициализирован. Проверьте OPENAI_API_KEY"
        )
    
    # Получаем данные о вакансиях для контекста
    vacancies_data = db.get_vacancies_data_for_chat()
    
    # Получаем ответ от чат-бота
    response = await chat_service.get_chat_response(request, vacancies_data)
    
    return response


@app.post("/api/recommendations")
async def get_recommendations(
    user_skills: List[str],
    user_experience: Optional[str] = None
):
    """
    Получить структурированные рекомендации по вакансиям и навыкам
    
    - **user_skills**: Список навыков пользователя
    - **user_experience**: Уровень опыта (junior, middle, senior, lead)
    """
    if not chat_service:
        raise HTTPException(
            status_code=500,
            detail="Chat service не инициализирован. Проверьте OPENAI_API_KEY"
        )
    
    vacancies_data = db.get_vacancies_data_for_chat()
    
    recommendations = chat_service.get_structured_recommendations(
        user_skills=user_skills,
        user_experience=user_experience,
        vacancies_data=vacancies_data
    )
    
    # Получаем полную информацию о рекомендованных вакансиях
    recommended_vacancies = []
    if "recommended_vacancy_ids" in recommendations:
        for vac_id in recommendations["recommended_vacancy_ids"]:
            vacancy = db.get_vacancy_by_id(vac_id)
            if vacancy:
                recommended_vacancies.append(vacancy)
    
    return {
        "recommended_vacancies": recommended_vacancies,
        "skill_recommendations": recommendations.get("skill_recommendations", []),
        "analysis": recommendations
    }


@app.get("/api/vacancies", response_model=List[Vacancy])
async def get_vacancies(
    skills: Optional[str] = None,
    experience_level: Optional[str] = None
):
    """
    Получить список вакансий
    
    - **skills**: Фильтр по навыкам (через запятую)
    - **experience_level**: Фильтр по уровню опыта
    """
    vacancies = db.get_all_vacancies()
    
    # Фильтрация по навыкам
    if skills:
        skills_list = [s.strip() for s in skills.split(",")]
        vacancies = db.get_vacancies_by_skills(skills_list)
    
    # Фильтрация по уровню опыта
    if experience_level:
        vacancies = [v for v in vacancies if v.experience_level and v.experience_level.value == experience_level]
    
    return vacancies


@app.get("/api/vacancies/{vacancy_id}", response_model=Vacancy)
async def get_vacancy(vacancy_id: int):
    """Получить вакансию по ID"""
    vacancy = db.get_vacancy_by_id(vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")
    return vacancy


@app.get("/api/companies", response_model=List[Company])
async def get_companies():
    """Получить список всех компаний"""
    return db.get_all_companies()


@app.get("/api/companies/{company_id}", response_model=Company)
async def get_company(company_id: int):
    """Получить компанию по ID"""
    company = db.get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    return company


@app.get("/api/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {
        "status": "healthy",
        "chat_service_available": chat_service is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

