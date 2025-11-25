# SHL Recommendation System

This project is a recommendation engine designed to help hiring teams find the most suitable assessments from the SHL catalog. Using input such as job descriptions, skills or role requirements, the system matches those to assessments that best fit the criteria — so recruiters can make faster, smarter decisions.

---

## Why this project?

In many organisations, selecting the right assessment for a job role can be cumbersome. There are many tests, varying durations, and different skill-areas to cover. The SHL Recommendation System was built to simplify that process: given your role, required skills and time constraints, it suggests assessments aligned with your needs.  
As someone passionate about AI/ML and full-stack development, I developed this system to bring machine intelligence into the assessment selection workflow.

---

## What it does

- Accepts user input in the form of a job description text, role profile or skills list.  
- Parses and understands the key requirements (skills, duration, test type).  
- Searches a database or catalogue of SHL assessments for matches based on content, duration, and skill coverage.  
- Ranks and returns a list of recommended assessments, with link(s), duration and key details.  
- Provides a minimal web app interface to input and review the results.

---

## Tech stack

- **Language:** Python  
- **Web Framework:** Flask / FastAPI (depending on your version) for the frontend input & output  
- **Data Handling & ML:** Pandas, NumPy, Scikit-learn (or similar) for preprocessing and matching  
- **Natural Language Processing:** (If implemented) libraries such as spaCy, NLTK or transformer models to extract features from text  
- **Database / Data Storage:** A lightweight format (CSV/SQLite) for the assessment catalogue  
- **Frontend UI:** HTML/CSS/JavaScript for user interaction (optionally Bootstrap)  
- **Deployment:** Local or cloud (Heroku / AWS / GCP) as a web service  

---

## Project structure

```text
SHL-Recommendation/
├── app.py                # Entry point for the web application
├── recommendation.py     # Core logic: parse input, match assessments, rank output
├── catalog.csv           # Catalogue of SHL assessments with metadata (skills, duration, etc.)
├── templates/            # HTML templates for UI (input form + results display)
│   ├── index.html
│   └── result.html
├── static/               # CSS, JS, images (if any)
└── README.md             # This file
