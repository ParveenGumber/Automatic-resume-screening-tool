SKILLS = [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "pandas",
    "numpy",
    "excel",
    "power bi",
    "communication",
    "problem solving",
    "java",
    "javascript",
    "react"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills