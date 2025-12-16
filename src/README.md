# 📄 AI-Powered Resume Screener

**AI-Powered Resume Screener** is a web application built with **Streamlit** that allows recruiters or job seekers to quickly analyze resumes. The app extracts text from PDF resumes, cleans it, tokenizes, detects years of experience, and matches skills against predefined job roles using a **skills JSON file**.

---

## 🚀 Features

- Upload a PDF resume and extract text
- Clean and tokenize text for analysis
- Detect years of experience (heuristic)
- Match skills with multiple roles:
  - Data Analyst
  - ML Engineer
  - Frontend Developer
  - Backend Developer
  - Mobile Developer
- Calculate match scores for each role with progress bars
- Fully web-based with interactive Streamlit UI

---

## 🛠️ Tech Stack

- **Python** – core programming and logic  
- **Streamlit** – interactive web UI  
- **Regex** – text cleaning and experience detection  
- **JSON** – skill dictionary for roles  
- **PyPDF2** – PDF text extraction  

---

## 📁 Project Structure
resume-screener/
│── venv/ # Virtual environment (ignored in git)
│── src/
│ ├── app.py # Main Streamlit app
│ ├── extractor.py # PDF text extraction
│ ├── preprocess.py # Text cleaning, tokenization, experience detection
│ └── skills.py # Skill matching functions (loads skills.json)
│── skills.json # Role skill dictionary
│── README.md # Project description
│── .gitignore

1. **Clone the repository**

git clone https://github.com/<your-username>/resume-screener.git
cd resume-screener

Create a virtual environment and activate it
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

Install dependencies

pip install -r requirements.txt
If you don’t have requirements.txt, you can install manually:

pip install streamlit PyPDF2
Run the Streamlit app

streamlit run src/app.py

📷 Screenshots


🔧 How it Works
Upload PDF → text is extracted using PyPDF2

Clean Text → remove punctuation, emails, URLs, lowercase

Tokenize → simple split for analysis

Experience Detection → regex for "X years" patterns

Skill Matching → compares text to skills.json per role

Match Score → percentage + progress bar