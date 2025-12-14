# MajorMatch Recommendation System

A lightweight recommendation engine to match students with university majors using TF-IDF similarity plus rule-based adjustments. The project now ships as a Python package with a minimal backend and a simple HTML questionnaire for local testing.

## Repository contents
- `data/majors.json`: data for 25 majors (name, keywords, requirements, example career paths).
- `data/context.txt`: background text describing the Omani grading context plus skills, hobbies, and career examples.
- `major_matcher/`: Python package for loading data, computing similarity, applying rules, and generating recommendations.
- `backend/app.py`: Flask server exposing `POST /api/recommend` for browser clients.
- `frontend/questionnaire.html`: Collects grades, skills, hobbies, and career aspirations then calls the backend.
- `frontend/recommendations.html`: Displays the latest recommendations saved from the questionnaire page.
- `major_recommender_main.ipynb` and `major_recommender_testing.ipynb`: Original Colab-friendly notebooks for exploration and testing.

## Quickstart
1. Install dependencies: `pip install -r requirements.txt`.
2. From the project root, start the backend: `python backend/app.py` (runs on port 5000).
3. Open `frontend/questionnaire.html` in your browser (file:// or a simple static server).
4. Fill in grades, skills, hobbies, and career aspiration, then submit. The page will POST to `http://localhost:5000/api/recommend` and render results inline. It also stores the response so `frontend/recommendations.html` can present the same results.

## Python package usage
```python
from major_matcher import recommend, normalize_user_data

raw_form = {
    "grades": {"english": "85", "mathematics": "90"},
    "career_aspiration": "software engineer in fintech",
    "skills": ["Problem Solving", "Digital Literacy / Technology Skills"],
    "hobbies": ["Coding"],
}
user_profile = normalize_user_data(raw_form)
recommendations = recommend(user_profile)
```

## Notes
- Data paths are relative to the repository root; ensure `data/majors.json` and `data/context.txt` remain in place.
- Rule weights and thresholds live in `major_matcher/config.py` and can be tuned as needed.
