from typing import Dict, List, Any


class MockAIService:
    """
    Mock AI service for MVP. Replace with OpenAI/Claude integration later
    by implementing the same interface.
    """

    ROADMAP_TEMPLATES: Dict[str, Dict[str, Any]] = {
        "default": {
            "months": [
                {
                    "month": 1,
                    "title": "Foundation & Self-Discovery",
                    "description": "Build your knowledge base and map out your goals.",
                    "tasks": [
                        "Research your target field for 30 min/day",
                        "Watch 3 intro lectures on your chosen major",
                        "Join 2 online communities in your field",
                        "Set up your study schedule",
                    ],
                },
                {
                    "month": 2,
                    "title": "English & Core Skills",
                    "description": "Strengthen language skills and build fundamentals.",
                    "tasks": [
                        "Complete 20 hours of English practice",
                        "Take a free online course in your major",
                        "Start building your study portfolio",
                        "Research 5 target universities",
                    ],
                },
                {
                    "month": 3,
                    "title": "First Real Project",
                    "description": "Create something tangible to show universities.",
                    "tasks": [
                        "Complete a beginner project in your field",
                        "Write a 1-page personal statement draft",
                        "Attend 1 virtual campus tour or webinar",
                        "Ask 2 people for a reference letter",
                    ],
                },
                {
                    "month": 4,
                    "title": "University Research & Documents",
                    "description": "Shortlist universities and prepare your documents.",
                    "tasks": [
                        "Create final shortlist of 5-8 universities",
                        "Gather all required documents",
                        "Get transcripts translated if needed",
                        "Draft your Statement of Purpose",
                    ],
                },
                {
                    "month": 5,
                    "title": "Applications Open!",
                    "description": "Submit your applications with confidence.",
                    "tasks": [
                        "Submit 3 applications this month",
                        "Track application deadlines in a spreadsheet",
                        "Write unique essays for each university",
                        "Prepare for possible interviews",
                    ],
                },
                {
                    "month": 6,
                    "title": "Interviews, Visa & Next Steps",
                    "description": "Ace interviews and prepare for your journey abroad.",
                    "tasks": [
                        "Practice 5 mock interviews",
                        "Research visa requirements for your target country",
                        "Connect with current students at your target university",
                        "Celebrate every acceptance — you earned it!",
                    ],
                },
            ]
        },
    }

    COUNTRY_TIPS: Dict[str, str] = {
        "Germany": "German universities are tuition-free for many programs! Focus on German language or strong English proficiency.",
        "USA": "US admissions value extracurriculars and essays. Start SAT/ACT prep early.",
        "UK": "UK degrees are 3 years. UCAS applications open in September.",
        "Canada": "Canada is welcoming to international students. Check IELTS requirements.",
        "Turkey": "Turkey offers scholarships via Türkiye Bursları. Applications open in February.",
        "South Korea": "GKS scholarships available. Korean language skills are a big plus.",
        "Malaysia": "Affordable tuition. Many programs taught in English.",
        "Kazakhstan": "Check Bolashak scholarship. Strong focus on STEM programs.",
        "UAE": "Growing hub for international education. Many global university branches.",
    }

    MAJOR_TIPS: Dict[str, str] = {
        "Cybersecurity": "Build a home lab, get CompTIA Security+ certified, and contribute to CTF competitions.",
        "Software Engineering": "Build 3 GitHub projects and learn Git, algorithms, and one framework deeply.",
        "Artificial Intelligence": "Learn Python, NumPy, and complete Andrew Ng's ML course.",
        "Data Science": "Master Python, SQL, and visualization tools like Tableau or Power BI.",
        "Business Administration": "Develop leadership skills and start a small project or club.",
        "Medicine": "Shadow a doctor if possible, prepare strong grades in Biology/Chemistry.",
        "Psychology": "Read research papers and volunteer in social services.",
        "Architecture": "Build a portfolio of drawings and 3D models.",
        "International Law": "Join debate club, follow international news daily.",
        "Education": "Get tutoring experience and volunteer at schools.",
    }

    @classmethod
    def generate_profile_explanation(cls, data: Dict[str, Any]) -> str:
        top_cats = data.get("top_categories", [])
        rec_majors = data.get("recommended_majors", [])
        name = data.get("full_name", "Explorer")

        cat_labels = {
            "IT_ENGINEERING": "Technology & Engineering",
            "DATA_AI": "Data Science & AI",
            "MEDICINE": "Medicine & Health",
            "BUSINESS": "Business & Finance",
            "LAW": "Law & Policy",
            "DESIGN_CREATIVE": "Design & Creativity",
            "SOCIAL_SCIENCES": "Social Sciences",
            "EDUCATION": "Education",
        }
        top_names = [cat_labels.get(c, c) for c in top_cats[:2]]
        majors_str = ", ".join(rec_majors[:3]) if rec_majors else "various exciting fields"

        return (
            f"Hey {name}! Your assessment reveals that you have a natural talent for "
            f"{' and '.join(top_names)}. "
            f"Based on your answers, you would thrive in fields like {majors_str}. "
            f"You're the kind of person who combines analytical thinking with real-world curiosity — "
            f"exactly what international universities are looking for. "
            f"Your journey to a top global university starts now. Let's build your roadmap!"
        )

    @classmethod
    def generate_admission_roadmap(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        major = data.get("target_major", "your chosen field")
        country = data.get("target_country", "your target country")
        english_level = data.get("english_level", "B1")
        budget = data.get("budget_usd", 15000)

        template = cls.ROADMAP_TEMPLATES["default"]
        months = []

        country_tip = cls.COUNTRY_TIPS.get(country, f"Research specific requirements for {country}.")
        major_tip = cls.MAJOR_TIPS.get(major, f"Build a strong portfolio in {major}.")

        for i, month_data in enumerate(template["months"]):
            tasks = list(month_data["tasks"])
            if i == 0:
                tasks.append(major_tip)
            if i == 1 and english_level in ["A1", "A2", "B1"]:
                tasks.insert(0, "Enroll in an intensive English course (IELTS/TOEFL prep)")
            if i == 3:
                tasks.append(country_tip)
            months.append({
                "month_number": month_data["month"],
                "title": month_data["title"],
                "description": month_data["description"],
                "tasks": tasks,
                "xp_reward": 50,
            })

        duration = 6
        if english_level in ["A1", "A2"]:
            duration = 9
            months.extend([
                {
                    "month_number": 7,
                    "title": "Advanced English & Test Prep",
                    "description": "Reach B2+ level and pass your English test.",
                    "tasks": [
                        "Take a full IELTS/TOEFL mock test",
                        "Score at least 6.0 on IELTS practice",
                        "Review weak areas with a tutor",
                        "Read 2 academic articles in English per week",
                    ],
                    "xp_reward": 50,
                },
                {
                    "month_number": 8,
                    "title": "Final Applications & Scholarship Hunt",
                    "description": "Apply for scholarships and finalize applications.",
                    "tasks": [
                        "Apply for 2 scholarships",
                        "Submit remaining university applications",
                        "Request final recommendation letters",
                        "Prepare financial documents",
                    ],
                    "xp_reward": 50,
                },
                {
                    "month_number": 9,
                    "title": "Results & Pre-Departure",
                    "description": "Handle offers, visa, and celebrate your achievement.",
                    "tasks": [
                        "Compare offers and make your final choice",
                        "Apply for student visa",
                        "Book flights and accommodation",
                        "Connect with your future university community",
                    ],
                    "xp_reward": 75,
                },
            ])

        title = f"Your {major} Journey to {country}"
        summary = (
            f"This {duration}-month roadmap will guide you step by step from where you are now "
            f"to submitting strong applications to universities in {country}. "
            f"Each month builds on the last — stay consistent and you'll get there!"
        )
        return {
            "title": title,
            "summary": summary,
            "duration_months": duration,
            "months": months,
        }

    @classmethod
    def generate_daily_tasks(cls, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        major = data.get("target_major", "your field")
        english_level = data.get("english_level", "B1")

        base_tasks = [
            {"title": f"Read one article about {major}", "xp": 10, "duration_min": 15},
            {"title": "Practice English for 20 minutes", "xp": 10, "duration_min": 20},
            {"title": "Review your roadmap progress", "xp": 5, "duration_min": 5},
        ]
        if english_level in ["A1", "A2", "B1"]:
            base_tasks.append({"title": "Learn 10 new English words (Anki or Quizlet)", "xp": 10, "duration_min": 10})
        base_tasks.append({"title": f"Watch a 10-min video about {major}", "xp": 15, "duration_min": 10})
        return base_tasks


def get_ai_service() -> MockAIService:
    return MockAIService()
