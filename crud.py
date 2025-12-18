from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Job, Company
from schemas import JobCreate, JobUpdate, CompanyCreate, CompanyUpdate


# CRUD operations for Companies
def get_company(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()


def create_company(db: Session, company: CompanyCreate):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def update_company(db: Session, company_id: int, company: CompanyUpdate):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company:
        for key, value in company.dict(exclude_unset=True).items():
            setattr(db_company, key, value)
        db.commit()
        db.refresh(db_company)
    return db_company


def delete_company(db: Session, company_id: int):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company:
        db.delete(db_company)
        db.commit()
    return db_company


# CRUD operations for Jobs
def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def get_jobs(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    city: str = None, 
    grade: str = None, 
    format: str = None,
    company_id: int = None,
    is_active: bool = True
):
    query = db.query(Job).join(Job.company)
    
    filters = []
    if city:
        filters.append(Job.city == city)
    if grade:
        filters.append(Job.grade == grade)
    if format:
        filters.append(Job.format == format)
    if company_id:
        filters.append(Job.company_id == company_id)
    if is_active is not None:
        filters.append(Job.is_active == is_active)
    
    if filters:
        query = query.filter(and_(*filters))
    
    return query.offset(skip).limit(limit).all()


def create_job(db: Session, job: JobCreate):
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(db: Session, job_id: int, job: JobUpdate):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job:
        for key, value in job.dict(exclude_unset=True).items():
            setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job:
        db.delete(db_job)
        db.commit()
    return db_job