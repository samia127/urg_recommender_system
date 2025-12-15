"""Helpers for preparing user data coming from web forms or APIs."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Dict, List, Optional

from .data_loader import load_context
from .subject_normalization import normalize_subject
from .text_clean import clean_text


def _combine_entries(selected: List[str] | None, custom: List[str] | None) -> List[str]:
    combined: List[str] = []
    for source in (selected or [], custom or []):
        if isinstance(source, list):
            combined.extend([item.strip() for item in source if item and item.strip()])
    return combined


@lru_cache(maxsize=1)
def _context_terms() -> Dict[str, set]:
    context = load_context()
    return {
        "skills": {item.lower() for item in context.get("skills", [])},
        "hobbies": {item.lower() for item in context.get("hobbies", [])},
    }


def _normalize_entries(entries: List[str], kind: str) -> List[str]:
    canon = _context_terms().get(kind, set())
    normalized: List[str] = []
    for entry in entries:
        cleaned = clean_text(entry)
        if not cleaned:
            continue
        if cleaned in canon:
            normalized.append(next(item for item in canon if item == cleaned))
        else:
            normalized.append(cleaned)
    return normalized


def _parse_grade(value) -> Optional[float]:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        pass
    if isinstance(value, str):
        match = re.search(r"\d+(?:\.\d+)?", value)
        if match:
            try:
                return float(match.group(0))
            except ValueError:
                return None
    return None


def normalize_user_data(form_data: Dict[str, object]) -> Dict[str, object]:
    grades_input = form_data.get("grades", {})
    normalized_grades: Dict[str, Optional[float]] = {}
    overall = None

    if isinstance(grades_input, dict):
        overall = _parse_grade(grades_input.get("overall"))
        for key, value in grades_input.items():
            if key == "overall":
                continue
            normalized_key = normalize_subject(key)
            parsed = _parse_grade(value)
            normalized_grades[normalized_key] = parsed

    skills = _normalize_entries(
        _combine_entries(form_data.get("skills"), form_data.get("custom_skills")),
        "skills",
    )
    hobbies = _normalize_entries(
        _combine_entries(form_data.get("hobbies"), form_data.get("custom_hobbies")),
        "hobbies",
    )

    raw_career = str(form_data.get("career_aspiration", "")).strip()

    return {
        "grades": normalized_grades,
        "grades_text": "; ".join(
            f"{k}: {v}" for k, v in normalized_grades.items() if v is not None
        ),
        "overall_grade": overall,
        "career_aspiration": clean_text(raw_career).strip(),
        "career_aspiration_text": raw_career,
        "skills": skills,
        "hobbies": hobbies,
        "stream": str(form_data.get("stream", "")).strip().lower() or None,
    }


__all__ = ["normalize_user_data"]
