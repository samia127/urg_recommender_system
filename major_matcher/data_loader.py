"""Data loading and preprocessing utilities for MajorMatch."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd

from . import config

SectionData = Dict[str, Iterable[str]]


def _clean_line(line: str) -> str:
    """Normalize bullet points and whitespace."""
    cleaned = re.sub(r"^[\s\-•·\d\.]+", "", line).strip()
    return cleaned


def _extract_section(lines: List[str], start_marker: str, stop_markers: Tuple[str, ...]) -> List[str]:
    """Collect lines between markers, cleaning out empties."""
    collected: List[str] = []
    active = False
    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith(start_marker):
            active = True
            continue
        if active and any(stripped.startswith(marker) for marker in stop_markers):
            break
        if active:
            cleaned = _clean_line(raw)
            if cleaned:
                collected.append(cleaned)
    return collected


def load_majors_data(json_path: str | Path | None = None) -> pd.DataFrame:
    """Load the majors JSON into a DataFrame, handling edge cases gracefully."""

    path = Path(json_path) if json_path else config.MAJORS_PATH
    if not path.exists():
        # Fallback to default location if a custom path was provided but missing
        if json_path:
            path = config.MAJORS_PATH
        if not path.exists():
            return pd.DataFrame()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return pd.DataFrame()

    if not isinstance(data, list):
        return pd.DataFrame()

    frame = pd.DataFrame(data)
    expected_list_fields = [
        "required_hs_subjects",
        "example_career_paths",
        "curriculum_keywords",
        "industry_keywords",
        "learning_style",
    ]
    for field in expected_list_fields:
        if field not in frame.columns:
            frame[field] = [[] for _ in range(len(frame))]
        else:
            frame[field] = frame[field].apply(lambda v: v if isinstance(v, list) else [])

    # Ensure text-friendly columns exist for later concatenation
    for field in ["major_name", "faculty", "degree_type"]:
        if field not in frame.columns:
            frame[field] = ""
        frame[field] = frame[field].fillna("")

    numeric_fields = ["min_overall_percentage (%)"]
    for field in numeric_fields:
        if field in frame.columns:
            frame[field] = pd.to_numeric(frame[field], errors="coerce")
        else:
            frame[field] = float("nan")

    return frame


def load_context(txt_path: str | Path | None = None) -> Dict[str, object]:
    """Parse the free-form context text file into structured pieces.

    Returns a dictionary containing:
        grade_scale: str
        skills: List[str]
        hobbies: List[str]
        career_aspirations: List[str]
    """

    path = Path(txt_path) if txt_path else config.CONTEXT_PATH
    if not path.exists():
        if txt_path:
            path = config.CONTEXT_PATH
        if not path.exists():
            return {
                "grade_scale": "",
                "skills": [],
                "hobbies": [],
                "career_aspirations": [],
            }

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    grade_lines = _extract_section(lines, "1.", ("2.", "3.", "4."))
    skills_lines = _extract_section(lines, "2.", ("3.", "4."))
    hobby_lines = _extract_section(lines, "3.", ("4.",))
    career_lines = _extract_section(lines, "4.", tuple())

    def _filter_entries(entries: List[str]) -> List[str]:
        cleaned: List[str] = []
        for entry in entries:
            if not entry or "?" in entry or entry.endswith(":"):
                continue
            cleaned.append(entry)
        return cleaned

    return {
        "grade_scale": " ".join(grade_lines).strip(),
        "skills": _filter_entries(skills_lines),
        "hobbies": _filter_entries(hobby_lines),
        "career_aspirations": _filter_entries(career_lines),
    }


__all__ = ["load_majors_data", "load_context"]
