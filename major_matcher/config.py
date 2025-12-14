"""Configuration constants for the MajorMatch recommender package."""

from __future__ import annotations

from pathlib import Path

# Base directory for the repository/package
BASE_DIR = Path(__file__).resolve().parent.parent

# Data locations
DATA_DIR = BASE_DIR / "data"
MAJORS_PATH = DATA_DIR / "majors.json"
CONTEXT_PATH = DATA_DIR / "context.txt"

# Recommendation settings
RULES_TOP_N = 10
RETURN_TOP_K = 4
SKILL_OVERLAP_THRESHOLD = 2
GRADE_PENALTY_FACTOR = 0.75
CAREER_BOOST_FACTOR = 1.15
SKILL_BOOST_FACTOR = 1.10

__all__ = [
    "BASE_DIR",
    "DATA_DIR",
    "MAJORS_PATH",
    "CONTEXT_PATH",
    "RULES_TOP_N",
    "RETURN_TOP_K",
    "SKILL_OVERLAP_THRESHOLD",
    "GRADE_PENALTY_FACTOR",
    "CAREER_BOOST_FACTOR",
    "SKILL_BOOST_FACTOR",
]
