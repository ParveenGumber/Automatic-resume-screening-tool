import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

from src.extract_text import extract_text
from src.cleaner import clean_text
from src.matcher import calculate_similarity
from src.skill_extractor import extract_skills

from src.parser import (
    extract_experience,
    extract_education,
    extract_certifications
)

from src.file_handler import save_uploaded_file

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="ATS Resume Screening Tool",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------
# SIDEBAR
# ---------------------------------

st.sidebar.title("📌 ATS Dashboard")

st.sidebar.info(
    """
    Automated Resume Screening Tool

    Features:
    ✅ Resume Parsing
    ✅ Skill Matching
    ✅ ATS Scoring
    ✅ Resume Ranking
    ✅ Resume Upload
    """
)

# ---------------------------------
# FILE UPLOAD
# ---------------------------------

uploaded_files = st.sidebar.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files:

    for uploaded_file in uploaded_files:

        save_uploaded_file(uploaded_file)

    st.sidebar.success(
        "Resumes uploaded successfully!"
    )

# ---------------------------------
# TITLE
# ---------------------------------

st.title("📄 Automated Resume Screening Tool")

st.markdown(
    "### AI-Powered Applicant Tracking System"
)

# ---------------------------------
# LOAD JOB DESCRIPTION
# ---------------------------------

with open("data/job_description.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

cleaned_job_description = clean_text(job_description)

job_skills = extract_skills(cleaned_job_description)

# ---------------------------------
# PROCESS RESUMES
# ---------------------------------

results = []

resume_folder = "resumes"

for file_name in os.listdir(resume_folder):

    file_path = os.path.join(
        resume_folder,
        file_name
    )

    resume_text = extract_text(file_path)

    cleaned_resume = clean_text(resume_text)

    # Similarity Score
    similarity_score = calculate_similarity(
        cleaned_job_description,
        cleaned_resume
    )

    # Skills
    resume_skills = extract_skills(
        cleaned_resume
    )

    matched_skills = list(
        set(job_skills).intersection(
            set(resume_skills)
        )
    )

    skill_match_percentage = (
        len(matched_skills) / len(job_skills)
    ) * 100

    # Final Score
    final_score = (
        similarity_score * 0.7
        + skill_match_percentage * 0.3
    )

    # Experience
    experience = extract_experience(
        cleaned_resume
    )

    # Education
    education = extract_education(
        cleaned_resume
    )

    # Certifications
    certifications = extract_certifications(
        cleaned_resume
    )

    # Decision
    decision = (
        "Shortlisted"
        if final_score >= 50
        else "Rejected"
    )

    # Store Results
    results.append({
        "Resume": file_name,
        "Experience": experience,
        "Education": ", ".join(education),
        "Certifications": ", ".join(certifications),
        "Similarity Score": round(similarity_score, 2),
        "Skill Match %": round(skill_match_percentage, 2),
        "Final Score": round(final_score, 2),
        "Decision": decision
    })

# ---------------------------------
# CREATE DATAFRAME
# ---------------------------------

df = pd.DataFrame(results)

df = df.sort_values(
    by="Final Score",
    ascending=False
)

# ---------------------------------
# METRICS
# ---------------------------------

total_resumes = len(df)

shortlisted_count = len(
    df[df["Decision"] == "Shortlisted"]
)

average_score = round(
    df["Final Score"].mean(),
    2
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "📄 Total Resumes",
    total_resumes
)

col2.metric(
    "✅ Shortlisted",
    shortlisted_count
)

col3.metric(
    "📊 Average ATS Score",
    average_score
)

# ---------------------------------
# SHOW TABLE
# ---------------------------------

st.subheader("📋 Resume Ranking Table")

st.dataframe(df)

# ---------------------------------
# BAR CHART
# ---------------------------------

st.subheader("📈 ATS Score Visualization")

fig, ax = plt.subplots(
    figsize=(8, 4)
)

ax.bar(
    df["Resume"],
    df["Final Score"]
)

ax.set_xlabel("Resume")

ax.set_ylabel("Final Score")

plt.xticks(rotation=15)

st.pyplot(fig)

# ---------------------------------
# PIE CHART
# ---------------------------------

st.subheader("📊 Selection Ratio")

decision_counts = df["Decision"].value_counts()

fig2, ax2 = plt.subplots()

ax2.pie(
    decision_counts,
    labels=decision_counts.index,
    autopct='%1.1f%%'
)

st.pyplot(fig2)

# ---------------------------------
# SHORTLISTED
# ---------------------------------

st.subheader("🏆 Shortlisted Candidates")

shortlisted = df[
    df["Decision"] == "Shortlisted"
]

st.dataframe(shortlisted)

# ---------------------------------
# DOWNLOAD CSV
# ---------------------------------

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download ATS Report",
    data=csv,
    file_name="resume_ranking.csv",
    mime="text/csv"
)

# ---------------------------------
# FOOTER
# ---------------------------------

st.markdown("---")

st.caption(
    "Built with Python, NLP, TF-IDF, Cosine Similarity, and Streamlit"
)