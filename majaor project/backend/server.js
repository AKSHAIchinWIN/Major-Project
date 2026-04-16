const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Ensure uploads directory exists
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Set up multer for file uploads
const upload = multer({ dest: 'uploads/' });

// API to analyze resume vs job description
app.post('/api/resume-analysis', upload.single('resume'), (req, res) => {
    const jobDesc = req.body.jobDescription || '';
    
    // Mocking an ATS score and missing skills logic
    setTimeout(() => {
        let ats = 78;
        let missing = ['TypeScript', 'GraphQL', 'AWS', 'Docker'];

        // mock dynamic behavior
        if (jobDesc.toLowerCase().includes('python')) {
            ats = 65;
            missing.push('Python (from Job Description)');
        }
        if (jobDesc.toLowerCase().includes('java')) {
            ats = 60;
            missing.push('Java (from Job Description)');
        }

        res.json({
            success: true,
            atsScore: ats,
            extractedSkills: ['JavaScript', 'HTML', 'CSS', 'React', 'Node.js'],
            missingSkills: missing,
            message: 'Resume analyzed against Job Description successfully.'
        });
    }, 1500); // simulate delay
});

// API for career path
app.get('/api/career-path', (req, res) => {
    res.json({
        success: true,
        currentLevel: 'Junior Developer',
        targetRole: 'Full Stack Engineer',
        roadmapSteps: [
            { id: 1, title: 'Master Frontend Basics', completed: true },
            { id: 2, title: 'Learn React & State Management', completed: true },
            { id: 3, title: 'Backend with Node.js & Express', completed: false },
            { id: 4, title: 'Database Design (SQL/NoSQL)', completed: false },
            { id: 5, title: 'Cloud Deployment (AWS/Vercel)', completed: false }
        ]
    });
});

// API for courses
app.get('/api/courses', (req, res) => {
    res.json({
        success: true,
        courses: [
            { id: 101, title: 'AWS Cloud Practitioner Essentials', provider: 'Coursera', level: 'Beginner', duration: '2 weeks' },
            { id: 102, title: 'TypeScript for React Developers', provider: 'Udemy', level: 'Intermediate', duration: '15 hours' },
            { id: 103, title: 'Docker for Absolute Beginners', provider: 'Pluralsight', level: 'Beginner', duration: '4 hours' },
            { id: 104, title: 'GraphQL with Apollo Server', provider: 'Frontend Masters', level: 'Advanced', duration: '6 hours' }
        ]
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
