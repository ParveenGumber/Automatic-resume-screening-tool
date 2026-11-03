import pdfplumber
import docx


def extract_pdf_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return text


def extract_docx_text(docx_path):

    doc = docx.Document(docx_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_txt_text(txt_path):

    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text(file_path):

    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx_text(file_path)

    elif file_path.endswith(".txt"):
        return extract_txt_text(file_path)

    else:
        return ""