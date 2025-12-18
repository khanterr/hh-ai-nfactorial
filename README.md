# Job Search Platform Backend

A comprehensive backend API for a job search platform built with FastAPI and SQLite.

## Features

- Job listings with detailed information
- Company profiles with descriptions
- Advanced filtering by city, grade, and format
- RESTful API endpoints
- Proper data validation with Pydantic
- SQLite database with SQLAlchemy ORM

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database with sample data:
```bash
python init_db.py
```

3. Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

After starting the server, you can access:
- Interactive API docs at `http://localhost:8000/docs`
- Alternative API docs at `http://localhost:8000/redoc`

## API Endpoints

### Jobs
- `GET /api/v1/jobs` - Get all jobs with optional filtering
- `GET /api/v1/jobs/{id}` - Get a specific job
- `POST /api/v1/jobs` - Create a new job
- `PUT /api/v1/jobs/{id}` - Update a job
- `DELETE /api/v1/jobs/{id}` - Delete a job

### Companies
- `GET /api/v1/companies` - Get all companies
- `GET /api/v1/companies/{id}` - Get a specific company
- `POST /api/v1/companies` - Create a new company
- `PUT /api/v1/companies/{id}` - Update a company
- `DELETE /api/v1/companies/{id}` - Delete a company

## Filtering Options

Jobs can be filtered by:
- City: `?city=San%20Francisco`
- Grade: `?grade=Senior`
- Format: `?format=Remote`
- Multiple filters: `?city=Remote&grade=Mid&format=Remote`

## Project Structure

```
├── main.py                 # Main application entry point
├── database.py             # Database setup and session management
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas for request/response validation
├── crud.py                 # Database operations
├── routers/                # API route definitions
│   ├── jobs.py
│   └── companies.py
├── init_db.py              # Script to initialize database with sample data
└── requirements.txt        # Project dependencies
```
