// AI Chat Widget Configuration
const AI_API_BASE_URL = 'http://localhost:8001/api';

// Chat State
let chatHistory = [];
let isProcessing = false;

// DOM Elements
const chatWidget = document.getElementById('chatWidget');
const chatToggle = document.getElementById('chatToggle');
const chatClose = document.getElementById('chatClose');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const chatSend = document.getElementById('chatSend');

// Initialize chat
document.addEventListener('DOMContentLoaded', () => {
    setupChatEventListeners();
});

// Setup Event Listeners
function setupChatEventListeners() {
    chatToggle.addEventListener('click', () => {
        openChat();
    });

    chatClose.addEventListener('click', () => {
        closeChat();
    });

    chatSend.addEventListener('click', () => {
        sendMessage();
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// Open chat widget
function openChat() {
    chatWidget.classList.add('active');
    chatToggle.style.display = 'none';
    chatInput.focus();
}

// Close chat widget
function closeChat() {
    chatWidget.classList.remove('active');
    chatToggle.style.display = 'flex';
}

// Send message
async function sendMessage() {
    const message = chatInput.value.trim();

    if (!message || isProcessing) {
        return;
    }

    // Add user message to chat
    addMessage(message, 'user');
    chatInput.value = '';

    // Update chat history
    chatHistory.push({
        role: 'user',
        content: message
    });

    // Show typing indicator
    const typingId = showTypingIndicator();
    isProcessing = true;
    chatSend.disabled = true;

    try {
        // Send request to AI API
        const response = await fetch(`${AI_API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_history: chatHistory,
                user_skills: [], // Can be populated from user profile
                user_experience: null // Can be populated from user profile
            })
        });

        if (!response.ok) {
            throw new Error('Failed to get response from AI');
        }

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator(typingId);

        // Add AI response to chat
        addMessage(data.response, 'bot');

        // Update chat history
        chatHistory.push({
            role: 'assistant',
            content: data.response
        });

        // If there are suggested vacancies, show them
        if (data.suggested_vacancies && data.suggested_vacancies.length > 0) {
            showSuggestedVacancies(data.suggested_vacancies);
        }

    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator(typingId);

        // Show error message
        addMessage(
            'Извините, произошла ошибка при обработке вашего сообщения. Убедитесь, что AI сервис запущен на порту 8001.',
            'bot'
        );
    } finally {
        isProcessing = false;
        chatSend.disabled = false;
        chatInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';

    const content = document.createElement('div');
    content.className = 'message-content';

    // Convert markdown-like formatting to HTML
    const formattedText = formatMessage(text);
    content.innerHTML = formattedText;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    scrollToBottom();
}

// Format message text
function formatMessage(text) {
    // Simple markdown-like formatting
    let formatted = text;

    // Bold: **text** -> <strong>text</strong>
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Lists: convert lines starting with - or * to <li>
    const lines = formatted.split('\n');
    let inList = false;
    let result = [];

    for (let line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('-') || trimmed.startsWith('*')) {
            if (!inList) {
                result.push('<ul>');
                inList = true;
            }
            result.push(`<li>${trimmed.substring(1).trim()}</li>`);
        } else {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            if (trimmed) {
                result.push(`<p>${trimmed}</p>`);
            }
        }
    }

    if (inList) {
        result.push('</ul>');
    }

    return result.join('');
}

// Show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot-message typing-message';
    typingDiv.id = 'typing-indicator';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';

    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;

    typingDiv.appendChild(avatar);
    typingDiv.appendChild(indicator);
    chatMessages.appendChild(typingDiv);

    scrollToBottom();
    return 'typing-indicator';
}

// Remove typing indicator
function removeTypingIndicator(id) {
    const typing = document.getElementById(id);
    if (typing) {
        typing.remove();
    }
}

// Show suggested vacancies
function showSuggestedVacancies(vacancyIds) {
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'chat-message bot-message';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';

    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = `
        <p><strong>Рекомендую посмотреть эти вакансии:</strong></p>
        <p>ID вакансий: ${vacancyIds.join(', ')}</p>
        <p><small>Прокрутите список вакансий на странице, чтобы посмотреть детали.</small></p>
    `;

    suggestionsDiv.appendChild(avatar);
    suggestionsDiv.appendChild(content);
    chatMessages.appendChild(suggestionsDiv);

    scrollToBottom();
}

// Scroll chat to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Export functions for potential use in main app.js
window.chatWidget = {
    open: openChat,
    close: closeChat,
    sendMessage: (message) => {
        chatInput.value = message;
        sendMessage();
    }
};
