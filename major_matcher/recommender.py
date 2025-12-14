"""Public recommender entry point for MajorMatch."""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, List

from . import config
from .data_loader import load_context, load_majors_data
from .rules import apply_rules, build_reason
from .similarity import compute_similarity_scores, vectorize_majors, vectorize_user_profile

UserData = Dict[str, object]


def _ensure_resources():
    majors_df, context, vectors = _cached_resources()
    if majors_df.empty:
        raise ValueError("Majors data could not be loaded. Ensure data/majors.json exists.")
    return majors_df, context, vectors


@lru_cache(maxsize=1)
def _cached_resources():
    majors_df = load_majors_data()
    context = load_context()
    vectors = vectorize_majors(majors_df)
    return majors_df, context, vectors


def recommend(user_data: UserData) -> List[Dict[str, object]]:
    """Return ordered recommendations for the supplied user profile.

    Args:
        user_data: Dict with keys "grades" (dict or str), "career_aspiration",
            "skills" (list[str]), and "hobbies" (list[str]).

    Returns:
        List of recommendation dicts: {"major_name": str, "score": float, "reason": str}
    """

    majors_df, _context, vectors = _ensure_resources()

    user_vector = vectorize_user_profile(user_data, vectors["vectorizer"])
    ranked = compute_similarity_scores(user_vector, vectors["matrix"], majors_df)
    if not ranked:
        return []

    adjusted = apply_rules(ranked, user_data, majors_df, top_n=config.RULES_TOP_N)

    results: List[Dict[str, object]] = []
    for entry in adjusted[: config.RETURN_TOP_K]:
        reason = build_reason(entry, user_data, majors_df)
        results.append(
            {
                "major_name": entry["major_name"],
                "score": float(entry["score"]),
                "reason": reason,
            }
        )

    return results


__all__ = ["recommend"]
