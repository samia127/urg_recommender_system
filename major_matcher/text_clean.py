"""Shared text preprocessing utilities for the recommender."""

from __future__ import annotations

import re
from typing import Iterable, List, Set

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

ACRONYM_MAP = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "it": "information technology",
    "cs": "computer science",
    "se": "software engineering",
    "is": "information systems",
    "mis": "management information systems",
    "ee": "electrical engineering",
    "ce": "civil engineering",
    "me": "mechanical engineering",
    "che": "chemical engineering",
    "ie": "industrial engineering",
    "hr": "human resources",
    "pr": "public relations",
    "ux": "user experience",
    "ui": "user interface",
    "qa": "quality assurance",
    "gis": "geographic information systems",
    "bim": "building information modeling",
    "cad": "computer aided design",
    "fintech": "financial technology",
    "edtech": "education technology",
    "biotech": "biotechnology",
}

PUNCT_PATTERN = re.compile(r"[^a-z\s]")
SEPARATOR_PATTERN = re.compile(r"[\/_-]+")
WHITESPACE_PATTERN = re.compile(r"\s+")


def _expand_acronyms(text: str) -> str:
    def replacer(match: re.Match[str]) -> str:
        key = match.group(0).lower()
        return ACRONYM_MAP.get(key, key)

    pattern = re.compile(r"\b(" + "|".join(map(re.escape, ACRONYM_MAP.keys())) + r")\b", re.IGNORECASE)
    return pattern.sub(replacer, text)


def clean_text(text: str) -> str:
    """Normalize text for similarity: lowercase, expand acronyms, strip punctuation."""

    if not isinstance(text, str):
        return ""

    lowered = text.lower()
    expanded = _expand_acronyms(lowered)
    separators_normalized = SEPARATOR_PATTERN.sub(" ", expanded)
    no_punct = PUNCT_PATTERN.sub(" ", separators_normalized)
    collapsed = WHITESPACE_PATTERN.sub(" ", no_punct).strip()
    return collapsed


def tokenize(text: str, *, drop_stopwords: bool = True) -> List[str]:
    cleaned = clean_text(text)
    tokens = cleaned.split()
    if drop_stopwords:
        stopwords: Set[str] = set(ENGLISH_STOP_WORDS)
        tokens = [tok for tok in tokens if tok not in stopwords]
    return tokens


def combine_and_clean(parts: Iterable[str]) -> str:
    cleaned_parts = [clean_text(part) for part in parts if part]
    return " ".join(part for part in cleaned_parts if part)


__all__ = ["clean_text", "tokenize", "combine_and_clean", "ACRONYM_MAP"]
