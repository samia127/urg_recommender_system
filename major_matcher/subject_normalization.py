import re

SUBJECT_MAP = {
    # math variants
    "advanced maths": "Mathematics",
    "advanced math": "Mathematics",
    "core maths": "Mathematics",
    "core math": "Mathematics",
    "pure mathematics": "Mathematics",
    "pure maths": "Mathematics",
    "mathematics": "Mathematics",
    "maths": "Mathematics",
    "math": "Mathematics",

    # english variants (optional)
    "core english language": "English",
    "english language": "English",
    "english": "English",
}

def normalize_subject(s: str) -> str:
    if not isinstance(s, str):
        return s
    cleaned = re.sub(r"\s+", " ", s.strip()).lower()
    return SUBJECT_MAP.get(cleaned, s.strip())

def normalize_subject_list(lst):
    if not isinstance(lst, list):
        return lst
    return [normalize_subject(x) for x in lst]
