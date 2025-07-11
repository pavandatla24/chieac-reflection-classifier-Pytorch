import os
import re
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader

def extract_text_from_docx(path):
    try:
        doc = Document(path)
        return " ".join([p.text for p in doc.paragraphs])
    except:
        return ""

def extract_text_from_pdf(path):
    try:
        reader = PdfReader(path)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except:
        return ""

def clean_text(text):
    # Lowercase, remove extra spaces, remove newlines
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)  # optional: remove punctuation
    return text.strip()


data_dir = "data/ChieAC_Student_Reflections"


records = []

for fname in os.listdir(data_dir):
    full_path = os.path.join(data_dir, fname)
    
    if fname.endswith(".docx"):
        raw = extract_text_from_docx(full_path)
    elif fname.endswith(".pdf"):
        raw = extract_text_from_pdf(full_path)
    else:
        continue

    if len(raw.strip()) < 100:
        continue  # skip empty or tiny documents

    cleaned = clean_text(raw)
    records.append({
        "filename": fname,
        "text": cleaned
    })

df = pd.DataFrame(records)
df.to_csv("data/reflections_cleaned.csv", index=False)
print("Saved to data/reflections_cleaned.csv")
