# src/app.py
import streamlit as st
import joblib
import os

from extractor import extract_text_from_pdf
from preprocess import clean_text, simple_tokenize, extract_years_of_experience
from skills import SKILLS_DICT, match_skills
from explain import get_top_keywords

# ----------------- Page Config -----------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("📄 AI-Powered Resume Screener")

# ----------------- Load ML Model -----------------
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "resume_role_model.pkl")
    vectorizer_path = os.path.join(base_dir, "tfidf_vectorizer.pkl")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

model, vectorizer = load_model()

# ----------------- Helper Functions -----------------
def render_skills(matched, missing):
    matched_html = " ".join([f"<span style='color:green; font-weight:bold'>{s.title()}</span>" for s in matched])
    missing_html = " ".join([f"<span style='color:red; font-weight:bold'>{s.title()}</span>" for s in missing])
    st.markdown(f"✅ Matched Skills: {matched_html}", unsafe_allow_html=True)
    st.markdown(f"❌ Missing Skills: {missing_html}", unsafe_allow_html=True)

def render_keywords(keywords):
    for word in keywords:
        st.markdown(f"<span style='background-color:#FFD700; padding:3px 6px; margin:2px; border-radius:4px'>{word}</span>", unsafe_allow_html=True)

def render_improvement_skills(skills):
    for skill in skills:
        st.markdown(f"<span style='background-color:#87CEFA; padding:4px; border-radius:5px; margin:2px'>{skill.title()}</span>", unsafe_allow_html=True)

# ----------------- Upload Resume -----------------
uploaded = st.file_uploader("Upload a resume (PDF)", type=["pdf"])

if uploaded:
    tmp_path = "tmp_resume.pdf"
    with open(tmp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # Extract & Clean
    raw_text = extract_text_from_pdf(tmp_path)
    cleaned = clean_text(raw_text)

    # ----------------- Columns Layout -----------------
    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader("📄 Cleaned Resume Text (first 1000 chars)")
        st.code(cleaned[:1000])
        st.write("Tokens (first 80):")
        st.write(simple_tokenize(cleaned)[:80])

    with col2:
        st.subheader("📊 Resume Insights")
        st.write("Detected years of experience:", extract_years_of_experience(raw_text))

    # ----------------- ML Prediction -----------------
    X_vec = vectorizer.transform([cleaned])
    probs = model.predict_proba(X_vec)[0]
    roles = model.classes_
    role_probs = sorted(zip(roles, probs), key=lambda x: x[1], reverse=True)

    st.subheader("🎯 Top Role Predictions & Hybrid Confidence")
    alpha = 0.6
    hybrid_scores = {}

    for role, ml_prob in role_probs[:3]:
        matched, missing, skill_score = match_skills(cleaned, role)
        hybrid_conf = alpha * ml_prob + (1 - alpha) * (skill_score / 100)
        hybrid_scores[role] = hybrid_conf

        st.markdown(f"**{role.replace('_', ' ').title()}**")
        st.progress(int(hybrid_conf * 100))
        render_skills(matched, missing)
        st.write("---")

    top_role = max(hybrid_scores, key=hybrid_scores.get)
    _, missing_skills_top, _ = match_skills(cleaned, top_role)

    # ----------------- Resume Improvement Suggestions -----------------
    st.subheader(f"💡 Resume Improvement Suggestions for {top_role.replace('_',' ').title()}")
    if missing_skills_top:
        render_improvement_skills(missing_skills_top)
    else:
        st.write("🎉 Your resume already covers all key skills!")

    # ----------------- Explainability -----------------
    st.subheader(f"🧠 Why '{top_role.replace('_',' ').title()}'?")
    top_keywords = get_top_keywords(cleaned, model, vectorizer)
    if top_keywords:
        render_keywords(top_keywords)
    else:
        st.write("No strong keywords detected.")

    # ----------------- Skill Match Breakdown -----------------
    st.subheader("🛠️ Skill Match Breakdown")
    for role_key in SKILLS_DICT.keys():
        matched, missing, score = match_skills(cleaned, role_key)
        role_title = role_key.replace("_", " ").title()
        with st.expander(f"{role_title} — Match Score: {score:.2f}%"):
            render_skills(matched, missing)

    # ----------------- Debug Section -----------------
    with st.expander("🔍 View Extracted Text (Debug)"):
        st.code(raw_text[:1500])

    # Cleanup
    try:
        os.remove(tmp_path)
    except:
        pass
