# SkillSync AI — Intelligent Skill Gap Analyzer

A production-quality NLP web application that maps your current skills against a target role, identifies gaps, and generates a personalized learning roadmap.

---

## Features

- TF-IDF + cosine similarity skill matching
- Weighted match scoring per role requirements
- Readiness score adjusted for experience level
- Prioritized learning roadmap with resources and timelines
- Interactive radar chart, gauge, and bar visualizations
- Light / Dark theme toggle
- Downloadable text report

---

## Setup

### 1. Clone or extract the project

```bash
cd SkillSync_AI
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The application opens at `http://localhost:8501`

---

## Project Structure

```
SkillSync_AI/
├── app.py                   # Main Streamlit application
├── requirements.txt
├── README.md
├── assets/                  # Static assets (favicon, etc.)
├── data/
│   ├── __init__.py
│   └── roles_skills.py      # Role definitions, required skills, weights, learning paths
├── utils/
│   ├── __init__.py
│   ├── nlp_engine.py        # TF-IDF, cosine similarity, scoring, roadmap logic
│   └── report.py            # Text report generator
└── models/                  # Reserved for future model artifacts
```

---

## Supported Roles

- Data Scientist
- Machine Learning Engineer
- Full Stack Developer
- DevOps Engineer
- Product Manager
- Cybersecurity Analyst
- Cloud Architect
- Data Engineer

---

## Tech Stack

| Component         | Technology                          |
|------------------|-------------------------------------|
| UI Framework      | Streamlit                           |
| NLP / Similarity  | TF-IDF Vectorizer + Cosine Similarity (scikit-learn) |
| Data Processing   | Pandas, NumPy                       |
| Visualizations    | Plotly                              |
| Fonts             | Playfair Display, Inter (Google Fonts) |

---

## Configuration

All role data, skill weights, and learning paths are defined in `data/roles_skills.py`. To add a new role, follow the existing structure:

```python
"New Role": {
    "required_skills": [...],
    "weights": {skill: importance_1_to_10, ...},
    "learning_paths": {
        skill: {"resource": "...", "duration": "N weeks", "priority": "Critical|High|Medium|Low"}
    }
}
```
