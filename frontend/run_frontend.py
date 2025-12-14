

from flask import Flask, request, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 


MAJORS_DATA = [
    {
        "id": 101,
        "name_en": "Software Engineering",
        "name_ar": "هندسة البرمجيات",
        "description": "تطوير وتصميم الأنظمة والتطبيقات الحاسوبية المعقدة.",
        "required_skills": ["Programming", "Logic", "Problem_Solving", "Technical"],
        "interest_match": ["Technology", "Innovation", "Analysis"],
        "min_score": 90,
    },
    {
        "id": 102,
        "name_en": "Digital Marketing",
        "name_ar": "التسويق الرقمي",
        "description": "استخدام القنوات الرقمية لترويج المنتجات وبناء العلامات التجارية.",
        "required_skills": ["Communication", "Creativity", "Analysis"],
        "interest_match": ["Communication", "Marketing", "Trend_Analysis"],
        "min_score": 80,
    },
    {
        "id": 103,
        "name_en": "Financial Management",
        "name_ar": "الإدارة المالية",
        "description": "إدارة الأصول والاستثمارات وتحليل البيانات المالية للمؤسسات.",
        "required_skills": ["Mathematics", "Analysis", "Attention_to_Detail"],
        "interest_match": ["Finance", "Investment", "Risk_Management"],
        "min_score": 85,
    },
    {
        "id": 104,
        "name_en": "Human Medicine",
        "name_ar": "الطب البشري",
        "description": "دراسة التشخيص والعلاج والوقاية من الأمراض البشرية.",
        "required_skills": ["Biology", "Chemistry", "Patience", "High_Academic_Performance"],
        "interest_match": ["Science", "Help_People", "Research"],
        "min_score": 95,
    },
    {
        "id": 105,
        "name_en": "Architecture",
        "name_ar": "الهندسة المعمارية",
        "description": "تصميم وتخطيط المباني والمنشآت مع الجانب الجمالي والوظيفي.",
        "required_skills": ["Creativity", "Drawing", "Problem_Solving", "Physics"],
        "interest_match": ["Design", "Art", "Structure"],
        "min_score": 88,
    },
    {
        "id": 106,
        "name_en": "Data Science",
        "name_ar": "علم البيانات",
        "description": "تحليل مجموعات البيانات الضخمة (Big Data) واستخراج الرؤى والمعلومات لاتخاذ القرارات.",
        "required_skills": ["Programming", "Analysis", "Mathematics", "Problem_Solving"],
        "interest_match": ["Technology", "Research", "Analysis"],
        "min_score": 92,
    },
    {
        "id": 107,
        "name_en": "Civil Engineering",
        "name_ar": "الهندسة المدنية",
        "description": "تصميم وبناء وإدارة المشاريع الهيكلية الكبيرة مثل الجسور والطرق والمباني.",
        "required_skills": ["Mathematics", "Physics", "Attention_to_Detail", "Problem_Solving"],
        "interest_match": ["Structure", "Construction", "Project_Management"],
        "min_score": 85,
    },
    {
        "id": 108,
        "name_en": "Graphic Design",
        "name_ar": "التصميم الجرافيكي",
        "description": "إنشاء مرئيات واتصالات بصرية باستخدام البرامج والأدوات الرقمية.",
        "required_skills": ["Creativity", "Artistic_Skill", "Technical"],
        "interest_match": ["Design", "Art", "Communication"],
        "min_score": 75,
    },
    {
        "id": 109,
        "name_en": "Mass Communication (Journalism)",
        "name_ar": "الإعلام والاتصال الجماهيري (الصحافة)",
        "description": "نقل المعلومات والأخبار عبر وسائل الإعلام المختلفة وتحليل القضايا الاجتماعية.",
        "required_skills": ["Communication", "Writing", "Research", "Social_Analysis"],
        "interest_match": ["Communication", "Writing", "Social_Issues"],
        "min_score": 80,
    }
]


def calculate_match_score(user_data, major):
    score = 10 
    
    def get_academic_score(subject_key):
        score_str = user_data.get(subject_key, "0")
        try:
            if subject_key not in user_data or user_data.get(subject_key) == '':
                 return 0
            return int(score_str)
        except ValueError:
            return 0

    math_score = get_academic_score('academic_math')
    physics_score = get_academic_score('academic_physics')
    biology_score = get_academic_score('academic_biology')
    chemistry_score = get_academic_score('academic_chemistry')
    cs_score = get_academic_score('academic_cs')
    arabic_score = get_academic_score('academic_arabic')
    english_score = get_academic_score('academic_english')
    history_score = get_academic_score('academic_history')
    

    if major["name_en"] in ["Software Engineering", "Architecture", "Civil Engineering", "Data Science"]:
        
        if major["name_en"] in ["Software Engineering", "Data Science"]:
              engineering_average = (math_score + physics_score + cs_score) / 3
        else: 
              engineering_average = (math_score + physics_score) / 2
        
        if engineering_average >= 85:
            score += 45 
        elif engineering_average >= 70:
            score += 25
        
        if engineering_average < 50:
            score -= 40 
            
    if major["name_en"] == "Human Medicine":
        medical_average = (biology_score + chemistry_score) / 2
        
        if medical_average >= 90:
            score += 50 
        elif medical_average >= 75:
            score += 35
        
        if medical_average < 60:
            score -= 45
        
    if major["name_en"] == "Data Science":
        data_science_average = (math_score + cs_score) / 2
        
        if data_science_average >= 88:
            score += 35
        elif data_science_average >= 70:
            score += 15
        
        if data_science_average < 50:
            score -= 30
            
    if major["name_en"] == "Mass Communication (Journalism)":
        humanities_average = (arabic_score + english_score + history_score) / 3
        
        if humanities_average >= 80:
            score += 30
        
        if humanities_average < 50:
             score -= 25
        
    if major["name_en"] == "Digital Marketing":
         if english_score >= 80:
            score += 15
    
    
    if major["name_en"] in ["Software Engineering", "Data Science"] and user_data.get('hobby_coding') is True:
        score += 8
        
    if major["name_en"] in ["Digital Marketing", "Mass Communication (Journalism)"] and user_data.get('skill_communication') is True:
        score += 8
        
    if major["name_en"] == "Graphic Design":
        if user_data.get('skill_creativity') is True or user_data.get('skill_technical') is True: 
              score += 10
              
    if major["name_en"] == "Human Medicine" and user_data.get('skill_interpersonal') is True:
        score += 5


    return max(0, min(score, 100))



@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    if not request.json:
        return jsonify({"error": "Missing JSON data"}), 400

    user_data = request.json
    print("Received data from frontend:", user_data)
    
    results = []
    
    for major in MAJORS_DATA:
        match_percentage = calculate_match_score(user_data, major)
        
        if match_percentage >= 70:
            results.append({
                "name_en": major["name_en"],
                "name_ar": major["name_ar"], 
                "description": major["description"],
                "match_score": f"{match_percentage}%", 
            })
    
    results.sort(key=lambda x: int(x['match_score'].replace('%', '')), reverse=True)
    
    return jsonify(results[:5]) 

if __name__ == '__main__':
    app.run(debug=True, port=5000)