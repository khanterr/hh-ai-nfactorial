# Job Search Platform (LinkedIn / HH mini)

A comprehensive job search platform with AI-powered features, built as a team project.

## Team Structure

This project is organized by roles:

- 🎨 **Frontend Developer** - User interface and client-side development
- ⚙️ **Backend Developer** - API and server-side logic
- 🧠 **AI Engineer** - Machine learning models and intelligent features
- 🧪 **QA Engineer & Workflow Master** - Testing, quality assurance, and CI/CD

## Features

- Job listings with detailed information
- Company profiles with descriptions
- Advanced filtering by city, grade, and format
- AI-powered job recommendations
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
├── frontend/               # 🎨 Frontend Developer workspace
│   └── README.md          # Frontend setup and guidelines
├── backend/                # ⚙️ Backend Developer workspace
│   └── README.md          # Backend setup and guidelines
├── ai-engineer/            # 🧠 AI Engineer workspace
│   └── README.md          # AI/ML setup and guidelines
├── qa-workflow/            # 🧪 QA Engineer & Workflow Master workspace
│   └── README.md          # QA and workflow documentation
├── main.py                 # Main application entry point
├── database.py             # Database setup and session management
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas for request/response validation
├── crud.py                 # Database operations
├── init_db.py              # Script to initialize database with sample data
└── requirements.txt        # Project dependencies
```

## Getting Started

Each team member should work in their designated directory:
- Frontend developers: See [frontend/README.md](frontend/README.md)
- Backend developers: See [backend/README.md](backend/README.md)
- AI engineers: See [ai-engineer/README.md](ai-engineer/README.md)
- QA engineers: See [qa-workflow/README.md](qa-workflow/README.md)
