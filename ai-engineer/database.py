"""
Модуль для работы с данными о вакансиях и компаниях.
В реальном проекте здесь будет подключение к БД.
Сейчас используем мок-данные для демонстрации.
"""
from typing import List, Dict, Optional
from models import Vacancy, Company, JobType, ExperienceLevel
from datetime import datetime


# Мок-данные компаний
MOCK_COMPANIES = [
    Company(
        id=1,
        name="TechCorp",
        description="Ведущая IT-компания в области разработки ПО",
        industry="IT",
        website="https://techcorp.com",
        location="Москва"
    ),
    Company(
        id=2,
        name="DataSoft",
        description="Специализация на больших данных и машинном обучении",
        industry="IT",
        website="https://datasoft.ru",
        location="Санкт-Петербург"
    ),
    Company(
        id=3,
        name="WebDev Studio",
        description="Веб-разработка и дизайн",
        industry="IT",
        website="https://webdev.studio",
        location="Казань"
    ),
]


# Мок-данные вакансий
MOCK_VACANCIES = [
    Vacancy(
        id=1,
        title="Python Backend Developer",
        description="Разработка backend-приложений на Python, работа с Django/FastAPI",
        company_id=1,
        location="Москва",
        salary_min=150000,
        salary_max=250000,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MIDDLE,
        required_skills=["Python", "Django", "PostgreSQL", "REST API"],
        preferred_skills=["Docker", "Kubernetes", "Redis"],
        posted_date=datetime(2024, 1, 15)
    ),
    Vacancy(
        id=2,
        title="Frontend Developer (React)",
        description="Разработка пользовательских интерфейсов на React",
        company_id=3,
        location="Казань",
        salary_min=120000,
        salary_max=200000,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MIDDLE,
        required_skills=["React", "TypeScript", "JavaScript", "CSS"],
        preferred_skills=["Redux", "Next.js", "Webpack"],
        posted_date=datetime(2024, 1, 20)
    ),
    Vacancy(
        id=3,
        title="Data Scientist",
        description="Разработка ML-моделей и анализ данных",
        company_id=2,
        location="Санкт-Петербург",
        salary_min=200000,
        salary_max=350000,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.SENIOR,
        required_skills=["Python", "Machine Learning", "Pandas", "NumPy", "Scikit-learn"],
        preferred_skills=["TensorFlow", "PyTorch", "SQL"],
        posted_date=datetime(2024, 1, 18)
    ),
    Vacancy(
        id=4,
        title="Junior Python Developer",
        description="Стажировка для начинающих разработчиков",
        company_id=1,
        location="Москва",
        salary_min=80000,
        salary_max=120000,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.JUNIOR,
        required_skills=["Python", "Git"],
        preferred_skills=["Django", "SQL"],
        posted_date=datetime(2024, 1, 22)
    ),
    Vacancy(
        id=5,
        title="Full Stack Developer",
        description="Разработка полного цикла: frontend и backend",
        company_id=3,
        location="Казань",
        salary_min=180000,
        salary_max=280000,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MIDDLE,
        required_skills=["Python", "React", "PostgreSQL", "REST API"],
        preferred_skills=["Docker", "AWS", "TypeScript"],
        posted_date=datetime(2024, 1, 19)
    ),
]


class Database:
    """
    Класс для работы с данными о вакансиях и компаниях.
    В реальном проекте здесь будет подключение к БД (PostgreSQL, MongoDB и т.д.)
    """
    
    def __init__(self):
        self.companies = {c.id: c for c in MOCK_COMPANIES}
        self.vacancies = {}
        for vac in MOCK_VACANCIES:
            vac.company = self.companies.get(vac.company_id)
            self.vacancies[vac.id] = vac
    
    def get_all_vacancies(self) -> List[Vacancy]:
        """Получить все вакансии"""
        return list(self.vacancies.values())
    
    def get_vacancy_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        """Получить вакансию по ID"""
        return self.vacancies.get(vacancy_id)
    
    def get_vacancies_by_skills(self, skills: List[str]) -> List[Vacancy]:
        """Получить вакансии, требующие указанные навыки"""
        matching = []
        skills_lower = [s.lower() for s in skills]
        
        for vacancy in self.vacancies.values():
            vacancy_skills = [s.lower() for s in vacancy.required_skills + vacancy.preferred_skills]
            if any(skill in vacancy_skills for skill in skills_lower):
                matching.append(vacancy)
        
        return matching
    
    def get_vacancies_data_for_chat(self) -> List[Dict]:
        """
        Получить данные о вакансиях в формате для чат-бота
        """
        result = []
        for vac in self.vacancies.values():
            result.append({
                "id": vac.id,
                "title": vac.title,
                "description": vac.description,
                "company_name": vac.company.name if vac.company else "N/A",
                "location": vac.location,
                "salary_min": vac.salary_min,
                "salary_max": vac.salary_max,
                "job_type": vac.job_type.value if vac.job_type else None,
                "experience_level": vac.experience_level.value if vac.experience_level else None,
                "required_skills": vac.required_skills,
                "preferred_skills": vac.preferred_skills,
            })
        return result
    
    def get_company_by_id(self, company_id: int) -> Optional[Company]:
        """Получить компанию по ID"""
        return self.companies.get(company_id)
    
    def get_all_companies(self) -> List[Company]:
        """Получить все компании"""
        return list(self.companies.values())


# Глобальный экземпляр БД
db = Database()

