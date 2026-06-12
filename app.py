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
# Session State
# -------------------------

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "score" not in st.session_state:
    st.session_state.score = None

if "gemini_result" not in st.session_state:
    st.session_state.gemini_result = None

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
# Start Analysis Button
# -------------------------

start_analysis = st.button("🚀 Start Analysis")

# -------------------------
# Analysis
# -------------------------

if start_analysis:

    if not uploaded_file:
        st.error("❌ Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.error("❌ Please paste a job description.")
        st.stop()

    try:

        resume_text = extract_text(uploaded_file)

        if not resume_text:
            st.error(
                "❌ No text could be extracted from the uploaded PDF."
            )
            st.stop()

        if not resume_text.strip():
            st.error(
                "❌ The uploaded resume appears to be empty."
            )
            st.stop()

        if len(resume_text.split()) < 20:
            st.error(
                "❌ The resume contains insufficient text for analysis."
            )
            st.stop()

        score = calculate_similarity(
            resume_text,
            job_description
        )

        st.session_state.resume_text = resume_text
        st.session_state.score = score
        st.session_state.analysis_complete = True
        st.session_state.gemini_result = None

    except Exception as e:

        st.error(
            f"Application Error:\n\n{e}"
        )

# -------------------------
# Show Analysis Results
# -------------------------

if st.session_state.analysis_complete:

    st.subheader("📊 Resume Match Score")

    st.metric(
        label="Resume Match %",
        value=f"{st.session_state.score}%"
    )

    with st.expander(
        "📄 View Extracted Resume Text"
    ):
        st.text(
            st.session_state.resume_text[:2000]
        )

    st.markdown("---")

    # -------------------------
    # Gemini Button
    # -------------------------

    gemini_feedback = st.button(
        "🤖 Gemini Feedback"
    )

    if gemini_feedback:

        try:

            with st.spinner(
                "Generating Gemini Feedback..."
            ):

                result = analyze_resume(
                    st.session_state.resume_text[:4000],
                    job_description[:1500]
                )

            st.session_state.gemini_result = result

        except Exception as e:

            st.error(
                f"AI Analysis Error:\n\n{e}"
            )

    # -------------------------
    # Show Gemini Result
    # -------------------------

    if st.session_state.gemini_result:

        st.subheader(
            "🤖 Gemini Feedback"
        )

        st.markdown(
            st.session_state.gemini_result
        )

        pdf_file = create_pdf_report(
            st.session_state.score,
            st.session_state.gemini_result
        )

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="resume_report.pdf",
            mime="application/pdf"
        )

# -------------------------
# Default Message
# -------------------------

if not st.session_state.analysis_complete:

    st.info(
        "📌 Upload a resume and paste a job description to begin."
    )

