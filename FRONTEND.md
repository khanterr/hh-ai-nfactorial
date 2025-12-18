# Job Search Platform

This is a comprehensive job search platform with both backend (FastAPI) and frontend (React) components.

## Frontend Overview

The frontend is a modern React application that provides:

- **Job Listings Page**: Browse all available jobs with filtering by city, grade, and format
- **Job Detail Page**: Detailed view of individual job postings
- **Company Information Page**: View company details and their open positions
- **Responsive Design**: Fully responsive layout that works on all device sizes
- **Modern UI**: Clean, professional design with Tailwind CSS
- **State Management**: Context API for managing application state
- **API Integration**: Seamless integration with the backend API
- **End-to-End Tests**: Comprehensive Playwright test suite

## Frontend Architecture

### Technology Stack
- **React 18**: Modern component-based UI framework
- **React Router**: Client-side navigation
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication
- **Heroicons**: Beautiful SVG icon library
- **Playwright**: End-to-end testing framework

### Project Structure
```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── Header.js       # Navigation header
│   │   ├── Footer.js       # Page footer
│   │   ├── JobCard.js      # Job listing card component
│   │   ├── FilterSidebar.js # Filtering component
│   │   ├── MobileMenu.js   # Mobile navigation
│   │   ├── LoadingSpinner.js # Loading indicator
│   │   └── ...             # Other components
│   ├── pages/              # Page components
│   │   ├── HomePage.js     # Landing page
│   │   ├── JobListingsPage.js # Job listings with filters
│   │   ├── JobDetailPage.js # Job detail view
│   │   └── CompanyInfoPage.js # Company information
│   ├── utils/
│   │   └── api.js          # API service configuration
│   ├── contexts/
│   │   └── JobContext.js   # Global state management
│   ├── styles/
│   │   ├── index.css       # Tailwind imports and custom styles
│   │   └── App.css         # App-specific styles
│   ├── App.js              # Main application component
│   └── index.js            # Application entry point
├── package.json            # Dependencies and scripts
├── tailwind.config.js      # Tailwind CSS configuration
└── README.md               # Frontend documentation
```

### Key Features Implemented

1. **Job Listings with Advanced Filtering**
   - Filter by city, experience level (Junior, Mid, Senior, Lead), and work format (Remote, On-site, Hybrid)
   - Search functionality across job titles, descriptions, and company names
   - Responsive card layout with hover effects

2. **Detailed Job Views**
   - Comprehensive job information display
   - Company information integration
   - Salary range formatting
   - Requirements and benefits sections

3. **Company Information Pages**
   - Detailed company profiles
   - Company's open positions display
   - Logo and description presentation

4. **Responsive Design**
   - Mobile-first approach
   - Adaptive layouts for all screen sizes
   - Touch-friendly interface elements
   - Collapsible mobile navigation

5. **State Management**
   - Context API for global state
   - Loading and error states
   - Data caching and retrieval

6. **API Integration**
   - Axios for HTTP requests
   - Request/response interceptors
   - Error handling
   - Loading states

7. **Testing**
   - Comprehensive Playwright test suite
   - Mock API responses for consistent testing
   - Cross-browser compatibility
   - Mobile viewport testing

## Getting Started with Frontend

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`.

## API Integration

The frontend connects to the backend API at `http://localhost:8000/api/v1` and uses the following endpoints:

- `GET /api/v1/jobs` - Retrieve job listings (with optional filters)
- `GET /api/v1/jobs/{id}` - Get specific job details
- `GET /api/v1/companies` - Get company listings
- `GET /api/v1/companies/{id}` - Get specific company details

## Testing

### Unit Tests
Run React component tests:
```bash
npm test
```

### End-to-End Tests
First install Playwright browsers:
```bash
npm run install-playwright
```

Then run E2E tests:
```bash
npm run test-e2e
```

## Deployment

To build the application for production:
```bash
npm run build
```

This creates an optimized build in the `build` directory.

## Development Best Practices

- Component reusability and modularity
- Proper state management with Context API
- Responsive design with Tailwind CSS
- Accessibility considerations
- Performance optimization
- Error handling and loading states
- Consistent code formatting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request