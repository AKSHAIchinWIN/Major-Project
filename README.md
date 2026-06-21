# 📄 GenAI Resume Analyzer

An AI-powered web app that compares a resume against a job description, returns a quantitative match score, and generates qualitative improvement feedback using Google's Gemini AI packaged as a downloadable PDF report.

**Live demo:** https://genai-resume-analyzer-yhzaead2rmkfhcibzntbbv.streamlit.app/

---

## Overview

Job seekers often don't know how well their resume actually aligns with a specific job posting, or what to change to improve it. This project combines a classical NLP similarity score with LLM-generated feedback to give two complementary signals: a numeric match percentage and concrete, readable suggestions for improvement.

## Features

- PDF resume upload and text extraction
- Resume-to-job-description match scoring using TF-IDF and cosine similarity
- AI-generated, personalized improvement feedback via Gemini AI
- Input validation for empty, unreadable, or unrealistically short resumes before analysis runs
- Two-step workflow: similarity scoring first, AI feedback as a separate, user-triggered step (reduces unnecessary AI calls)
- Downloadable PDF analysis report combining the match score and AI feedback
- Session-state management so results persist across interactions without recomputation
- Deployed on Streamlit Community Cloud

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Web App / Deployment | Streamlit, Streamlit Community Cloud |
| NLP / Matching | Scikit-Learn (TF-IDF, Cosine Similarity) |
| AI Feedback | Gemini AI |
| PDF Parsing | PDFPlumber |
| PDF Report Generation | ReportLab |

## How It Works

1. **Upload & validation** - The user uploads a resume PDF and pastes a job description. Before any analysis runs, the app checks that text was successfully extracted, that the resume isn't empty, and that it contains a minimum amount of content (at least 20 words) to avoid wasting an analysis cycle on unusable input.
2. **Similarity scoring** - Resume and job description text are vectorized with TF-IDF and compared using cosine similarity to produce a match percentage. This step is fast, local, and doesn't depend on an external AI call.
3. **AI feedback (on demand)** - Only if the user explicitly requests it, the resume and job description text are sent to Gemini AI for qualitative feedback. Both inputs are truncated (resume to 4,000 characters, job description to 1,500) before the call, to keep the request within a reliable context size and avoid degraded or truncated responses from an oversized prompt.
4. **Report generation** - The match score and Gemini's feedback are combined into a downloadable PDF report using ReportLab.

## Project Structure

```
GenAi-Resume-Analyzer/
├── app.py                   # Streamlit UI, workflow control, session state
├── utils/
│   ├── pdf_parser.py         # PDF text extraction
│   ├── similarity.py         # TF-IDF + cosine similarity scoring
│   ├── gemini_service.py     # Gemini AI feedback generation
│   └── pdf_report.py         # PDF report generation (ReportLab)
├── requirements.txt
└── README.md
```

## Running Locally

```bash
git clone https://github.com/GauravSh-7/GenAi-Resume-Analyzer.git
cd GenAi-Resume-Analyzer
pip install -r requirements.txt
streamlit run app.py
```
A Gemini API key is required for the AI feedback step set it as an environment variable as configured in `utils/gemini_service.py`.

## Design Notes

- **Why split similarity scoring and AI feedback into separate steps?** The TF-IDF score is cheap to compute and gives immediate feedback, while the Gemini call is slower and rate-limited. Decoupling them means a user gets useful signal instantly and only triggers the AI step when they actually want deeper feedback — reducing unnecessary API usage.
- **Why truncate input before the Gemini call?** Long, unbounded prompts increase the risk of the model losing track of relevant details or producing inconsistent output. Capping input length keeps the prompt focused and the response quality more predictable.

## Limitations & Future Improvements

- TF-IDF/cosine similarity captures keyword overlap but not deeper semantic meaning — a future version could use embedding-based similarity for more nuanced matching.
- Truncating resume/job description text means very long documents may lose relevant content; a smarter chunking or summarization step could help.
- No automated tests currently cover the parsing, scoring, or PDF generation logic.
- Gemini feedback quality isn't currently benchmarked against a labeled set of "good" vs. "weak" resume-job pairs.

## Author

[Gaurav](https://github.com/GauravSh-7)
