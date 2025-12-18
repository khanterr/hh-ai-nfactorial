import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db, Base
from models import Company, Job

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_company():
    response = client.post(
        "/api/v1/companies",
        json={
            "name": "Test Company",
            "description": "A test company for API testing",
            "location": "Test City, TC"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Company"
    assert data["description"] == "A test company for API testing"
    company_id = data["id"]
    
    # Test getting the created company
    response = client.get(f"/api/v1/companies/{company_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Company"


def test_create_job():
    # First create a company to associate with the job
    response = client.post(
        "/api/v1/companies",
        json={
            "name": "Test Job Company",
            "description": "A test company for job testing",
            "location": "Test City, TC"
        }
    )
    assert response.status_code == 200
    company_data = response.json()
    company_id = company_data["id"]
    
    # Now create a job associated with this company
    response = client.post(
        "/api/v1/jobs",
        json={
            "title": "Software Engineer",
            "description": "Test job description",
            "requirements": "Test requirements",
            "benefits": "Test benefits",
            "city": "Test City",
            "grade": "Mid",
            "format": "Hybrid",
            "company_id": company_id
        }
    )
    assert response.status_code == 200
    job_data = response.json()
    assert job_data["title"] == "Software Engineer"
    assert job_data["company"]["id"] == company_id


def test_get_jobs_with_filters():
    # Create a few jobs for testing filters
    # Create a company first
    response = client.post(
        "/api/v1/companies",
        json={
            "name": "Filter Test Company",
            "description": "Company for filter testing",
            "location": "Test City, TC"
        }
    )
    assert response.status_code == 200
    company_data = response.json()
    company_id = company_data["id"]
    
    # Create jobs with different attributes
    client.post(
        "/api/v1/jobs",
        json={
            "title": "Remote Junior Developer",
            "description": "Remote job for junior developers",
            "city": "Remote",
            "grade": "Junior",
            "format": "Remote",
            "company_id": company_id
        }
    )
    
    client.post(
        "/api/v1/jobs",
        json={
            "title": "On-site Senior Developer",
            "description": "On-site job for senior developers",
            "city": "New York",
            "grade": "Senior",
            "format": "On-site",
            "company_id": company_id
        }
    )
    
    # Test filtering by city
    response = client.get("/api/v1/jobs?city=Remote")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    for job in data:
        assert job["city"] == "Remote"
    
    # Test filtering by grade
    response = client.get("/api/v1/jobs?grade=Senior")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    for job in data:
        assert job["grade"] == "Senior"
    
    # Test filtering by format
    response = client.get("/api/v1/jobs?format=Remote")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    for job in data:
        assert job["format"] == "Remote"