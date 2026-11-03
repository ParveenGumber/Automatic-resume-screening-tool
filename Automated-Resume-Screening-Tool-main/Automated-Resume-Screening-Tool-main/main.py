import os
import pandas as pd

from src.extract_text import extract_text   
from src.cleaner import clean_text
from src.matcher import calculate_similarity
from src.skill_extractor import extract_skills

from src.parser import (
    extract_experience,
    extract_education,
    extract_certifications
)

# -----------------------------
# LOAD JOB DESCRIPTION
# -----------------------------

with open("data/job_description.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

cleaned_job_description = clean_text(job_description)

# Extract required skills from job description
job_skills = extract_skills(cleaned_job_description)

# -----------------------------
# PROCESS RESUMES
# -----------------------------

results = []

resume_folder = "resumes"

print("\n===== ATS Resume Screening Started =====\n")

for file_name in os.listdir(resume_folder):

    file_path = os.path.join(resume_folder, file_name)

    print(f"Processing Resume: {file_name}")

    # Extract Resume Text
    resume_text = extract_text(file_path)

    # Clean Resume Text
    cleaned_resume = clean_text(resume_text)

    # Calculate Similarity Score
    similarity_score = calculate_similarity(
        cleaned_job_description,
        cleaned_resume
    )

    # Extract Skills
    resume_skills = extract_skills(cleaned_resume)

    # Extract Experience
    experience = extract_experience(cleaned_resume)

    # Extract Education
    education = extract_education(cleaned_resume)

    # Extract Certifications
    certifications = extract_certifications(cleaned_resume)

    # Find Matching Skills
    matched_skills = list(
        set(job_skills).intersection(set(resume_skills))
    )

    # Skill Match Percentage
    skill_match_percentage = (
        len(matched_skills) / len(job_skills)
    ) * 100

    # Final ATS Score
    final_score = (
        similarity_score * 0.7
        + skill_match_percentage * 0.3
    )

    # Shortlist Decision
    decision = (
        "Shortlisted"
        if final_score >= 50
        else "Rejected"
    )

    # Save Results
    results.append({
        "Resume": file_name,
        "Experience (Years)": experience,
        "Education": ", ".join(education),
        "Certifications": ", ".join(certifications),
        "Similarity Score": round(similarity_score, 2),
        "Skill Match %": round(skill_match_percentage, 2),
        "Final Score": round(final_score, 2),
        "Matched Skills": ", ".join(matched_skills),
        "Decision": decision
    })

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

df = pd.DataFrame(results)

# Sort by Final Score
df = df.sort_values(
    by="Final Score",
    ascending=False
)

# -----------------------------
# SAVE CSV REPORT
# -----------------------------

output_path = "outputs/resume_ranking.csv"

df.to_csv(output_path, index=False)

# -----------------------------
# DISPLAY RESULTS
# -----------------------------

print("\n===== FINAL ATS RANKING =====\n")

print(df)

print(f"\nCSV Report Saved Successfully: {output_path}")