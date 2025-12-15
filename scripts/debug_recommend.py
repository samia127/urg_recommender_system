"""Quick debug helper to run sample recommendations."""

from __future__ import annotations

from pprint import pprint

from major_matcher import recommend, normalize_user_data


SCIENCE_SAMPLE = {
    "stream": "science",
    "grades": {
        "maths": "92",
        "english": "85",
        "physics": "88",
        "chemistry": "90",
        "islam": "78",
        "arabic": "80",
        "social": "75",
        "biology": "86",
        "arts": "70",
        "music": "65",
        "physical_education": "72",
        "overall": "88",
    },
    "career_aspiration": "software engineering or data analytics",
    "skills": ["problem solving", "teamwork"],
    "custom_skills": ["AI", "ML"],
    "hobbies": ["coding", "reading"],
    "custom_hobbies": [],
}


LITERARY_SAMPLE = {
    "stream": "literary",
    "grades": {
        "maths": "80",
        "english": "90",
        "islam": "82",
        "arabic": "88",
        "social": "85",
        "arts": "91",
        "music": "76",
        "physical_education": "80",
        "overall": "86",
    },
    "career_aspiration": "journalism and public relations",
    "skills": ["communication", "creativity"],
    "custom_skills": [],
    "hobbies": ["writing", "photography"],
    "custom_hobbies": ["blogging"],
}


def run_sample(payload):
    normalized = normalize_user_data(payload)
    results = recommend(normalized)
    pprint(results)


if __name__ == "__main__":
    print("Science stream sample:")
    run_sample(SCIENCE_SAMPLE)

    print("\nLiterary stream sample:")
    run_sample(LITERARY_SAMPLE)
