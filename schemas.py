from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Company Schemas
class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Job Schemas
class JobBase(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    city: str
    grade: str
    format: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    company_id: int
    is_active: bool = True


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    city: Optional[str] = None
    grade: Optional[str] = None
    format: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    company_id: Optional[int] = None
    is_active: Optional[bool] = None


class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime
    company: Company

    class Config:
        orm_mode = True


# Job Query Parameters Schema
class JobFilterParams(BaseModel):
    city: Optional[str] = None
    grade: Optional[str] = None
    format: Optional[str] = None
    company_id: Optional[int] = None
    is_active: Optional[bool] = True