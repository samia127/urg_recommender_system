"""Helpers for preparing user data coming from web forms or APIs."""

from __future__ import annotations

from typing import Dict, List


def _combine_entries(selected: List[str] | None, custom: List[str] | None) -> List[str]:
    combined: List[str] = []
    for source in (selected or [], custom or []):
        if isinstance(source, list):
            combined.extend([item.strip() for item in source if item and item.strip()])
    return combined


'''def normalize_user_data(form_data: Dict[str, object]) -> Dict[str, object]:
    """Normalize raw form data into the structure expected by the recommender."""

    grades = form_data.get("grades", {})
    if isinstance(grades, dict):
        grades_text = "; ".join(f"{k}: {v}" for k, v in grades.items() if v)
    else:
        grades_text = str(grades)

    skills = _combine_entries(form_data.get("skills"), form_data.get("custom_skills"))
    hobbies = _combine_entries(form_data.get("hobbies"), form_data.get("custom_hobbies"))

    return {
        "grades": grades_text,
        "career_aspiration": str(form_data.get("career_aspiration", "")).strip(),
        "skills": skills,
        "hobbies": hobbies,
    }'''

def normalize_user_data(form_data):
    grades = form_data.get("grades", {})
    overall = None

    if isinstance(grades, dict):
        overall = grades.get("overall")
        grades_text = "; ".join(f"{k}: {v}" for k, v in grades.items() if v)
    else:
        grades_text = str(grades)

    skills = _combine_entries(form_data.get("skills"), form_data.get("custom_skills"))
    hobbies = _combine_entries(form_data.get("hobbies"), form_data.get("custom_hobbies"))

    return {
        "grades": grades_text,
        "overall_grade": float(overall) if overall not in (None, "") else None,
        "career_aspiration": str(form_data.get("career_aspiration", "")).strip(),
        "skills": skills,
        "hobbies": hobbies,
    }



__all__ = ["normalize_user_data"]
