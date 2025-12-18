import { test, expect } from '@playwright/test';

// Using the backend API directly instead of the HTML file
test.describe('AI Chat Bot API End-to-End Tests', () => {
  const baseUrl = 'http://localhost:8000';

  test('should return welcome message at root endpoint', async ({ request }) => {
    const response = await request.get(`${baseUrl}/`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data.message).toBe('AI Chat Bot API для вакансий');
    expect(data.version).toBe('1.0.0');
  });

  test('should handle chat endpoint properly', async ({ request }) => {
    const response = await request.post(`${baseUrl}/api/chat`, {
      data: {
        message: 'Привет, помоги найти вакансии по Python разработке',
        user_skills: ['Python', 'Django'],
        user_experience: 'middle'
      }
    });
    
    expect(response.status()).toBe(200);
    const data = await response.json();
    
    expect(data).toHaveProperty('response');
    expect(typeof data.response).toBe('string');
    
    // Depending on the API key availability, these may or may not be present
    if (data.suggested_vacancies) {
      expect(Array.isArray(data.suggested_vacancies)).toBeTruthy();
    }
    
    if (data.skill_recommendations) {
      expect(Array.isArray(data.skill_recommendations)).toBeTruthy();
    }
  });

  test('should return all vacancies', async ({ request }) => {
    const response = await request.get(`${baseUrl}/api/vacancies`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(Array.isArray(data)).toBeTruthy();
    expect(data.length).toBeGreaterThan(0);
    
    // Check structure of first vacancy
    const firstVacancy = data[0];
    expect(firstVacancy).toHaveProperty('id');
    expect(firstVacancy).toHaveProperty('title');
    expect(firstVacancy).toHaveProperty('description');
    expect(firstVacancy).toHaveProperty('company_id');
  });

  test('should filter vacancies by skills', async ({ request }) => {
    const response = await request.get(`${baseUrl}/api/vacancies?skills=Python`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(Array.isArray(data)).toBeTruthy();
    
    // Verify that returned vacancies have Python in their skills
    if (data.length > 0) {
      const firstVacancy = data[0];
      const allSkills = [...firstVacancy.required_skills, ...firstVacancy.preferred_skills];
      const hasPythonSkill = allSkills.some((skill: string) => 
        skill.toLowerCase().includes('python')
      );
      expect(hasPythonSkill).toBeTruthy();
    }
  });

  test('should return all companies', async ({ request }) => {
    const response = await request.get(`${baseUrl}/api/companies`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(Array.isArray(data)).toBeTruthy();
    expect(data.length).toBeGreaterThan(0);
    
    // Check structure of first company
    const firstCompany = data[0];
    expect(firstCompany).toHaveProperty('id');
    expect(firstCompany).toHaveProperty('name');
    expect(firstCompany).toHaveProperty('description');
  });

  test('should return specific company by ID', async ({ request }) => {
    // First get all companies to pick an ID
    const companiesResponse = await request.get(`${baseUrl}/api/companies`);
    expect(companiesResponse.status()).toBe(200);
    
    const companies = await companiesResponse.json();
    expect(companies.length).toBeGreaterThan(0);
    
    const companyId = companies[0].id;
    const response = await request.get(`${baseUrl}/api/companies/${companyId}`);
    expect(response.status()).toBe(200);
    
    const company = await response.json();
    expect(company.id).toBe(companyId);
  });

  test('should return specific vacancy by ID', async ({ request }) => {
    // First get all vacancies to pick an ID
    const vacanciesResponse = await request.get(`${baseUrl}/api/vacancies`);
    expect(vacanciesResponse.status()).toBe(200);
    
    const vacancies = await vacanciesResponse.json();
    expect(vacancies.length).toBeGreaterThan(0);
    
    const vacancyId = vacancies[0].id;
    const response = await request.get(`${baseUrl}/api/vacancies/${vacancyId}`);
    expect(response.status()).toBe(200);
    
    const vacancy = await response.json();
    expect(vacancy.id).toBe(vacancyId);
  });

  test('should return health check status', async ({ request }) => {
    const response = await request.get(`${baseUrl}/api/health`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('status');
    expect(data.status).toBe('healthy');
    expect(data).toHaveProperty('chat_service_available');
  });

  test('should handle recommendations endpoint', async ({ request }) => {
    const response = await request.post(`${baseUrl}/api/recommendations`, {
      data: {
        user_skills: ['Python', 'Django'],
        user_experience: 'middle'
      }
    });
    
    expect(response.status()).toBe(200);
    const data = await response.json();
    
    expect(data).toHaveProperty('recommended_vacancies');
    expect(data).toHaveProperty('skill_recommendations');
    expect(data).toHaveProperty('analysis');
    
    expect(Array.isArray(data.recommended_vacancies)).toBeTruthy();
    expect(Array.isArray(data.skill_recommendations)).toBeTruthy();
    expect(typeof data.analysis).toBe('object');
  });

  test('should handle invalid request gracefully', async ({ request }) => {
    const response = await request.post(`${baseUrl}/api/chat`, {
      data: {
        message: '' // Invalid - empty message
      }
    });
    
    // Even with an empty message, the API should handle it gracefully
    // Status might be 200 (successful processing) or 422 (validation error)
    expect([200, 422]).toContain(response.status());
  });
});