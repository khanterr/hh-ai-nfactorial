# Frontend Demo Guide

## Quick Start Guide

### Step 1: Start the Backend Server

Open a terminal in the project root directory and run:

```bash
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Initialize the database with sample data
python init_db.py

# Start the FastAPI server
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Step 2: Start the Frontend

Option A - Using Python's built-in server:
```bash
cd frontend
python -m http.server 8080
```

Option B - Just open the file directly:
```bash
# Open in your default browser
start index.html  # Windows
open index.html   # macOS
xdg-open index.html  # Linux
```

Option C - Using VS Code Live Server:
- Right-click on `index.html`
- Select "Open with Live Server"

### Step 3: Access the Application

Navigate to `http://localhost:8080` (or the file path if opened directly)

## Features to Try

### 1. Browse Jobs
- Scroll through the job listings
- Each card shows company, location, salary, and description

### 2. Filter Jobs
Use the sidebar filters:
- **City**: Filter by Almaty, Astana, Shymkent, or Remote
- **Experience Level**: Junior, Mid, Senior, Lead
- **Work Format**: Remote, Office, Hybrid

### 3. Search
- Type in the search box at the top
- Search works across job titles, company names, and descriptions
- Results update in real-time

### 4. Clear Filters
- Click "Clear Filters" button to reset all filters

### 5. Interact with Job Cards
- Click on a job card to view details (currently shows alert)
- Click "Save" bookmark icon to save a job (demo)
- Click "Apply" button to start application (demo)

## Design Features

### LinkedIn-Inspired Design
- Professional blue color scheme
- Clean, card-based layout
- Sticky navigation bar
- Responsive sidebar

### Responsive Design
- **Desktop**: Full layout with sidebar
- **Tablet**: Collapsible sidebar
- **Mobile**: Stacked layout, simplified navigation

Test responsiveness by resizing your browser window!

## API Integration

The frontend connects to these backend endpoints:

- `GET /api/v1/jobs` - Fetch all jobs
- `GET /api/v1/companies` - Fetch all companies

### Testing API Connection

Open browser console (F12) to see:
- API requests being made
- Data being loaded
- Any errors

## Troubleshooting

### Jobs Not Loading?

1. Check if backend is running:
   ```bash
   curl http://localhost:8000/api/v1/jobs
   ```

2. Check browser console for errors (F12)

3. Make sure database is initialized:
   ```bash
   python init_db.py
   ```

### CORS Errors?

If you see CORS errors, make sure the backend has CORS enabled. The backend should have:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Styling Issues?

1. Hard refresh the page: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)
2. Check that `styles.css` is in the same directory as `index.html`

## Screenshots Expected View

### Desktop View
- Navigation bar at top
- Filters sidebar on left (260px wide)
- Job cards grid on right
- Footer at bottom

### Mobile View
- Stacked layout
- Full-width search
- Filters above job listings
- Simplified navigation icons

## Next Steps

This is a demo version. In a production app, you would add:

- User authentication
- Detailed job pages
- Application submission
- User profiles
- Resume upload
- Saved jobs page
- Application tracking
- Email notifications
- Advanced search with autocomplete
- Pagination or infinite scroll
