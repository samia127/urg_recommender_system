"""Vectorization and similarity computation utilities."""

from __future__ import annotations

from typing import Dict, List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _row_to_text(row: pd.Series) -> str:
    parts: List[str] = []
    for field in ["major_name", "faculty", "degree_type"]:
        value = row.get(field, "")
        if isinstance(value, str):
            parts.append(value)
    list_fields = [
        "required_hs_subjects",
        "example_career_paths",
        "curriculum_keywords",
        "industry_keywords",
        "learning_style",
    ]
    for field in list_fields:
        value = row.get(field, [])
        if isinstance(value, list):
            parts.extend([str(item) for item in value])
        elif isinstance(value, str):
            parts.append(value)
    return " ".join([part for part in parts if part])


def vectorize_majors(majors_df: pd.DataFrame) -> Dict[str, object]:
    """Create TF-IDF vectors for the majors corpus."""

    text_corpus = majors_df.apply(_row_to_text, axis=1).tolist()
    vectorizer = TfidfVectorizer(stop_words="english")
    majors_matrix = vectorizer.fit_transform(text_corpus)
    return {"vectorizer": vectorizer, "matrix": majors_matrix}


def vectorize_user_profile(user_profile: Dict[str, object], vectorizer: TfidfVectorizer):
    """Vectorize the user profile using the fitted vectorizer."""

    skills = user_profile.get("skills", []) or []
    hobbies = user_profile.get("hobbies", []) or []
    aspiration = user_profile.get("career_aspiration", "")
    combined = " ".join(
        [aspiration] + [" ".join(skills)] + [" ".join(hobbies)] + [str(user_profile.get("grades", ""))]
    )
    return vectorizer.transform([combined])


def compute_similarity_scores(user_vector, majors_matrix, majors_df: pd.DataFrame) -> List[Dict[str, object]]:
    """Compute cosine similarity and return sorted results."""

    similarities = cosine_similarity(user_vector, majors_matrix)[0]
    ranked = []
    for idx, score in enumerate(similarities):
        major_name = majors_df.iloc[idx].get("major_name", f"Major {idx}")
        ranked.append({"major_name": major_name, "score": float(score), "index": idx})
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked
