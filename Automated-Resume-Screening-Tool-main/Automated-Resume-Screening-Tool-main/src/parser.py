import re

# Detect years of experience
def extract_experience(text):

    pattern = r'(\d+)\s+years'

    matches = re.findall(pattern, text.lower())

    if matches:
        return max([int(year) for year in matches])

    return 0


# Detect education
def extract_education(text):

    education_keywords = [
        "b.tech",
        "m.tech",
        "bca",
        "mca",
        "bsc",
        "msc",
        "phd",
        "computer science",
        "data science"
    ]

    found = []

    text = text.lower()

    for edu in education_keywords:
        if edu in text:
            found.append(edu)

    return found


# Detect certifications
def extract_certifications(text):

    certification_keywords = [
        "aws",
        "azure",
        "google cloud",
        "machine learning",
        "data analytics",
        "python certification",
        "tensorflow"
    ]

    found = []

    text = text.lower()

    for cert in certification_keywords:
        if cert in text:
            found.append(cert)

    return found