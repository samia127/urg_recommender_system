# MajorMatch - Detailed Technical Documentation

## Overview

MajorMatch is a university major recommendation system designed to match Omani high school students with appropriate university majors based on their academic performance, skills, hobbies, and career aspirations. The system uses a hybrid approach combining TF-IDF vectorization for semantic similarity matching with rule-based adjustments to refine recommendations.

## System Architecture

### High-Level Flow

```
User Input (Frontend) 
  → Data Normalization 
  → TF-IDF Vectorization 
  → Cosine Similarity Computation 
  → Rule-Based Adjustments 
  → Recommendation Ranking 
  → Response Generation
```

The system is **stateless** - no user data is persisted between sessions. Each request is processed independently using in-memory data structures.

## Data Sources

### majors.json

The primary data source containing information about 25 university majors. Each major entry includes:

- **Basic Information**: `major_id`, `major_name`, `university_name`, `faculty`, `degree_type`, `duration`
- **Academic Requirements**: 
  - `required_hs_subjects`: List of required high school subjects
  - `min_grade_requirements (%)`: Minimum grade requirements per subject
  - `min_overall_percentage (%)`: Minimum overall percentage required
- **Content Fields** (used for similarity matching):
  - `curriculum_keywords`: Topics covered in the major
  - `industry_keywords`: Related career fields
  - `example_career_paths`: Sample career outcomes
  - `learning_style`: Teaching approach (theory, practical, etc.)

**Data Loading Process**:
1. System checks for `majors.normalized.json` first (if normalization script was run)
2. Falls back to `majors.json` if normalized version doesn't exist
3. Loads JSON into pandas DataFrame
4. Normalizes subject names using `subject_normalization.py`
5. Converts grade requirements to standardized format
6. Ensures all list fields are properly formatted (empty lists if missing)

### context.txt

A structured text file containing domain knowledge about the Omani educational system:

1. **Academic Performance Context**: Explains the Science vs Literary stream system, required subjects, and grading scales
2. **Skills List**: Canonical list of skills that students might possess
3. **Hobbies List**: Standard hobbies for normalization
4. **Career Aspirations Examples**: Sample career paths for reference

The context file is parsed using section markers to extract structured lists. These lists are used to normalize user input (e.g., matching "problem solving" to "Problem Solving").

## Preprocessing Pipeline

### User Data Normalization (`user_profile.py`)

When user data arrives from the frontend, it undergoes several normalization steps:

1. **Grade Parsing**:
   - Extracts numeric values from grade strings (handles formats like "85", "85%", "Grade: 85")
   - Normalizes subject names (e.g., "maths" → "mathematics", "islam" → "islamic studies")
   - Stores grades as float values or None if missing

2. **Skills/Hobbies Normalization**:
   - Combines checkbox selections with custom text input
   - Normalizes entries against canonical lists from `context.txt`
   - Cleans text using `text_clean.py` utilities
   - Removes duplicates and empty entries

3. **Career Aspiration Processing**:
   - Preserves original text for display
   - Creates cleaned version for similarity matching
   - Handles empty/missing values gracefully

4. **Stream Identification**:
   - Extracts stream from form data ("science" or "literary")
   - Normalizes to lowercase for consistency

**Output Structure**:
```python
{
    "grades": {"mathematics": 90.0, "english": 85.0, ...},
    "grades_text": "mathematics: 90.0; english: 85.0; ...",
    "overall_grade": 88.5,
    "career_aspiration": "cleaned text for matching",
    "career_aspiration_text": "original user input",
    "skills": ["problem solving", "leadership", ...],
    "hobbies": ["coding", "reading", ...],
    "stream": "science"
}
```

### Text Cleaning (`text_clean.py`)

The text cleaning module standardizes text for similarity matching:

1. **Lowercasing**: Converts all text to lowercase
2. **Acronym Expansion**: Expands common acronyms (e.g., "AI" → "artificial intelligence", "CS" → "computer science")
3. **Separator Normalization**: Replaces "/", "-", "_" with spaces
4. **Punctuation Removal**: Strips all punctuation except alphanumeric and spaces
5. **Whitespace Collapse**: Reduces multiple spaces to single spaces

**Example**:
```
Input:  "Software Engineering / AI & ML"
Output: "software engineering artificial intelligence machine learning"
```

### Subject Normalization (`subject_normalization.py`)

Maps various subject name variants to canonical forms:

- Mathematics variants: "maths", "math", "pure mathematics", "advanced maths" → "mathematics"
- English variants: "english language", "core english language" → "english"
- Science subjects: "physics", "chemistry", "biology" (unchanged)
- Computing: "cs", "ict", "it" → "computer science"
- Humanities: "islam", "islamic studies" → "islamic studies"
- Others: "pe", "physical ed" → "physical education"

This ensures consistent matching between user input and major requirements.

## Vectorization & Similarity Computation

### Major Vectorization (`similarity.py`)

The system creates TF-IDF vectors for all majors by combining multiple text fields:

**Text Corpus Construction**:
For each major, the following fields are concatenated:
- `major_name`
- `faculty`
- `degree_type`
- `required_hs_subjects` (list → space-separated)
- `example_career_paths` (list → space-separated)
- `curriculum_keywords` (list → space-separated)
- `industry_keywords` (list → space-separated)
- `learning_style` (list → space-separated)

The combined text is cleaned using `combine_and_clean()` which applies text cleaning to each part and joins them.

**TF-IDF Configuration**:
- `stop_words="english"`: Removes common English stop words
- `ngram_range=(1, 2)`: Captures both unigrams and bigrams (e.g., "machine learning" as a single feature)
- Vectorizer is fitted once on all majors and cached using `@lru_cache`

**Output**: 
- `vectorizer`: Fitted TfidfVectorizer object
- `matrix`: Sparse matrix of shape (n_majors, n_features)

### User Profile Vectorization

The user profile is vectorized using the same vectorizer (ensuring feature alignment):

**Input Combination**:
- Career aspiration text (cleaned)
- Skills list (space-joined)
- Hobbies list (space-joined)
- Stream identifier

**Process**:
1. Combine all parts with `combine_and_clean()`
2. Transform using the pre-fitted vectorizer
3. Returns sparse vector of shape (1, n_features)

### Cosine Similarity Computation

Similarity scores are computed using cosine similarity between:
- User vector: (1, n_features)
- Majors matrix: (n_majors, n_features)

**Formula**: `cosine_similarity(user_vector, majors_matrix)[0]`

This returns an array of similarity scores (one per major), where:
- Score range: [0, 1]
- Higher scores indicate stronger semantic similarity
- Scores are based on shared terms/ngrams between user profile and major descriptions

**Ranking**: Majors are sorted by similarity score in descending order.

## Rule-Based Adjustments

### Purpose

While TF-IDF captures semantic similarity, it doesn't account for:
- Academic requirements (minimum grades)
- Subject-specific prerequisites
- Career aspiration alignment
- Skill overlap with curriculum

Rule-based adjustments modify similarity scores to reflect these domain constraints.

### Rule Application (`rules.py`)

Rules are applied only to the **top N** candidates (default: 10) from the similarity ranking to reduce computation.

#### 1. Overall Grade Penalty

**Rule**: If user's overall grade is below the major's minimum requirement, reduce score.

```python
if user_grade < min_required_grade:
    score *= GRADE_PENALTY_FACTOR  # Default: 0.75
```

**Rationale**: Students who don't meet minimum requirements should be deprioritized, but not eliminated (they might still be good matches if other factors align).

#### 2. Subject Grade Penalty

**Rule**: For each required subject where user's grade is below minimum, apply penalty.

```python
for subject, required_grade in subject_requirements.items():
    if user_grade < required_grade:
        score *= SUBJECT_GRADE_PENALTY  # Default: 0.6
```

**Rationale**: Subject-specific requirements are critical for certain majors (e.g., mathematics for engineering).

#### 3. Career Aspiration Boost

**Rule**: If user's career text overlaps with major's career paths/industry keywords, boost score.

**Process**:
1. Tokenize user career text and major career paths
2. Extract root tokens (remove common suffixes: "ing", "er", "or", "s")
3. Remove common tokens ("engineer", "engineering", "manager", etc.) to avoid false positives
4. Count overlapping root tokens
5. Apply boost: `score *= min(CAREER_BOOST_FACTOR * (1 + 0.05 * (hits - 1)), 1.4)`

**Example**:
- User: "software developer"
- Major: ["software engineering", "web development"]
- Overlap: "software", "develop" → 2 hits
- Boost: 1.15 * (1 + 0.05 * 1) = 1.2075

**Rationale**: Strong career alignment indicates good fit even if similarity score is moderate.

#### 4. Skill Overlap Boost

**Rule**: If user skills overlap significantly with major's curriculum keywords, boost score.

**Process**:
1. Extract curriculum keywords, learning style, and required subjects from major
2. Count case-insensitive overlaps with user skills
3. If overlap count >= threshold (default: 2), apply boost: `score *= SKILL_BOOST_FACTOR` (default: 1.10)

**Rationale**: Skills that align with curriculum suggest the student will succeed in that major.

### Final Ranking

After rule application:
1. All adjusted scores are re-sorted in descending order
2. Top K majors (default: 4) are selected for return
3. Each major gets a "reason" explanation generated

## Recommendation Explanation Generation

### Reason Building (`rules.py`)

For each recommended major, the system generates a human-readable explanation:

**Components**:
1. **Skill Overlap**: "Matched X of your skills with the major's curriculum"
2. **Career Alignment**: "Career aspiration closely aligns with example paths"
3. **Key Subjects**: "Key subjects: Mathematics, Physics, Chemistry"
4. **Fallback**: "Strong textual similarity to your interests and profile"

**Priority**: Reasons are concatenated with "; " separator, prioritizing skill overlap and career alignment over generic similarity.

## Backend API

### Flask Application (`backend/app.py`)

**Endpoint**: `POST /api/recommend`

**Request Format**:
```json
{
    "stream": "science" | "literary",
    "grades": {
        "maths": "90",
        "english": "85",
        "physics": "88",
        ...
        "overall": "87.5"
    },
    "career_aspiration": "I want to be a software engineer...",
    "skills": ["Problem Solving", "Leadership"],
    "custom_skills": ["Custom skill 1", "Custom skill 2"],
    "hobbies": ["Coding", "Reading"],
    "custom_hobbies": ["Custom hobby"]
}
```

**Processing Flow**:
1. Parse JSON payload
2. Normalize user data using `normalize_user_data()`
3. Generate recommendations using `recommend()`
4. Format response

**Response Format**:
```json
{
    "top_recommendation": {
        "major_name": "Bachelor of Science in Computer Science",
        "score": 0.85,
        "reason": "Matched 3 of your skills...; Career aspiration aligns..."
    },
    "alternatives": [
        {
            "major_name": "...",
            "score": 0.78,
            "reason": "..."
        },
        ...
    ],
    "message": "success"
}
```

**Error Handling**:
- Invalid JSON → 400 with error message
- Processing exception → 500 with error details
- No recommendations → 200 with `top_recommendation: null` and message

**CORS**: Enabled for local development (allows frontend to call from file:// or different port)

## Frontend Architecture

### Page Structure

1. **Landing Page** (`index.html`):
   - Stream selection (Science vs Literary)
   - Language toggle (English/Arabic)

2. **Questionnaire Pages** (`questionnaire_science.html`, `questionnaire_lit.html`):
   - Stream-specific grade inputs
   - Skills checkboxes + custom input
   - Hobbies checkboxes + custom input
   - Career aspiration textarea
   - Form submission to backend

3. **Results Page** (`recommendations.html`):
   - Displays top recommendation (highlighted)
   - Lists alternatives with scores
   - Reads from localStorage (set by questionnaire)

### Data Flow

1. User fills questionnaire
2. JavaScript collects form data
3. POST request to `http://127.0.0.1:5000/api/recommend`
4. Response stored in `localStorage.setItem('latestRecommendations', ...)`
5. Redirect to `recommendations.html`
6. Results page reads from localStorage and renders

### Language Support

**Translation System** (`translations.js`):
- Dictionary-based translations (English/Arabic)
- Automatic RTL switching for Arabic
- Language preference persisted in localStorage
- Dynamic translation of UI elements via `data-translate` attributes

**RTL Support**:
- HTML `dir` attribute switches to "rtl" for Arabic
- CSS rules adjust layout (input-row flex-direction, checkbox margins, etc.)
- Border positioning adjusts (left border for RTL instead of right)

## Performance Characteristics

### Caching Strategy

1. **Major Data Loading**: Loaded once on first request, cached in memory
2. **TF-IDF Vectorization**: Vectorizer and matrix computed once, cached using `@lru_cache`
3. **Context Loading**: Parsed once, cached using `@lru_cache`

**Memory Usage**: 
- Majors DataFrame: ~25 rows × ~15 columns (minimal)
- TF-IDF Matrix: Sparse matrix, typically < 1MB
- Context: Small dictionary (< 100KB)

### Response Time

**Typical Request Processing**:
1. Data normalization: < 10ms
2. User vectorization: < 5ms
3. Similarity computation: < 50ms
4. Rule application: < 20ms
5. Reason generation: < 10ms

**Total**: < 100ms for typical requests (well under 3-second target)

**Bottlenecks**:
- First request: ~500ms (data loading + vectorization)
- Subsequent requests: < 100ms (cached resources)

## Design Decisions

### Why TF-IDF + Rules?

1. **Transparency**: Easy to understand and explain to users
2. **Speed**: Fast computation, no model training required
3. **Interpretability**: Can generate clear reasons for recommendations
4. **Flexibility**: Rules can be adjusted without retraining
5. **No Training Data Required**: Works with structured major data only

### Why Not Neural Networks?

1. **Data Availability**: Limited training data (only 25 majors)
2. **Cold Start**: New majors can be added without retraining
3. **Explainability**: TF-IDF + rules provide clear reasoning
4. **Maintenance**: Simpler to maintain and debug

### Why Stateless?

1. **Privacy**: No user data storage
2. **Simplicity**: No database required
3. **Scalability**: Easy to scale horizontally (no session state)
4. **Compliance**: Easier to meet data protection requirements

## Limitations & Future Improvements

### Current Limitations

1. **Limited Major Coverage**: Only 25 majors in dataset
2. **Static Data**: Major information must be manually updated
3. **No Learning**: System doesn't improve from user feedback
4. **No Personalization History**: Each session is independent
5. **English-Only Backend**: Reason texts are in English (frontend translates)

### Potential Enhancements

1. **Database Integration**: Store user sessions, feedback, major updates
2. **User Authentication**: Track recommendations per user
3. **Feedback Loop**: Collect user satisfaction, adjust weights
4. **Major Expansion**: Add more majors, universities, specializations
5. **Advanced ML**: Fine-tune embeddings, use transformer models
6. **Multi-language Backend**: Generate reasons in Arabic directly
7. **Recommendation History**: Show previous recommendations to returning users
8. **Comparison Tool**: Allow side-by-side major comparison

## File Structure Summary

```
major_matcher/
  ├── __init__.py          # Package exports
  ├── config.py            # Configuration constants
  ├── data_loader.py       # Load majors.json and context.txt
  ├── recommender.py       # Main recommendation function
  ├── similarity.py        # TF-IDF vectorization and cosine similarity
  ├── rules.py             # Rule-based score adjustments
  ├── user_profile.py      # User data normalization
  ├── subject_normalization.py  # Subject name mapping
  └── text_clean.py        # Text preprocessing utilities

backend/
  └── app.py               # Flask API server

frontend/
  ├── index.html           # Landing page
  ├── questionnaire_science.html  # Science stream form
  ├── questionnaire_lit.html       # Literary stream form
  ├── recommendations.html         # Results display
  ├── style.css           # Styling (with RTL support)
  └── translations.js      # Language translation system

data/
  ├── majors.json         # Major data (25 entries)
  └── context.txt         # Domain knowledge
```

## Conclusion

MajorMatch is a lightweight, transparent, and efficient recommendation system that balances semantic similarity matching with domain-specific rules. Its stateless design ensures privacy and simplicity while providing accurate, explainable recommendations for Omani students choosing university majors.

