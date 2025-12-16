AI-Powered Resume Screener

Interactive web app that analyzes PDF resumes, predicts suitable roles, and provides skill matching insights.

🚀 Features

Upload a PDF resume and extract text using PyPDF2.

Clean and preprocess text with NLTK for analysis.

Predict the most suitable role using a trained ML model (Data Analyst, ML Engineer, Frontend, Backend, Mobile).

Hybrid confidence score combining ML prediction + skill matching.

Skill match breakdown: matched skills & missing skills.

Resume improvement suggestions for top predicted role.

Explainable AI: shows top keywords influencing the prediction.

Built with Python and Streamlit for a simple interactive UI.

🎯 Supported Roles

Data Analyst

ML Engineer

Frontend Developer

Backend Developer

Mobile Developer

Other roles are currently not implemented.

🛠️ Tech Stack

Python

Streamlit

Scikit-learn

NLTK

PyPDF2

TF-IDF vectorization

NLP preprocessing

📈 Demo

Live demo available here:
Open in Browser

💻 Installation / Run Locally
# Clone the repo
git clone https://github.com/vishmi11/resume-screener.git
cd resume-screener

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/app.py

📄 Usage

Upload a PDF resume.

View raw & cleaned text.

Check predicted role & hybrid confidence.

Explore skill match breakdown & suggestions.

View top keywords influencing prediction.

🔗 Links

GitHub Repository: https://github.com/vishmi11/resume-screener

Live Demo: https://resume-screener-umvdg9bzxyya8iwb6gys9t.streamlit.app
