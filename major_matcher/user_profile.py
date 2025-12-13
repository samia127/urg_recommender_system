"""User input helpers designed for Google Colab text workflows."""

from __future__ import annotations

from typing import Dict, List


def _select_from_options(options: List[str], prompt: str) -> List[str]:
    if not options:
        return []

    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"[{idx}] {option}")

    selection = input("Enter comma-separated numbers (or leave blank): ").strip()
    chosen: List[str] = []
    if selection:
        tokens = [token.strip() for token in selection.split(",") if token.strip()]
        for token in tokens:
            if token.isdigit():
                number = int(token)
                if 1 <= number <= len(options):
                    chosen.append(options[number - 1])
                else:
                    print(f"Ignoring invalid choice: {token}")
            else:
                print(f"Ignoring invalid token: {token}")

    custom = input("Add any custom entries (comma-separated, optional): ").strip()
    if custom:
        chosen.extend([item.strip() for item in custom.split(",") if item.strip()])

    return chosen


def collect_user_input(skills: List[str] | None = None, hobbies: List[str] | None = None) -> Dict[str, object]:
    """Collect user information in a notebook-friendly way."""

    print("Please provide your academic grades (e.g., 'Overall 85% | Math 90 | English 88').")
    grades = input("Academic grades: ").strip()

    print("Describe your career aspiration in one sentence (e.g., 'software engineer in fintech').")
    career_aspiration = input("Career aspiration: ").strip()

    skills_list = skills or []
    hobbies_list = hobbies or []

    chosen_skills = _select_from_options(skills_list, "Select your skills (checkbox style):")
    chosen_hobbies = _select_from_options(hobbies_list, "Select your hobbies (checkbox style):")

    user_profile = {
        "grades": grades,
        "career_aspiration": career_aspiration,
        "skills": chosen_skills,
        "hobbies": chosen_hobbies,
    }

    return user_profile
