import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an experienced recruiter, hiring manager, and career coach.

The resume has already been scored separately by an NLP system.

Return your response in Markdown format using the following structure:

## Strengths
- List strong points in the resume.

## Missing Skills
- List skills from the job description that appear missing.

## Resume Improvements
- Suggest improvements to resume content, wording, or structure.

## Important Keywords
- Keywords that should be added naturally to improve visibility.

## Project Suggestions
- Projects that would strengthen the candidate's profile for this role.

## Interview Preparation Tips
- Topics and skills the candidate should prepare for.

Keep the response concise, practical, and professional.

Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = model.generate_content(prompt)

    return response.text