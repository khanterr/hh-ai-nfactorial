from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class ExperienceLevel(str, Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"


class Company(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None


class Vacancy(BaseModel):
    id: int
    title: str
    description: str
    company_id: int
    company: Optional[Company] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    posted_date: Optional[datetime] = None


class ChatMessage(BaseModel):
    role: str = Field(..., description="Роль: 'user' или 'assistant'")
    content: str = Field(..., description="Содержание сообщения")


class ChatRequest(BaseModel):
    message: str = Field(..., description="Сообщение пользователя")
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=[], description="История разговора"
    )
    user_skills: Optional[List[str]] = Field(
        default=[], description="Навыки пользователя для подбора вакансий"
    )
    user_experience: Optional[str] = Field(
        default=None, description="Уровень опыта пользователя"
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="Ответ чат-бота")
    suggested_vacancies: Optional[List[int]] = Field(
        default=None, description="ID рекомендованных вакансий"
    )
    skill_recommendations: Optional[List[str]] = Field(
        default=None, description="Рекомендации по навыкам для улучшения"
    )

