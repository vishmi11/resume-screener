# src/app.py
import streamlit as st
from extractor import extract_text_from_pdf
from preprocess import clean_text, simple_tokenize, extract_years_of_experience
from skills import SKILLS_DICT, match_skills
import os

# --- Streamlit page config ---
st.set_page_config(page_title="Resume Screener — Demo", layout="wide")
st.title("📄 Resume Screener — PDF Extractor Demo")

# --- File uploader ---
uploaded = st.file_uploader("Upload a resume PDF", type=["pdf"])

if uploaded:
    # Save uploaded PDF temporarily
    tmp_file_path = "tmp_upload.pdf"
    with open(tmp_file_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # --- Extract raw text ---
    raw_text = extract_text_from_pdf(tmp_file_path)
    st.subheader("Raw Extracted Text (first 1500 chars)")
    st.code(raw_text[:1500])

    # --- Clean text ---
    cleaned = clean_text(raw_text)
    st.subheader("Cleaned Text (first 800 chars)")
    st.code(cleaned[:800])

    # --- Tokens preview ---
    st.subheader("Tokens (first 80)")
    st.write(simple_tokenize(cleaned)[:80])

    # --- Years of experience ---
    years = extract_years_of_experience(raw_text)
    st.write(f"Detected years of experience (heuristic): {years}")

    # --- Skill Matching ---
    st.subheader("Skill Matching & Match Scores")
    for role_key in SKILLS_DICT.keys():
        matched, missing, score = match_skills(cleaned, role_key)
        role_name = role_key.replace("_", " ").title()
        st.markdown(f"**{role_name} Match Score:** {score}%")
        st.progress(score / 100)  # progress bar
        st.write("Matched Skills:", matched or "None")
        st.write("Missing Skills:", missing or "None")
        st.write("---")

    # --- Cleanup temporary file ---
    try:
        os.remove(tmp_file_path)
    except:
        pass
