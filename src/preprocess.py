# src/preprocess.py
import re
import nltk
from typing import List
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOPWORDS = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    """
    Lowercase, remove emails/urls/extra chars, normalize whitespace.
    """
    text = text.lower()
    text = re.sub(r'\S+@\S+', ' ', text)      # remove emails
    text = re.sub(r'http\S+|www\.\S+', ' ', text)  # remove urls
    text = re.sub(r'\d{2,}', ' ', text)       # remove long numbers (years left intentionally? we'll extract years separately)
    text = re.sub(r'[^a-zA-Z0-9\s\+\#\.\-]', ' ', text)  # keep hashtags, dots, pluses optionally
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text: str) -> List[str]:
    toks = word_tokenize(text)
    toks = [t for t in toks if t.isalnum()]  # filter punctuation
    toks = [t for t in toks if t not in STOPWORDS]
    return toks

def simple_tokenize(text: str):
    # Simple and reliable tokenizer
    return text.split()


def extract_years_of_experience(text: str) -> int:
    """
    Simple heuristic: find 'X year(s)' patterns or look for 'experience' contexts.
    Returns max years found, or 0 if none
    """
    years = 0
    # find patterns like '3 years', '5+ years', '2-3 years'
    matches = re.findall(r'(\d+)\s*\+?\s*-\s*(\d+)\s*years|(\d+)\s*\+?\s*years|(\d+)\s*years', text)
    # matches returns tuple groups; flatten and convert
    found = []
    for m in matches:
        for g in m:
            if g and g.isdigit():
                found.append(int(g))
    if found:
        years = max(found)
    else:
        # fallback: search for 'experience: X years' or 'x yrs'
        matches2 = re.findall(r'(\d+)\s*yrs|experience\s*[:\-]?\s*(\d+)\s*years', text)
        for m in matches2:
            for g in m:
                if g and g.isdigit():
                    found.append(int(g))
        if found:
            years = max(found)
    return years
