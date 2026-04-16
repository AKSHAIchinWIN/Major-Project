const API_BASE_URL = 'http://localhost:5000/api';

// Set active navigation based on current HTML file
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (currentPath.includes(href) || (currentPath.endsWith('/') && href === 'index.html')) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
});

// Common fetch utility with error handling
async function fetchFromAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Function to handle resume and job description upload
async function uploadResumeAndJob(file, jobDescription) {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('jobDescription', jobDescription);
    
    return fetchFromAPI('/resume-analysis', {
        method: 'POST',
        body: formData
    });
}

// Function to get career path (for career.html)
async function getCareerPath() {
    return fetchFromAPI('/career-path');
}

// Function to get courses (for courses.html)
async function getCourses() {
    return fetchFromAPI('/courses');
}
