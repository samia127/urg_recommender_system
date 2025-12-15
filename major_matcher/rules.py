"""Rule-based refinements and reporting for recommendations."""

from __future__ import annotations

import math
import re
from typing import Dict, List

import pandas as pd

from . import config


'''
def _extract_overall_grade(grade_text: str) -> float | None:
    """Extract a numeric overall grade percentage if present."""

    numbers = re.findall(r"\d+(?:\.\d+)?", grade_text)
    if not numbers:
        return None
    try:
        return float(numbers[0])
    except ValueError:
        return None
'''

def _count_overlaps(user_terms: List[str], target_terms: List[str]) -> int:
    user_lower = {term.lower() for term in user_terms if term}
    target_lower = {term.lower() for term in target_terms if term}
    return len(user_lower & target_lower)


def apply_rules(
    ranked_majors: List[Dict[str, object]],
    user_profile: Dict[str, object],
    majors_df: pd.DataFrame,
    top_n: int = config.RULES_TOP_N,
):
    """Apply simple domain rules to the top ranked majors."""

    trimmed = ranked_majors[:top_n]
    #grade_value = _extract_overall_grade(str(user_profile.get("grades", "")))
    grade_value = user_profile.get("overall_grade")

    career_text = str(user_profile.get("career_aspiration", "")).lower()
    user_skills = user_profile.get("skills", []) or []

    adjusted = []
    for entry in trimmed:
        idx = entry["index"]
        score = entry["score"]
        row = majors_df.iloc[idx]

        min_grade = row.get("min_overall_percentage (%)")
        if isinstance(min_grade, (int, float)) and not math.isnan(min_grade) and grade_value is not None:
            if grade_value < float(min_grade):
                score *= config.GRADE_PENALTY_FACTOR

        career_hits = 0
        for field in ["example_career_paths", "industry_keywords"]:
            options = row.get(field, [])
            if isinstance(options, list):
                career_hits += sum(1 for option in options if str(option).lower() in career_text)
        if career_hits:
            score *= config.CAREER_BOOST_FACTOR

        overlap_sources = []
        for field in ["curriculum_keywords", "learning_style", "required_hs_subjects"]:
            value = row.get(field, [])
            if isinstance(value, list):
                overlap_sources.extend([str(item) for item in value])
        overlap_count = _count_overlaps(user_skills, overlap_sources)
        if overlap_count >= config.SKILL_OVERLAP_THRESHOLD:
            score *= config.SKILL_BOOST_FACTOR

        adjusted.append(
            {
                "major_name": entry["major_name"],
                "score": score,
                "index": idx,
                "skill_overlap": overlap_count,
                "career_hits": career_hits,
            }
        )

    adjusted.sort(key=lambda item: item["score"], reverse=True)
    return adjusted


def build_reason(entry: Dict[str, object], user_profile: Dict[str, object], majors_df: pd.DataFrame) -> str:
    """Craft a short explanation for why a major was suggested."""

    idx = entry.get("index")
    row = majors_df.iloc[idx] if idx is not None and not majors_df.empty else {}
    matched_skills = entry.get("skill_overlap", 0)
    career_hits = entry.get("career_hits", 0)

    highlights = []
    if matched_skills:
        highlights.append(
            f"Matched {matched_skills} of your skills with the major's curriculum"
        )
    if career_hits:
        highlights.append("Career aspiration closely aligns with example paths")
    if isinstance(row, pd.Series):
        subjects = row.get("required_hs_subjects", [])
        if subjects:
            highlights.append(f"Key subjects: {', '.join(subjects)}")

    if not highlights:
        highlights.append("Strong textual similarity to your interests and profile")

    return "; ".join(highlights)


def generate_recommendation_report(
    top_major: Dict[str, object],
    user_profile: Dict[str, object],
    all_ranked_majors: List[Dict[str, object]],
):
    """Create a human-readable report summarizing the recommendation."""

    if not top_major:
        return "No recommendation could be generated. Please provide more details.", {}

    alternatives = [entry for entry in all_ranked_majors[1:6]]
    top_score = top_major.get("score", 0.0)
    max_score = all_ranked_majors[0].get("score", 1.0) if all_ranked_majors else top_score
    confidence = 0 if max_score == 0 else min(int((top_score / max_score) * 100), 100)

    reasons = [
        f"Career aspiration match: {user_profile.get('career_aspiration', 'N/A')}",
        f"Skills highlighted: {', '.join(user_profile.get('skills', [])) or 'N/A'}",
        f"Hobbies considered: {', '.join(user_profile.get('hobbies', [])) or 'N/A'}",
    ]

    report_lines = [
        f"Top Recommended Major: {top_major.get('major_name', 'Unknown')}",
        f"Confidence: {confidence}%",
        "Reasons:",
        *[f"- {reason}" for reason in reasons],
        "\nAlternative Majors (next best matches):",
        *[f"- {alt['major_name']} (score: {alt['score']:.3f})" for alt in alternatives],
    ]

    return "\n".join(report_lines), {
        "top_major": top_major,
        "alternatives": alternatives,
        "confidence": confidence,
    }


__all__ = ["apply_rules", "generate_recommendation_report", "build_reason"]
