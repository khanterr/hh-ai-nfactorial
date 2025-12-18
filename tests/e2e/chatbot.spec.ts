import { test, expect } from '@playwright/test';

test.describe('AI Chat Bot for Job Vacancies', () => {
  test.beforeEach(async ({ page }) => {
    // Serve the test HTML file or navigate to the app
    await page.goto('file:///Users/kuka/Documents/Nfactorial/project3/hh-ai-nfactorial/ai-engineer/test_frontend.html');
  });

  test('should display initial bot message', async ({ page }) => {
    // Wait for the initial bot message to appear
    await expect(page.locator('.message.bot')).toContainText('Привет! Я AI-ассистент для подбора вакансий. Чем могу помочь?');
  });

  test('should send a message and receive a response', async ({ page }) => {
    // Fill in the message input
    await page.fill('#messageInput', 'Привет, помоги найти вакансии по Python разработке');

    // Click the send button
    await page.click('#sendButton');

    // Wait for the user message to appear in the chat
    await expect(page.locator('.message.user').last()).toContainText('Привет, помоги найти вакансии по Python разработке');

    // Wait for the bot response to appear (timeout after 10 seconds)
    await page.waitForSelector('.message.bot', { state: 'visible', timeout: 10000 });
  });

  test('should handle Enter key press correctly', async ({ page }) => {
    // Fill in the message input
    await page.fill('#messageInput', 'Какие навыки требуются для Data Scientist?');

    // Press Enter to send the message
    await page.press('#messageInput', 'Enter');

    // Wait for the user message to appear in the chat
    await expect(page.locator('.message.user').last()).toContainText('Какие навыки требуются для Data Scientist?');

    // Wait for the bot response to appear
    await page.waitForSelector('.message.bot', { state: 'visible', timeout: 10000 });
  });

  test('should update API URL configuration', async ({ page }) => {
    const newApiUrl = 'http://localhost:8000';
    
    // Change the API URL
    await page.fill('#apiUrl', newApiUrl);
    
    // Verify the URL was updated
    await expect(page.locator('#apiUrl')).toHaveValue(newApiUrl);
  });

  test('should update user skills configuration', async ({ page }) => {
    const newSkills = 'JavaScript, React, Node.js';
    
    // Change the user skills
    await page.fill('#userSkills', newSkills);
    
    // Verify the skills were updated
    await expect(page.locator('#userSkills')).toHaveValue(newSkills);
  });

  test('should update user experience level', async ({ page }) => {
    const newExperience = 'senior';
    
    // Change the user experience level
    await page.fill('#userExperience', newExperience);
    
    // Verify the experience was updated
    await expect(page.locator('#userExperience')).toHaveValue(newExperience);
  });

  test('should disable send button while loading', async ({ page }) => {
    // Mock the API call to simulate delay
    await page.route('**/api/chat', async route => {
      await new Promise(resolve => setTimeout(resolve, 2000)); // 2 second delay
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          response: 'Test response from API',
          suggested_vacancies: [1, 2],
          skill_recommendations: ['Docker', 'Kubernetes']
        })
      });
    });

    // Fill in the message input
    await page.fill('#messageInput', 'Тестовое сообщение');

    // Click the send button
    await page.click('#sendButton');

    // Check that the button is disabled
    await expect(page.locator('#sendButton')).toBeDisabled();

    // Wait for the response to appear
    await page.waitForSelector('.message.bot', { state: 'visible' });

    // The button should become enabled again after the response
    await expect(page.locator('#sendButton')).toBeEnabled();
  });

  test('should show error message when API is unavailable', async ({ page }) => {
    // Block API requests to simulate failure
    await page.route('**/api/chat', route => route.abort());

    // Fill in the message input
    await page.fill('#messageInput', 'Тест сообщения при ошибке API');

    // Click the send button
    await page.click('#sendButton');

    // Wait for the error message to appear
    await page.waitForSelector('.message.bot', { state: 'visible', timeout: 10000 });

    // Check that an error message was displayed
    const botMessages = page.locator('.message.bot');
    const botMessageCount = await botMessages.count();
    await expect(botMessages.nth(botMessageCount - 1)).toContainText('Ошибка:');
  });

  test('should show additional recommendations when available', async ({ page }) => {
    // Mock API response with recommendations
    await page.route('**/api/chat', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        response: 'Вот несколько рекомендованных вакансий',
        suggested_vacancies: [1, 4],
        skill_recommendations: ['Docker', 'Kubernetes']
      })
    }));

    // Fill in the message input
    await page.fill('#messageInput', 'Рекомендуй вакансии');

    // Click the send button
    await page.click('#sendButton');

    // Wait for the response and recommendations to appear
    await page.waitForSelector('.message.bot', { state: 'visible', timeout: 10000 });

    // Verify that both the response and recommendations appear
    await expect(page.locator('.message.bot')).toContainText('Вот несколько рекомендованных вакансий');
    await expect(page.locator('.message.bot')).toContainText('💡 Рекомендованные вакансии: 1, 4');
    await expect(page.locator('.message.bot')).toContainText('📚 Рекомендуемые навыки: Docker, Kubernetes');
  });

  test('should maintain conversation history', async ({ page }) => {
    // Mock the API to return different responses
    let messageCount = 0;
    await page.route('**/api/chat', route => {
      messageCount++;
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          response: `Ответ на сообщение ${messageCount}`,
          suggested_vacancies: [],
          skill_recommendations: []
        })
      });
    });

    // Send first message
    await page.fill('#messageInput', 'Первое сообщение');
    await page.click('#sendButton');
    await page.waitForSelector('.message.bot', { state: 'visible', timeout: 5000 });

    // Send second message
    await page.fill('#messageInput', 'Второе сообщение');
    await page.click('#sendButton');
    await page.waitForSelector('.message.bot', { state: 'visible', timeout: 5000 });

    // Verify that multiple messages are displayed
    const userMessages = page.locator('.message.user');
    await expect(userMessages).toHaveCount(2);

    const botMessages = page.locator('.message.bot');
    await expect(botMessages).toHaveCount(3); // Including the initial message
  });
});