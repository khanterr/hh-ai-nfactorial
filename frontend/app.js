// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// State
let jobs = [];
let companies = [];
let filters = {
    city: '',
    grade: '',
    format: '',
    search: ''
};

// DOM Elements
const jobsContainer = document.getElementById('jobsContainer');
const jobCount = document.getElementById('jobCount');
const cityFilter = document.getElementById('cityFilter');
const gradeFilter = document.getElementById('gradeFilter');
const formatFilter = document.getElementById('formatFilter');
const searchInput = document.getElementById('searchInput');
const clearFiltersBtn = document.getElementById('clearFilters');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadInitialData();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    cityFilter.addEventListener('change', (e) => {
        filters.city = e.target.value;
        applyFilters();
    });

    gradeFilter.addEventListener('change', (e) => {
        filters.grade = e.target.value;
        applyFilters();
    });

    formatFilter.addEventListener('change', (e) => {
        filters.format = e.target.value;
        applyFilters();
    });

    searchInput.addEventListener('input', debounce((e) => {
        filters.search = e.target.value.toLowerCase();
        applyFilters();
    }, 300));

    clearFiltersBtn.addEventListener('click', () => {
        clearFilters();
    });
}

// Load initial data from API
async function loadInitialData() {
    try {
        jobsContainer.innerHTML = '<div class="loading">Loading jobs...</div>';

        // Fetch jobs and companies in parallel
        const [jobsResponse, companiesResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/jobs`),
            fetch(`${API_BASE_URL}/companies`)
        ]);

        if (!jobsResponse.ok || !companiesResponse.ok) {
            throw new Error('Failed to fetch data');
        }

        jobs = await jobsResponse.json();
        companies = await companiesResponse.json();

        // Create a map for quick company lookup
        const companyMap = {};
        companies.forEach(company => {
            companyMap[company.id] = company;
        });

        // Enrich jobs with company data
        jobs = jobs.map(job => ({
            ...job,
            company: companyMap[job.company_id] || { name: 'Unknown Company' }
        }));

        displayJobs(jobs);
    } catch (error) {
        console.error('Error loading data:', error);
        jobsContainer.innerHTML = `
            <div class="error">
                Failed to load jobs. Please make sure the backend server is running at ${API_BASE_URL}
                <br><br>
                Error: ${error.message}
            </div>
        `;
    }
}

// Apply filters
function applyFilters() {
    let filteredJobs = jobs;

    // Apply city filter
    if (filters.city) {
        filteredJobs = filteredJobs.filter(job =>
            job.city && job.city.toLowerCase() === filters.city.toLowerCase()
        );
    }

    // Apply grade filter
    if (filters.grade) {
        filteredJobs = filteredJobs.filter(job =>
            job.grade && job.grade.toLowerCase() === filters.grade.toLowerCase()
        );
    }

    // Apply format filter
    if (filters.format) {
        filteredJobs = filteredJobs.filter(job =>
            job.format && job.format.toLowerCase() === filters.format.toLowerCase()
        );
    }

    // Apply search filter
    if (filters.search) {
        filteredJobs = filteredJobs.filter(job => {
            const searchTerm = filters.search;
            return (
                job.title.toLowerCase().includes(searchTerm) ||
                job.company.name.toLowerCase().includes(searchTerm) ||
                (job.description && job.description.toLowerCase().includes(searchTerm))
            );
        });
    }

    displayJobs(filteredJobs);
}

// Display jobs
function displayJobs(jobsToDisplay) {
    jobCount.textContent = jobsToDisplay.length;

    if (jobsToDisplay.length === 0) {
        jobsContainer.innerHTML = `
            <div class="loading">
                No jobs found matching your criteria. Try adjusting your filters.
            </div>
        `;
        return;
    }

    jobsContainer.innerHTML = jobsToDisplay.map(job => createJobCard(job)).join('');
}

// Create job card HTML
function createJobCard(job) {
    const companyInitial = job.company.name.charAt(0).toUpperCase();
    const description = job.description || 'No description available';
    const truncatedDescription = description.length > 200
        ? description.substring(0, 200) + '...'
        : description;

    const postedDate = job.created_at ? formatDate(job.created_at) : 'Recently posted';

    return `
        <div class="job-card" onclick="viewJobDetails(${job.id})">
            <div class="company-logo">${companyInitial}</div>

            <div class="job-info">
                <h3 class="job-title">${escapeHtml(job.title)}</h3>
                <div class="company-name">${escapeHtml(job.company.name)}</div>

                <div class="job-details">
                    ${job.city ? `<span class="detail-item">📍 ${escapeHtml(job.city)}</span>` : ''}
                    ${job.grade ? `<span class="detail-item">💼 ${escapeHtml(job.grade)}</span>` : ''}
                    ${job.format ? `<span class="detail-item">🏢 ${escapeHtml(job.format)}</span>` : ''}
                    ${job.salary ? `<span class="detail-item">💰 ${escapeHtml(job.salary)}</span>` : ''}
                </div>

                <div class="job-description">${escapeHtml(truncatedDescription)}</div>

                <div class="job-tags">
                    ${job.grade ? `<span class="tag">${escapeHtml(job.grade)}</span>` : ''}
                    ${job.format ? `<span class="tag">${escapeHtml(job.format)}</span>` : ''}
                    ${job.city ? `<span class="tag">${escapeHtml(job.city)}</span>` : ''}
                </div>
            </div>

            <div class="job-actions">
                <div class="posted-time">${postedDate}</div>
                <button class="save-btn" onclick="event.stopPropagation(); saveJob(${job.id})" title="Save job">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z"/>
                    </svg>
                </button>
                <button class="apply-btn" onclick="event.stopPropagation(); applyToJob(${job.id})">Apply</button>
            </div>
        </div>
    `;
}

// Clear all filters
function clearFilters() {
    filters = {
        city: '',
        grade: '',
        format: '',
        search: ''
    };

    cityFilter.value = '';
    gradeFilter.value = '';
    formatFilter.value = '';
    searchInput.value = '';

    displayJobs(jobs);
}

// Job actions
function viewJobDetails(jobId) {
    console.log('View job details:', jobId);
    // In a real app, this would navigate to a detailed job page
    alert(`Opening job details for Job ID: ${jobId}\n\nIn a full implementation, this would show:\n- Complete job description\n- Company details\n- Requirements\n- Benefits\n- Application form`);
}

function saveJob(jobId) {
    console.log('Save job:', jobId);
    alert(`Job saved! Job ID: ${jobId}\n\nIn a full implementation, this would save the job to your favorites.`);
}

function applyToJob(jobId) {
    console.log('Apply to job:', jobId);
    alert(`Ready to apply! Job ID: ${jobId}\n\nIn a full implementation, this would:\n- Open the application form\n- Upload your resume\n- Submit your application`);
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
        return 'Today';
    } else if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
    } else {
        return date.toLocaleDateString();
    }
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
