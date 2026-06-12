import streamlit as st

from utils.pdf_parser import extract_text
from utils.similarity import calculate_similarity
from utils.gemini_service import analyze_resume
from utils.pdf_report import create_pdf_report

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -------------------------
# Header
# -------------------------

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and compare it against a job description."
)

# -------------------------
# Upload Resume
# -------------------------

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# -------------------------
# Job Description
# -------------------------

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

# -------------------------
# Main Logic
# -------------------------

if uploaded_file and job_description:

    try:

        # Extract Resume Text
        resume_text = extract_text(uploaded_file)

        # Limit Gemini tokens
        resume_text_ai = resume_text[:4000]
        job_description_ai = job_description[:1500]

        # Resume Match Score
        score = calculate_similarity(
            resume_text,
            job_description
        )

        st.subheader("📊 Resume Match Score")

        st.metric(
            label="Resume Match %",
            value=f"{score}%"
        )

        # Resume Preview
        with st.expander(
            "📄 View Extracted Resume Text"
        ):

            st.text(
                resume_text[:2000]
            )

        # Gemini Analysis
        if st.button("🤖 Get AI Advice"):

            try:

                with st.spinner(
                    "Analyzing Resume..."
                ):

                    result = analyze_resume(
                        resume_text_ai,
                        job_description_ai
                    )

                st.subheader(
                    "💡 AI Career Advice"
                )

                st.markdown(
                    result
                )

                # PDF Report
                pdf_file = create_pdf_report(
                    score,
                    result
                )

                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_file,
                    file_name="resume_report.pdf",
                    mime="application/pdf"
                )

            except Exception as e:

                st.error(
                    f"AI Analysis Error:\n\n{e}"
                )

                st.info(
                    "If Gemini quota is exceeded, wait a minute and try again."
                )

    except Exception as e:

        st.error(
            f"Application Error:\n\n{e}"
        )

else:

    st.info(
        "📌 Upload a resume and paste a job description to begin."
    )