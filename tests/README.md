# Playwright Tests for AI Chat Bot

This directory contains end-to-end tests for the AI Chat Bot application using Playwright.

## Prerequisites

Before running the tests, make sure you have:

1. Node.js (v14 or higher)
2. The backend server running on `http://localhost:8000`

## Installation

1. Install dependencies:
```bash
npm install
```

2. Install Playwright browsers:
```bash
npx playwright install
```

Or to install a specific browser:
```bash
npx playwright install chromium
```

## Running Tests

### Run all tests:
```bash
npm run test:e2e
```

### Run tests in UI mode:
```bash
npm run test:e2e:ui
```

### Run tests in debug mode:
```bash
npm run test:e2e:debug
```

### Run tests on a specific browser:
```bash
npm run test:e2e -- --project=chromium
```

## Test Structure

The tests are organized in two main files:

### `chatbot.spec.ts`
Tests the frontend UI components of the chatbot application, including:
- Displaying initial bot message
- Sending messages via input field and Enter key
- Updating configuration settings (API URL, skills, experience)
- Handling loading states
- Error handling when API is unavailable
- Displaying additional recommendations
- Maintaining conversation history

### `api-e2e.spec.ts`
Tests the backend API endpoints directly, including:
- Root endpoint (`/`)
- Chat endpoint (`/api/chat`)
- Vacancies endpoint (`/api/vacancies`)
- Company endpoints (`/api/companies`)
- Health check endpoint (`/api/health`)
- Recommendations endpoint (`/api/recommendations`)
- Error handling

## Running with Backend Server

The Playwright configuration is set up to automatically start the backend server using:
```bash
cd ai-engineer && python main.py
```

Make sure you have Python and the required dependencies installed:

```bash
pip install -r ai-engineer/requirements.txt
```

## Environment Variables

If needed, you can create a `.env` file in the project root to configure your test environment:

```env
BASE_URL=http://localhost:8000
API_TIMEOUT=30000
```

## Test Reports

After running tests, you can view the HTML report:

```bash
npm run report:open
```

## Troubleshooting

### API Key Issues
If tests fail because of missing OpenAI API key:
1. Create a `.env` file in the `ai-engineer` directory
2. Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`

### Backend Not Starting
If the backend server doesn't start automatically:
1. Manually start it: `cd ai-engineer && python main.py`
2. Or using uvicorn: `cd ai-engineer && uvicorn main:app --reload --host 0.0.0.0 --port 8000`

### File Path Issues
If you encounter file path issues, make sure the test frontend HTML file is accessible at:
`/Users/kuka/Documents/Nfactorial/project3/hh-ai-nfactorial/ai-engineer/test_frontend.html`