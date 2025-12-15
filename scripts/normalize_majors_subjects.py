"""Normalize subject names inside the majors dataset.

This script reads ``data/majors.json`` and writes ``data/majors.normalized.json``
with subject keys cleaned via :mod:`major_matcher.subject_normalization`.
"""

from __future__ import annotations

import json
from pathlib import Path

from major_matcher.subject_normalization import normalize_subject, normalize_subject_list

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
INPUT_PATH = DATA_DIR / "majors.json"
OUTPUT_PATH = DATA_DIR / "majors.normalized.json"


def normalize_record(record: dict) -> dict:
    record = dict(record)
    record["required_hs_subjects"] = normalize_subject_list(record.get("required_hs_subjects", []) or [])

    raw_requirements = record.get("min_grade_requirements", {}) or {}
    normalized_requirements = {}
    for key, value in raw_requirements.items():
        normalized_requirements[normalize_subject(key)] = value
    record["min_grade_requirements"] = normalized_requirements
    return record


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"Input file not found: {INPUT_PATH}")

    data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("majors.json is not a list of records")

    normalized = [normalize_record(entry) for entry in data]
    OUTPUT_PATH.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote normalized majors to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
