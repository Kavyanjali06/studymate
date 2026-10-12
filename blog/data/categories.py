CATEGORIES = [
    {
        "slug": "study-planning",
        "name": "Study Planning",
        "description": "Build effective study schedules, timetables, and daily routines that fit your life.",
        "icon": "bi-calendar2-check",
    },
    {
        "slug": "productivity-focus",
        "name": "Productivity & Focus",
        "description": "Beat procrastination, stay focused, and make the most of every study session.",
        "icon": "bi-lightning-charge",
    },
    {
        "slug": "exam-preparation",
        "name": "Exam Preparation",
        "description": "Prepare for tests and semester exams calmly with proven revision strategies.",
        "icon": "bi-pencil-square",
    },
    {
        "slug": "assignments-time-management",
        "name": "Assignments & Time Management",
        "description": "Manage deadlines, multiple assignments, and your college schedule without burnout.",
        "icon": "bi-clock-history",
    },
    {
        "slug": "student-success",
        "name": "Student Success",
        "description": "Develop habits, goals, and mindset that help you grow throughout your academic journey.",
        "icon": "bi-mortarboard",
    },
    {
        "slug": "digital-learning-ai-tools",
        "name": "Digital Learning & AI Tools",
        "description": "Use digital tools and AI thoughtfully to study better and learn faster.",
        "icon": "bi-robot",
    },
]

CATEGORY_MAP = {cat["slug"]: cat for cat in CATEGORIES}


def get_category(slug):
    return CATEGORY_MAP.get(slug)
