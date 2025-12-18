# 🎨 Frontend Developer

This directory contains the frontend application for the Job Search Platform, built with a LinkedIn-inspired design.

## Tech Stack

- HTML5, CSS3, Vanilla JavaScript
- Responsive design with CSS Grid and Flexbox
- RESTful API integration
- Modern ES6+ JavaScript

## Design Inspiration

The frontend is designed based on LinkedIn's professional aesthetic:
- Clean, card-based layout
- Blue color scheme (#0a66c2 primary)
- Professional typography
- Responsive design for mobile, tablet, and desktop

## Project Structure

```
frontend/
├── index.html          # Main jobs listing page
├── styles.css          # All styles with LinkedIn-inspired design
├── app.js             # JavaScript for API integration and interactivity
└── README.md          # This file
```

## Features

- **Job Listings**: Card-based layout with job details
- **Real-time Filtering**: Filter by city, grade, and format
- **Search**: Search across job titles, companies, and descriptions
- **Responsive Design**: Works on all screen sizes
- **API Integration**: Connects to FastAPI backend

## Getting Started

### Prerequisites

Make sure the backend server is running:
```bash
cd ..
uvicorn main:app --reload
```

### Running the Frontend

1. Open `index.html` in your browser, or use a local server:

```bash
# Using Python
python -m http.server 8080

# Using Node.js (if you have http-server installed)
npx http-server -p 8080
```

2. Navigate to `http://localhost:8080` in your browser

### API Configuration

The frontend connects to the backend API at `http://localhost:8000/api/v1`

If your backend runs on a different port, update the `API_BASE_URL` in `app.js`:
```javascript
const API_BASE_URL = 'http://localhost:YOUR_PORT/api/v1';
```

## Key Components

### Navigation Bar
- Logo and branding
- Search functionality
- Quick links to Jobs, Companies, Profile
- Sign In button

### Filters Sidebar
- City filter dropdown
- Experience level (Grade) filter
- Work format filter
- Clear filters button

### Job Cards
Each job card displays:
- Company logo (initial letter)
- Job title
- Company name
- Location, grade, format, salary
- Job description (truncated)
- Tags
- Posted date
- Save and Apply buttons

## Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-blue: #0a66c2;
    --primary-blue-hover: #004182;
    /* ... other colors */
}
```

### Layout
The main layout uses CSS Grid. Adjust breakpoints in the media queries at the bottom of `styles.css`.

## Future Enhancements

- [ ] User authentication UI
- [ ] Job detail page
- [ ] Company profile pages
- [ ] User profile and resume upload
- [ ] Saved jobs page
- [ ] Application tracking
- [ ] Advanced search with autocomplete
- [ ] Infinite scroll or pagination

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
