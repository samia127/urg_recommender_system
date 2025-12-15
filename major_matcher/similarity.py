"""Vectorization and similarity computation utilities."""

from __future__ import annotations

from typing import Dict, List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .text_clean import clean_text, combine_and_clean


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
    return combine_and_clean(parts)


def vectorize_majors(majors_df: pd.DataFrame) -> Dict[str, object]:
    """Create TF-IDF vectors for the majors corpus."""

    if majors_df.empty:
        return {"vectorizer": TfidfVectorizer(stop_words="english", ngram_range=(1, 2)), "matrix": None}

    text_corpus = majors_df.apply(_row_to_text, axis=1).tolist()
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    majors_matrix = vectorizer.fit_transform(text_corpus)
    return {"vectorizer": vectorizer, "matrix": majors_matrix}


def vectorize_user_profile(user_profile: Dict[str, object], vectorizer: TfidfVectorizer):
    """Vectorize the user profile using the fitted vectorizer."""

    skills = user_profile.get("skills", []) or []
    hobbies = user_profile.get("hobbies", []) or []
    aspiration = user_profile.get("career_aspiration", "")
    stream = user_profile.get("stream") or ""

    combined_text = combine_and_clean([
        aspiration,
        " ".join(skills),
        " ".join(hobbies),
        stream,
    ])

    return vectorizer.transform([combined_text]) if combined_text else vectorizer.transform([""])


def compute_similarity_scores(user_vector, majors_matrix, majors_df: pd.DataFrame) -> List[Dict[str, object]]:
    """Compute cosine similarity and return sorted results."""

    if majors_matrix is None or majors_df.empty:
        return []

    similarities = cosine_similarity(user_vector, majors_matrix)[0]
    ranked = []
    for idx, score in enumerate(similarities):
        major_name = majors_df.iloc[idx].get("major_name", f"Major {idx}")
        ranked.append({"major_name": major_name, "score": float(score), "index": idx})
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked


__all__ = ["vectorize_majors", "vectorize_user_profile", "compute_similarity_scores"]
