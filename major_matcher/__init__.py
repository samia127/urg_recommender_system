"""Utility package for the MajorMatch recommender demo."""

from .config import *
from .data_loader import load_context, load_majors_data
from .recommender import recommend
from .similarity import compute_similarity_scores, vectorize_majors, vectorize_user_profile
from .user_profile import normalize_user_data
from .rules import apply_rules, generate_recommendation_report, build_reason

__all__ = [
    "recommend",
    "normalize_user_data",
    "load_context",
    "load_majors_data",
    "vectorize_majors",
    "vectorize_user_profile",
    "compute_similarity_scores",
    "apply_rules",
    "generate_recommendation_report",
    "build_reason",
] + [name for name in dir() if name.isupper()]
