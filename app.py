import streamlit as st
from analyzer import (
    extract_text, analyze_resume, build_report,
    extract_skills, SKILL_CATEGORIES
)

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer")
st.caption("Compare a resume with a job description and get an explainable match report.")

with st.sidebar:
    st.header("How it works")
    st.write("1. Upload a resume (PDF, DOCX or TXT).")
    st.write("2. Paste the job description.")
    st.write("3. Review the match score, skills and improvement suggestions.")
    st.info("This starter project runs locally. It does not send resumes to an external AI service.")

col1, col2 = st.columns([1, 1])
with col1:
    uploaded_file = st.file_uploader("Upload candidate resume", type=["pdf", "docx", "txt"])
with col2:
    st.write("**Supported formats**")
    st.write("PDF · Word (.docx) · Text (.txt)")

job_description = st.text_area(
    "Paste the job description",
    height=260,
    placeholder="Paste the complete job description here, including responsibilities, required skills and qualifications..."
)

analyze_clicked = st.button("Analyze resume", type="primary", use_container_width=True)

if analyze_clicked:
    if uploaded_file is None:
        st.error("Please upload a resume first.")
        st.stop()
    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    try:
        resume_text = extract_text(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the uploaded file: {exc}")
        st.stop()

    if len(resume_text.strip()) < 40:
        st.error("Not enough readable text was found. If this is a scanned PDF, convert it to a text-based PDF or run OCR first.")
        st.stop()

    result = analyze_resume(resume_text, job_description)

    st.divider()
    st.subheader("Analysis results")

    score_col, matched_col, missing_col = st.columns(3)
    score_col.metric("Overall match", f"{result['match_score']}%")
    matched_col.metric("Matched skills", len(result["matched_skills"]))
    missing_col.metric("Skills to develop", len(result["missing_skills"]))

    st.progress(result["match_score"] / 100)

    if result["match_score"] >= 75:
        st.success("Strong keyword and content alignment. Review the evidence below before making a decision.")
    elif result["match_score"] >= 50:
        st.warning("Moderate alignment. The candidate may match some requirements, but there are gaps to review.")
    else:
        st.info("Limited alignment based on the text provided. Review transferable experience and context before deciding.")

    left, right = st.columns(2)
    with left:
        st.markdown("#### ✅ Matched skills")
        if result["matched_skills"]:
            st.write(", ".join(result["matched_skills"]))
        else:
            st.write("No skills from the built-in list were detected in both texts.")
    with right:
        st.markdown("#### 📌 Skills not found in resume")
        if result["missing_skills"]:
            st.write(", ".join(result["missing_skills"]))
        else:
            st.write("No missing skills detected from the job description's extracted skill list.")

    st.markdown("#### Match breakdown")
    st.write(f"**Text similarity:** {result['similarity_score']}%")
    st.write(f"**Required-skill coverage:** {result['skill_coverage']}%")
    st.caption("The overall score combines text similarity and skill coverage. It is an indicative screening aid, not a hiring decision.")

    st.markdown("#### Suggestions for improving the resume")
    for suggestion in result["suggestions"]:
        st.write(f"- {suggestion}")

    with st.expander("View extracted resume text"):
        st.text(resume_text[:12000])

    report = build_report(result, uploaded_file.name)
    st.download_button(
        "⬇️ Download analysis report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()
st.caption("Responsible use: scores can miss context, transferable skills and non-traditional experience. Do not use this score as the sole basis for employment decisions. Obtain consent before processing candidate data and delete files when no longer needed.")
