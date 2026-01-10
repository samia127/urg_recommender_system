// Translation dictionaries for MajorMatch system
const translations = {
  en: {
    // Landing page
    title: "Majors recommender system",
    findMajor: "FIND YOUR UNIVERSITY MAJOR",
    subtitle: "Answer a few questions and get personalized major recommendations",
    scienceStream: "Science Stream",
    literaryStream: "Literary Stream",
    
    // Questionnaire common
    academicPerformance: "Academic Performance",
    scienceStreamTitle: "Science Stream: Academic Performance",
    literaryStreamTitle: "Literary Stream: Academic Performance",
    whatAreYouGoodAt: "What are you good at?",
    otherSkills: "Other Skills (optional):",
    whatDoYouEnjoy: "What do you enjoy doing in your free time?",
    otherHobbies: "Other Hobbies (optional):",
    futureGoals: "What are your future goals?",
    getRecommendations: "GET RECOMMENDATIONS",
    processing: "PROCESSING...",
    
    // Subject names
    mathematics: "Mathematics",
    english: "English",
    physics: "Physics",
    chemistry: "Chemistry",
    biology: "Biology",
    islamicStudies: "Islamic Studies",
    arabic: "Arabic",
    socialStudies: "Social Studies",
    arts: "Arts",
    music: "Music",
    physicalEducation: "Physical Education",
    overallPercentage: "Overall Percentage",
    
    // Skills
    criticalThinking: "Critical Thinking",
    leadership: "Leadership",
    problemSolving: "Problem Solving",
    communication: "Communication",
    teamwork: "Teamwork",
    interpersonalSkills: "Interpersonal Skills",
    technicalLiteracy: "Technical Literacy",
    creativity: "Creativity",
    timeManagement: "Time Management",
    
    // Hobbies
    photography: "Photography",
    sports: "Sports",
    drawingPainting: "Drawing/Painting",
    playingInstrument: "Playing Instrument",
    codingProgramming: "Coding/Programming",
    reading: "Reading",
    volunteering: "Volunteering",
    cooking: "Cooking",
    debating: "Debating",
    
    // Recommendations page
    yourRecommendedMajors: "Your Recommended Majors",
    basedOnData: "Based on the data you provided in the questionnaire.",
    topMatch: "Top Match",
    why: "Why:",
    otherStrongOptions: "Other Strong Options",
    matchScore: "Match Score",
    noRecommendations: "No recommendations found. Please complete the questionnaire first.",
    errorLoading: "Error loading data.",
    noRecommendationFound: "No recommendation found based on your inputs.",
    noOtherMatches: "No other close matches found.",
    retakeQuestionnaire: "Retake Questionnaire",
    
    // Error messages
    backendError: "Backend error",
    fetchFailed: "Fetch failed. Check your connection or backend server.",
    
    // Language toggle
    language: "Language",
    english: "English",
    arabic: "Arabic",
    
    // Reason texts (from backend)
    matchedSkills: "Matched {count} of your skills with the major's curriculum",
    careerAligns: "Career aspiration closely aligns with example paths",
    keySubjects: "Key subjects: {subjects}",
    strongSimilarity: "Strong textual similarity to your interests and profile"
  },
  
  ar: {
    // Landing page
    title: "نظام توصية التخصصات",
    findMajor: "اكتشف تخصصك الجامعي",
    subtitle: "أجب على بضعة أسئلة واحصل على توصيات تخصص مخصصة",
    scienceStream: "المسار العلمي",
    literaryStream: "المسار الأدبي",
    
    // Questionnaire common
    academicPerformance: "الأداء الأكاديمي",
    scienceStreamTitle: "المسار العلمي: الأداء الأكاديمي",
    literaryStreamTitle: "المسار الأدبي: الأداء الأكاديمي",
    whatAreYouGoodAt: "ما الذي تجيده؟",
    otherSkills: "مهارات أخرى (اختياري):",
    whatDoYouEnjoy: "ماذا تستمتع بفعله في وقت فراغك؟",
    otherHobbies: "هوايات أخرى (اختياري):",
    futureGoals: "ما هي أهدافك المستقبلية؟",
    getRecommendations: "احصل على التوصيات",
    processing: "جاري المعالجة...",
    
    // Subject names
    mathematics: "الرياضيات",
    english: "اللغة الإنجليزية",
    physics: "الفيزياء",
    chemistry: "الكيمياء",
    biology: "الأحياء",
    islamicStudies: "الدراسات الإسلامية",
    arabic: "اللغة العربية",
    socialStudies: "الدراسات الاجتماعية",
    arts: "الفنون",
    music: "الموسيقى",
    physicalEducation: "التربية البدنية",
    overallPercentage: "النسبة المئوية الإجمالية",
    
    // Skills
    criticalThinking: "التفكير النقدي",
    leadership: "القيادة",
    problemSolving: "حل المشكلات",
    communication: "التواصل",
    teamwork: "العمل الجماعي",
    interpersonalSkills: "المهارات الشخصية",
    technicalLiteracy: "القراءة التقنية",
    creativity: "الإبداع",
    timeManagement: "إدارة الوقت",
    
    // Hobbies
    photography: "التصوير الفوتوغرافي",
    sports: "الرياضة",
    drawingPainting: "الرسم/التلوين",
    playingInstrument: "العزف على الآلات",
    codingProgramming: "البرمجة/التشفير",
    reading: "القراءة",
    volunteering: "التطوع",
    cooking: "الطبخ",
    debating: "المناظرة",
    
    // Recommendations page
    yourRecommendedMajors: "التخصصات الموصى بها",
    basedOnData: "بناءً على البيانات التي قدمتها في الاستبيان.",
    topMatch: "أفضل تطابق",
    why: "لماذا:",
    otherStrongOptions: "خيارات قوية أخرى",
    matchScore: "نقاط التطابق",
    noRecommendations: "لم يتم العثور على توصيات. يرجى إكمال الاستبيان أولاً.",
    errorLoading: "خطأ في تحميل البيانات.",
    noRecommendationFound: "لم يتم العثور على توصية بناءً على مدخلاتك.",
    noOtherMatches: "لم يتم العثور على تطابقات قريبة أخرى.",
    retakeQuestionnaire: "إعادة الاستبيان",
    
    // Error messages
    backendError: "خطأ في الخادم",
    fetchFailed: "فشل الاتصال. تحقق من اتصالك أو خادم الخلفية.",
    
    // Language toggle
    language: "اللغة",
    english: "English",
    arabic: "العربية",
    
    // Reason texts (from backend)
    matchedSkills: "تطابق {count} من مهاراتك مع منهج التخصص",
    careerAligns: "طموحك المهني يتماشى بشكل وثيق مع المسارات المثال",
    keySubjects: "المواد الأساسية: {subjects}",
    strongSimilarity: "تشابه نصي قوي مع اهتماماتك وملفك الشخصي"
  }
};

// Language management utilities
const LanguageManager = {
  currentLang: localStorage.getItem('majorMatchLanguage') || 'en',
  
  init() {
    this.setLanguage(this.currentLang);
  },
  
  setLanguage(lang) {
    if (!translations[lang]) {
      lang = 'en';
    }
    this.currentLang = lang;
    localStorage.setItem('majorMatchLanguage', lang);
    
    // Update HTML attributes
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    
    // Translate all elements
    this.translatePage();
    
    // Update language toggle if it exists
    this.updateLanguageToggle();
  },
  
  translatePage() {
    // Find all elements with data-translate attribute
    document.querySelectorAll('[data-translate]').forEach(el => {
      const key = el.getAttribute('data-translate');
      const translation = this.t(key);
      if (translation) {
        if (el.tagName === 'INPUT' && (el.type === 'text' || el.type === 'submit')) {
          if (el.type === 'text') {
            el.placeholder = translation;
          } else {
            el.value = translation;
          }
        } else if (el.tagName === 'BUTTON' || el.tagName === 'A') {
          el.textContent = translation;
        } else {
          el.textContent = translation;
        }
      }
    });
    
    // Translate title
    const titleKey = document.querySelector('[data-title-key]');
    if (titleKey) {
      const titleKeyValue = titleKey.getAttribute('data-title-key');
      if (titleKeyValue) {
        document.title = this.t(titleKeyValue);
      }
    }
  },
  
  t(key, params = {}) {
    const keys = key.split('.');
    let value = translations[this.currentLang];
    
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        return key; // Return key if translation not found
      }
    }
    
    // Replace placeholders
    if (typeof value === 'string' && params) {
      Object.keys(params).forEach(param => {
        value = value.replace(`{${param}}`, params[param]);
      });
    }
    
    return value || key;
  },
  
  updateLanguageToggle() {
    const toggle = document.getElementById('language-toggle');
    if (toggle) {
      toggle.textContent = this.currentLang === 'en' ? this.t('arabic') : this.t('english');
    }
  },
  
  toggle() {
    const newLang = this.currentLang === 'en' ? 'ar' : 'en';
    this.setLanguage(newLang);
  },
  
  translateReason(reasonText) {
    if (this.currentLang === 'en') {
      return reasonText;
    }
    
    // Translate common reason patterns from backend
    let translated = reasonText;
    
    // Match patterns like "Matched X of your skills"
    translated = translated.replace(/Matched (\d+) of your skills with the major's curriculum/g, (match, count) => {
      return this.t('matchedSkills', { count });
    });
    
    // Match "Career aspiration closely aligns"
    if (translated.includes('Career aspiration closely aligns')) {
      translated = this.t('careerAligns');
    }
    
    // Match "Key subjects: ..."
    translated = translated.replace(/Key subjects: (.+)/g, (match, subjects) => {
      return this.t('keySubjects', { subjects });
    });
    
    // Match "Strong textual similarity"
    if (translated.includes('Strong textual similarity')) {
      translated = this.t('strongSimilarity');
    }
    
    // If no pattern matched, return original (might be a custom reason)
    return translated === reasonText ? reasonText : translated;
  }
};

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => LanguageManager.init());
} else {
  LanguageManager.init();
}

