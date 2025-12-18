from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def init_db():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if we already have data
        existing_companies = db.query(models.Company).count()
        if existing_companies > 0:
            print("Database already has data. Skipping initialization.")
            return
        
        # Create sample companies
        tech_company = models.Company(
            name="Tech Innovations Inc.",
            description="A leading technology company focused on developing cutting-edge software solutions.",
            logo_url="https://example.com/tech-logo.png",
            website="https://techinnovations.example.com",
            location="San Francisco, CA"
        )
        
        startup_company = models.Company(
            name="Startup Solutions",
            description="An innovative startup creating solutions for modern business challenges.",
            logo_url="https://example.com/startup-logo.png",
            website="https://startupsolutions.example.com",
            location="New York, NY"
        )
        
        enterprise_company = models.Company(
            name="Enterprise Systems Ltd.",
            description="Providing enterprise-level solutions for large organizations.",
            logo_url="https://example.com/enterprise-logo.png",
            website="https://enterprisesystems.example.com",
            location="Chicago, IL"
        )
        
        db.add_all([tech_company, startup_company, enterprise_company])
        db.commit()
        
        # Refresh objects to get IDs
        db.refresh(tech_company)
        db.refresh(startup_company)
        db.refresh(enterprise_company)
        
        # Create sample jobs
        jobs_data = [
            # Tech Innovations jobs
            {
                "title": "Junior Software Engineer",
                "description": "We are looking for a junior software engineer to join our development team.",
                "requirements": "Bachelor's degree in Computer Science, 1-2 years experience with Python",
                "benefits": "Health insurance, remote work options, professional development budget",
                "city": "San Francisco",
                "grade": "Junior",
                "format": "Hybrid",
                "salary_min": 70000,
                "salary_max": 90000,
                "company_id": tech_company.id
            },
            {
                "title": "Senior Frontend Developer",
                "description": "Seeking an experienced frontend developer to lead our UI/UX initiatives.",
                "requirements": "5+ years experience with React, strong CSS skills",
                "benefits": "Stock options, flexible hours, unlimited PTO",
                "city": "San Francisco",
                "grade": "Senior",
                "format": "Hybrid",
                "salary_min": 120000,
                "salary_max": 150000,
                "company_id": tech_company.id
            },
            {
                "title": "DevOps Engineer",
                "description": "Responsible for managing our cloud infrastructure and deployment pipelines.",
                "requirements": "Experience with AWS, Docker, Kubernetes",
                "benefits": "Comprehensive health coverage, home office stipend",
                "city": "Remote",
                "grade": "Mid",
                "format": "Remote",
                "salary_min": 100000,
                "salary_max": 130000,
                "company_id": tech_company.id
            },
            
            # Startup Solutions jobs
            {
                "title": "Product Manager",
                "description": "Lead product development from conception to launch.",
                "requirements": "3+ years product management experience, technical background preferred",
                "benefits": "Equity package, casual work environment, learning budget",
                "city": "New York",
                "grade": "Mid",
                "format": "On-site",
                "salary_min": 95000,
                "salary_max": 125000,
                "company_id": startup_company.id
            },
            {
                "title": "Data Scientist",
                "description": "Analyze complex datasets to drive business insights and product improvements.",
                "requirements": "Master's degree in Data Science or related field, Python/R proficiency",
                "benefits": "Flexible schedule, conference attendance allowance",
                "city": "Remote",
                "grade": "Mid",
                "format": "Remote",
                "salary_min": 110000,
                "salary_max": 140000,
                "company_id": startup_company.id
            },
            
            # Enterprise Systems jobs
            {
                "title": "Lead Software Architect",
                "description": "Design and oversee the implementation of enterprise-scale software solutions.",
                "requirements": "10+ years software development experience, architectural design skills",
                "benefits": "Premium health plan, executive bonus program, sabbatical leave",
                "city": "Chicago",
                "grade": "Lead",
                "format": "On-site",
                "salary_min": 160000,
                "salary_max": 200000,
                "company_id": enterprise_company.id
            },
            {
                "title": "QA Engineer",
                "description": "Ensure software quality through comprehensive testing strategies.",
                "requirements": "2+ years QA experience, automation testing skills",
                "benefits": "Health and dental insurance, gym membership, professional development",
                "city": "Chicago",
                "grade": "Mid",
                "format": "Hybrid",
                "salary_min": 85000,
                "salary_max": 110000,
                "company_id": enterprise_company.id
            }
        ]
        
        jobs = [models.Job(**job_data) for job_data in jobs_data]
        db.add_all(jobs)
        db.commit()
        
        print("Database initialized with sample data successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()