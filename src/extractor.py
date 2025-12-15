# src/extractor.py
from PyPDF2 import PdfReader
import re
from typing import List

def extract_text_from_pdf(path: str) -> str:
    """
    Extracts text from a PDF file using PyPDF2.
    Returns combined text from all pages.
    """
    text_pages: List[str] = []
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_pages.append(page_text)
    except Exception as e:
        # fallback: return empty string or raise
        print(f"[extractor] Error reading {path}: {e}")
    full_text = "\n".join(text_pages)
    # normalize whitespace
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    return full_text

if __name__ == "__main__":
    # quick test
    path = "data/resumes/sample_resume.pdf"
    txt = extract_text_from_pdf(path)
    print(txt[:1000])
