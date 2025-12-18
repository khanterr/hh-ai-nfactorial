import os
from typing import List, Optional, Dict, Any
from openai import OpenAI
from models import ChatMessage, Vacancy, ChatRequest, ChatResponse
import json


class ChatBotService:
    def __init__(self, api_key: Optional[str] = None):
        """
        Инициализация сервиса чат-бота с OpenAI
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY не установлен. Установите переменную окружения или передайте api_key")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4-turbo-preview"  # Можно использовать gpt-3.5-turbo для экономии
        
    def _build_system_prompt(self, vacancies_data: Optional[List[Dict]] = None) -> str:
        """
        Создает системный промпт для чат-бота
        """
        base_prompt = """Ты - полезный AI-ассистент для веб-сайта с вакансиями и компаниями. 
Твоя задача:
1. Помогать пользователям подобрать подходящие вакансии на основе их навыков, опыта и предпочтений
2. Отвечать на вопросы о вакансиях, компаниях, требованиях и условиях работы
3. Давать рекомендации по навыкам, которые стоит подтянуть для конкретных вакансий

Будь дружелюбным, профессиональным и полезным. Если пользователь спрашивает о вакансиях, 
используй информацию о доступных вакансиях для точных рекомендаций.

Отвечай на русском языке, если пользователь пишет на русском."""
        
        if vacancies_data:
            vacancies_info = "\n\nДоступные вакансии:\n"
            for vac in vacancies_data[:10]:  # Ограничиваем для промпта
                vacancies_info += f"- ID {vac.get('id')}: {vac.get('title')} в {vac.get('company_name', 'N/A')}. "
                vacancies_info += f"Навыки: {', '.join(vac.get('required_skills', []))}. "
                vacancies_info += f"Уровень: {vac.get('experience_level', 'N/A')}\n"
            base_prompt += vacancies_info
        
        return base_prompt
    
    def _prepare_messages(
        self, 
        user_message: str, 
        conversation_history: List[ChatMessage],
        vacancies_data: Optional[List[Dict]] = None,
        user_skills: Optional[List[str]] = None,
        user_experience: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Подготавливает сообщения для отправки в OpenAI API
        """
        messages = [
            {"role": "system", "content": self._build_system_prompt(vacancies_data)}
        ]
        
        # Добавляем контекст о пользователе, если есть
        if user_skills or user_experience:
            user_context = "Информация о пользователе:\n"
            if user_skills:
                user_context += f"Навыки: {', '.join(user_skills)}\n"
            if user_experience:
                user_context += f"Уровень опыта: {user_experience}\n"
            messages.append({"role": "system", "content": user_context})
        
        # Добавляем историю разговора
        for msg in conversation_history[-10:]:  # Ограничиваем историю последними 10 сообщениями
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Добавляем текущее сообщение пользователя
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _extract_vacancy_ids(self, response_text: str) -> Optional[List[int]]:
        """
        Пытается извлечь ID вакансий из ответа (если бот их упомянул)
        """
        # Простая эвристика - можно улучшить с помощью regex или структурированного вывода
        import re
        ids = re.findall(r'ваканси[яи]\s*(?:№|#)?\s*(\d+)', response_text, re.IGNORECASE)
        if ids:
            return [int(id) for id in ids]
        return None
    
    def _extract_skill_recommendations(self, response_text: str) -> Optional[List[str]]:
        """
        Пытается извлечь рекомендации по навыкам из ответа
        """
        # Можно улучшить с помощью структурированного вывода OpenAI
        skills = []
        skill_keywords = ["изучить", "подтянуть", "освоить", "навык", "технология"]
        
        lines = response_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in skill_keywords):
                # Простая эвристика - можно улучшить
                words = line.split()
                for i, word in enumerate(words):
                    if word.lower() in skill_keywords and i + 1 < len(words):
                        potential_skill = words[i + 1].strip('.,!?;:')
                        if len(potential_skill) > 2:
                            skills.append(potential_skill)
        
        return skills[:5] if skills else None
    
    async def get_chat_response(
        self,
        request: ChatRequest,
        vacancies_data: Optional[List[Dict]] = None
    ) -> ChatResponse:
        """
        Получает ответ от чат-бота на основе запроса пользователя
        """
        try:
            messages = self._prepare_messages(
                user_message=request.message,
                conversation_history=request.conversation_history or [],
                vacancies_data=vacancies_data,
                user_skills=request.user_skills,
                user_experience=request.user_experience
            )
            
            # Вызов OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content
            
            # Извлекаем дополнительную информацию из ответа
            suggested_vacancies = self._extract_vacancy_ids(response_text)
            skill_recommendations = self._extract_skill_recommendations(response_text)
            
            return ChatResponse(
                response=response_text,
                suggested_vacancies=suggested_vacancies,
                skill_recommendations=skill_recommendations
            )
            
        except Exception as e:
            error_message = f"Произошла ошибка при обработке запроса: {str(e)}"
            return ChatResponse(response=error_message)
    
    def get_structured_recommendations(
        self,
        user_skills: List[str],
        user_experience: Optional[str],
        vacancies_data: List[Dict]
    ) -> Dict[str, Any]:
        """
        Получает структурированные рекомендации по вакансиям и навыкам
        """
        # Создаем промпт для структурированного анализа
        skills_str = ", ".join(user_skills) if user_skills else "не указаны"
        experience_str = user_experience or "не указан"
        
        vacancies_summary = "\n".join([
            f"ID {v['id']}: {v['title']} - Навыки: {', '.join(v.get('required_skills', []))}"
            for v in vacancies_data[:20]
        ])
        
        prompt = f"""Проанализируй следующие данные и дай структурированные рекомендации:

Навыки пользователя: {skills_str}
Уровень опыта: {experience_str}

Доступные вакансии:
{vacancies_summary}

Верни JSON с:
1. Список ID подходящих вакансий (top 5)
2. Рекомендации по навыкам для улучшения (top 3-5)

Формат:
{{
    "recommended_vacancy_ids": [1, 2, 3],
    "skill_recommendations": ["Python", "Docker", "Kubernetes"]
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты помощник по подбору вакансий. Отвечай только валидным JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {
                "recommended_vacancy_ids": [],
                "skill_recommendations": [],
                "error": str(e)
            }

