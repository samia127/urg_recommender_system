# MajorMatch Recommendation System

This repository contains a lightweight recommendation engine to match students with university majors using TF-IDF similarity plus rule-based adjustments. The project is designed for Google Colab and ships with two notebooks:

- `major_recommender_main.ipynb`: interactive pipeline for collecting user input and generating recommendations.
- `major_recommender_testing.ipynb`: testing harness with mock profiles and quick rule tuning.

## Repository contents
- `majors.json`: data for 25 majors (name, keywords, requirements, example career paths).
- `academics_and_skills_info`: background text describing the Omani grading context plus skills, hobbies, and career examples.
- `major_matcher/`: Python helpers for loading data, collecting input, computing similarity, applying rules, and reporting.

## Running in Google Colab
1. Upload the repo contents to Colab or mount the repository in your session.
2. Open `major_recommender_main.ipynb` and run all cells. The notebook will:
   - Load `majors.json` and parse `academics_and_skills_info`.
   - Collect user grades, skills, hobbies, and career aspirations via text inputs.
   - Compute TF-IDF similarity and apply heuristic rules.
   - Return a recommendation report with alternatives and confidence.
3. To validate the pipeline, open `major_recommender_testing.ipynb` and run all cells. Edit the `mock_profiles` list or `TOP_N` parameter to experiment with rule impacts.

## Python helper overview
- `major_matcher/data.py`: `load_majors_data` (JSON to DataFrame) and `load_context` (parse contextual text into grade scale, skills, hobbies, and career examples).
- `major_matcher/user_profile.py`: `collect_user_input` for notebook-friendly prompts.
- `major_matcher/similarity.py`: TF-IDF vectorization for majors and user profiles plus cosine similarity ranking.
- `major_matcher/rules.py`: heuristic adjustments for grades, career alignment, and skill overlaps, plus readable reporting.

All helpers are exposed via `major_matcher/__init__.py` so notebooks can simply `from major_matcher import ...` without deep imports.

## Notes
- The rule set is intentionally simple and can be tuned in `major_matcher/rules.py` or within the testing notebook.
- If `nbformat` is missing locally, install it with `pip install nbformat` before modifying the notebooks programmatically.
