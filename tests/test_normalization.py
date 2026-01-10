import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from major_matcher.user_profile import normalize_user_data
from major_matcher.subject_normalization import normalize_subject
from major_matcher.text_clean import clean_text
from major_matcher.rules import apply_rules


class NormalizationTests(unittest.TestCase):
    def test_subject_normalization_variants(self):
        self.assertEqual(normalize_subject("Advanced maths"), "mathematics")
        self.assertEqual(normalize_subject("cs"), "computer science")
        self.assertEqual(normalize_subject("physical education"), "physical education")

    def test_grade_parsing_structured(self):
        payload = {
            "grades": {
                "maths": "85%",
                "english": "90",
                "overall": "88%",
            },
            "career_aspiration": "",
            "skills": [],
            "hobbies": [],
        }
        normalized = normalize_user_data(payload)
        self.assertEqual(normalized["overall_grade"], 88.0)
        self.assertEqual(normalized["grades"].get("mathematics"), 85.0)

    def test_acronym_expansion(self):
        cleaned = clean_text("Interested in AI/ML and FinTech")
        self.assertIn("artificial intelligence", cleaned)
        self.assertIn("machine learning", cleaned)
        self.assertIn("financial technology", cleaned)

    def test_grade_penalty_applies(self):
        majors_df = pd.DataFrame(
            [
                {
                    "major_name": "Test Major",
                    "min_overall_percentage": 80,
                    "min_grade_requirements": {"mathematics": 85},
                    "required_hs_subjects": [],
                    "example_career_paths": [],
                    "industry_keywords": [],
                    "curriculum_keywords": [],
                    "learning_style": [],
                }
            ]
        )
        ranked = [{"major_name": "Test Major", "score": 1.0, "index": 0}]
        user_profile = {
            "overall_grade": 75.0,
            "grades": {"mathematics": 80.0},
            "career_aspiration": "",
            "skills": [],
        }
        adjusted = apply_rules(ranked, user_profile, majors_df, top_n=1)
        self.assertLess(adjusted[0]["score"], 1.0)
        # Expect both penalties to have applied
        self.assertAlmostEqual(adjusted[0]["score"], 1.0 * 0.75 * 0.6)


if __name__ == "__main__":
    unittest.main()
