"""Normalize subject names to stable canonical labels."""

from __future__ import annotations

import re
from typing import Dict

SUBJECT_MAP: Dict[str, str] = {
    # mathematics variants
    "advanced maths": "mathematics",
    "advanced math": "mathematics",
    "core maths": "mathematics",
    "core math": "mathematics",
    "pure mathematics": "mathematics",
    "pure maths": "mathematics",
    "maths": "mathematics",
    "math": "mathematics",
    "mathematics": "mathematics",
    # english variants
    "english language": "english",
    "core english language": "english",
    "english": "english",
    # sciences
    "physics": "physics",
    "chemistry": "chemistry",
    "biology": "biology",
    "science": "science",
    # computing / tech
    "computer science": "computer science",
    "cs": "computer science",
    "ict": "computer science",
    "it": "computer science",
    "software engineering": "software engineering",
    "se": "software engineering",
    "information systems": "information systems",
    "is": "information systems",
    "mis": "management information systems",
    # language / humanities
    "arabic": "arabic",
    "english literature": "english",
    "islamic studies": "islamic studies",
    "islam": "islamic studies",
    "social studies": "social studies",
    "social": "social studies",
    "history": "history",
    "geography": "geography",
    # arts / others
    "arts": "arts",
    "art": "arts",
    "music": "music",
    "physical education": "physical education",
    "pe": "physical education",
    "physical ed": "physical education",
    "physical-education": "physical education",
}


def normalize_subject(s: str) -> str:
    if not isinstance(s, str):
        return s
    cleaned = re.sub(r"\s+", " ", s.strip()).lower()
    return SUBJECT_MAP.get(cleaned, cleaned)


def normalize_subject_list(lst):
    if not isinstance(lst, list):
        return lst
    return [normalize_subject(x) for x in lst]


__all__ = ["normalize_subject", "normalize_subject_list", "SUBJECT_MAP"]
