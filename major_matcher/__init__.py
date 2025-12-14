"""Utility package for the MajorMatch recommender demo."""

from .data import load_context, load_majors_data
from .user_profile import collect_user_input
from .similarity import vectorize_majors, vectorize_user_profile, compute_similarity_scores
from .rules import apply_rules, generate_recommendation_report

__all__ = [
    "load_context",
    "load_majors_data",
    "collect_user_input",
    "vectorize_majors",
    "vectorize_user_profile",
    "compute_similarity_scores",
    "apply_rules",
    "generate_recommendation_report",
]
