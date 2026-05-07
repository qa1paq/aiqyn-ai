import sys
import os
from pathlib import Path

# Add backend/ to sys.path so imports work from any working directory
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.core.database import SessionLocal

# Import ALL models so SQLAlchemy can resolve all relationship references
import app.models.user
import app.models.profile
import app.models.assessment
import app.models.university
import app.models.choice
import app.models.match
import app.models.roadmap
import app.models.gamification

from app.models.university import University, Major
from app.services.gamification_service import GamificationService

UNIVERSITIES = [
    {
        "name": "Massachusetts Institute of Technology",
        "country": "USA",
        "city": "Cambridge",
        "website": "https://www.mit.edu",
        "description": "World-leading research university known for science, engineering, and technology innovation.",
        "ranking": 1,
        "tuition_min_usd": 55000,
        "tuition_max_usd": 60000,
    },
    {
        "name": "University of Toronto",
        "country": "Canada",
        "city": "Toronto",
        "website": "https://www.utoronto.ca",
        "description": "Canada's top research university with strong programs in every discipline.",
        "ranking": 21,
        "tuition_min_usd": 30000,
        "tuition_max_usd": 45000,
    },
    {
        "name": "University College London",
        "country": "UK",
        "city": "London",
        "website": "https://www.ucl.ac.uk",
        "description": "One of the UK's leading research universities located in the heart of London.",
        "ranking": 9,
        "tuition_min_usd": 28000,
        "tuition_max_usd": 40000,
    },
    {
        "name": "Technical University of Munich",
        "country": "Germany",
        "city": "Munich",
        "website": "https://www.tum.de",
        "description": "Germany's top technical university with tuition-free education for most programs.",
        "ranking": 50,
        "tuition_min_usd": 0,
        "tuition_max_usd": 3000,
    },
    {
        "name": "Koç University",
        "country": "Turkey",
        "city": "Istanbul",
        "website": "https://www.ku.edu.tr",
        "description": "Turkey's premier private university with strong English-language programs.",
        "ranking": 501,
        "tuition_min_usd": 8000,
        "tuition_max_usd": 15000,
    },
    {
        "name": "Seoul National University",
        "country": "South Korea",
        "city": "Seoul",
        "website": "https://www.snu.ac.kr",
        "description": "South Korea's most prestigious university with world-class research facilities.",
        "ranking": 36,
        "tuition_min_usd": 4000,
        "tuition_max_usd": 9000,
    },
    {
        "name": "University of Malaya",
        "country": "Malaysia",
        "city": "Kuala Lumpur",
        "website": "https://www.um.edu.my",
        "description": "Malaysia's oldest and highest-ranked university, with many English programs.",
        "ranking": 70,
        "tuition_min_usd": 3000,
        "tuition_max_usd": 8000,
    },
    {
        "name": "Nazarbayev University",
        "country": "Kazakhstan",
        "city": "Astana",
        "website": "https://nu.edu.kz",
        "description": "Kazakhstan's flagship research university modeled on world-class institutions.",
        "ranking": 600,
        "tuition_min_usd": 2000,
        "tuition_max_usd": 6000,
    },
    {
        "name": "New York University Abu Dhabi",
        "country": "UAE",
        "city": "Abu Dhabi",
        "website": "https://nyuad.nyu.edu",
        "description": "An elite liberal arts and science college in the heart of Abu Dhabi.",
        "ranking": 200,
        "tuition_min_usd": 20000,
        "tuition_max_usd": 55000,
    },
    {
        "name": "University of British Columbia",
        "country": "Canada",
        "city": "Vancouver",
        "website": "https://www.ubc.ca",
        "description": "One of Canada's top research universities on the Pacific coast.",
        "ranking": 34,
        "tuition_min_usd": 32000,
        "tuition_max_usd": 48000,
    },
    {
        "name": "RWTH Aachen University",
        "country": "Germany",
        "city": "Aachen",
        "website": "https://www.rwth-aachen.de",
        "description": "Germany's top technical university for engineering and computer science.",
        "ranking": 165,
        "tuition_min_usd": 0,
        "tuition_max_usd": 2500,
    },
    {
        "name": "University of Edinburgh",
        "country": "UK",
        "city": "Edinburgh",
        "website": "https://www.ed.ac.uk",
        "description": "Historic Scottish university ranked among the world's top 30.",
        "ranking": 22,
        "tuition_min_usd": 25000,
        "tuition_max_usd": 38000,
    },
    {
        "name": "KAIST",
        "country": "South Korea",
        "city": "Daejeon",
        "website": "https://www.kaist.ac.kr",
        "description": "Korea's top science and technology institute, fully English-taught.",
        "ranking": 42,
        "tuition_min_usd": 3000,
        "tuition_max_usd": 7000,
    },
    {
        "name": "University of Sharjah",
        "country": "UAE",
        "city": "Sharjah",
        "website": "https://www.sharjah.ac.ae",
        "description": "A leading UAE university with affordable tuition and diverse programs.",
        "ranking": 800,
        "tuition_min_usd": 5000,
        "tuition_max_usd": 12000,
    },
    {
        "name": "Bilkent University",
        "country": "Turkey",
        "city": "Ankara",
        "website": "https://www.bilkent.edu.tr",
        "description": "Turkey's first private university with excellent research output.",
        "ranking": 550,
        "tuition_min_usd": 7000,
        "tuition_max_usd": 13000,
    },
]

MAJORS = [
    # MIT
    {"uni": "Massachusetts Institute of Technology", "name": "Computer Science", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 57000, "duration_years": 4.0, "description": "World-class CS program covering algorithms, systems, and AI."},
    {"uni": "Massachusetts Institute of Technology", "name": "Artificial Intelligence", "category": "DATA_AI", "degree_level": "Master", "language": "English", "tuition_usd": 59000, "duration_years": 2.0, "description": "Cutting-edge AI research with top faculty in machine learning."},
    {"uni": "Massachusetts Institute of Technology", "name": "Data Science", "category": "DATA_AI", "degree_level": "Master", "language": "English", "tuition_usd": 59000, "duration_years": 1.5, "description": "Advanced data science with focus on real-world applications."},
    {"uni": "Massachusetts Institute of Technology", "name": "Cybersecurity", "category": "IT_ENGINEERING", "degree_level": "Master", "language": "English", "tuition_usd": 59000, "duration_years": 1.5, "description": "Deep dive into network security, cryptography, and cyber defense."},
    # University of Toronto
    {"uni": "University of Toronto", "name": "Software Engineering", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 42000, "duration_years": 4.0, "description": "Engineering-focused CS program with co-op opportunities."},
    {"uni": "University of Toronto", "name": "Business Administration", "category": "BUSINESS", "degree_level": "Bachelor", "language": "English", "tuition_usd": 38000, "duration_years": 4.0, "description": "Top-ranked Rotman commerce program with finance and strategy streams."},
    {"uni": "University of Toronto", "name": "Psychology", "category": "SOCIAL_SCIENCES", "degree_level": "Bachelor", "language": "English", "tuition_usd": 35000, "duration_years": 4.0, "description": "Comprehensive psychology program with strong research opportunities."},
    {"uni": "University of Toronto", "name": "Public Health", "category": "MEDICINE", "degree_level": "Master", "language": "English", "tuition_usd": 40000, "duration_years": 2.0, "description": "Global public health program addressing modern health challenges."},
    # UCL
    {"uni": "University College London", "name": "International Law", "category": "LAW", "degree_level": "Bachelor", "language": "English", "tuition_usd": 32000, "duration_years": 3.0, "description": "Rigorous law program in London's global legal hub."},
    {"uni": "University College London", "name": "Biomedical Science", "category": "MEDICINE", "degree_level": "Bachelor", "language": "English", "tuition_usd": 35000, "duration_years": 3.0, "description": "Combines biology and medicine for cutting-edge research."},
    {"uni": "University College London", "name": "Machine Learning", "category": "DATA_AI", "degree_level": "Master", "language": "English", "tuition_usd": 38000, "duration_years": 1.0, "description": "Intensive ML program at one of the world's AI research hubs."},
    {"uni": "University College London", "name": "Architecture", "category": "DESIGN_CREATIVE", "degree_level": "Bachelor", "language": "English", "tuition_usd": 33000, "duration_years": 3.0, "description": "Creative and technical architecture training in London."},
    # TU Munich
    {"uni": "Technical University of Munich", "name": "Computer Science", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 1000, "duration_years": 3.5, "description": "World-class CS education in Germany — nearly tuition-free."},
    {"uni": "Technical University of Munich", "name": "Informatics", "category": "IT_ENGINEERING", "degree_level": "Master", "language": "English", "tuition_usd": 1500, "duration_years": 2.0, "description": "Advanced computing and software systems — top German university."},
    {"uni": "Technical University of Munich", "name": "Data Engineering and Analytics", "category": "DATA_AI", "degree_level": "Master", "language": "English", "tuition_usd": 1500, "duration_years": 2.0, "description": "Big data and analytics engineering for industry applications."},
    {"uni": "Technical University of Munich", "name": "Biomedical Engineering", "category": "MEDICINE", "degree_level": "Bachelor", "language": "German", "tuition_usd": 1000, "duration_years": 3.5, "description": "Combining engineering and medicine for healthcare innovation."},
    # Koç University
    {"uni": "Koç University", "name": "International Business", "category": "BUSINESS", "degree_level": "Bachelor", "language": "English", "tuition_usd": 12000, "duration_years": 4.0, "description": "Business education with a global focus in Istanbul."},
    {"uni": "Koç University", "name": "Computer Engineering", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 12000, "duration_years": 4.0, "description": "Strong CS and engineering program at Turkey's top private university."},
    {"uni": "Koç University", "name": "International Relations", "category": "SOCIAL_SCIENCES", "degree_level": "Bachelor", "language": "English", "tuition_usd": 11000, "duration_years": 4.0, "description": "Politics, diplomacy and global affairs in one of the world's most strategic cities."},
    # Seoul National University
    {"uni": "Seoul National University", "name": "Computer Science and Engineering", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "Korean", "tuition_usd": 5000, "duration_years": 4.0, "description": "Korea's top CS program — highly competitive and research-intensive."},
    {"uni": "Seoul National University", "name": "Business Administration", "category": "BUSINESS", "degree_level": "Bachelor", "language": "English", "tuition_usd": 6000, "duration_years": 4.0, "description": "World-class business education in the heart of Seoul."},
    {"uni": "Seoul National University", "name": "Medicine", "category": "MEDICINE", "degree_level": "Bachelor", "language": "Korean", "tuition_usd": 7000, "duration_years": 6.0, "description": "Prestigious medical program at Korea's leading university."},
    # University of Malaya
    {"uni": "University of Malaya", "name": "Computer Science", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 5000, "duration_years": 3.0, "description": "Affordable and quality CS education in Southeast Asia."},
    {"uni": "University of Malaya", "name": "Finance", "category": "BUSINESS", "degree_level": "Bachelor", "language": "English", "tuition_usd": 4500, "duration_years": 3.0, "description": "Finance and banking program with links to Malaysia's financial sector."},
    {"uni": "University of Malaya", "name": "Education Studies", "category": "EDUCATION", "degree_level": "Bachelor", "language": "English", "tuition_usd": 3500, "duration_years": 4.0, "description": "Teacher training and education research in Malaysia."},
    # Nazarbayev University
    {"uni": "Nazarbayev University", "name": "Computer Science", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 3000, "duration_years": 4.0, "description": "Modern CS program taught entirely in English in Kazakhstan."},
    {"uni": "Nazarbayev University", "name": "Chemical Engineering", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 3500, "duration_years": 4.0, "description": "Engineering program tied to Kazakhstan's energy sector needs."},
    {"uni": "Nazarbayev University", "name": "Public Policy", "category": "LAW", "degree_level": "Master", "language": "English", "tuition_usd": 5000, "duration_years": 2.0, "description": "Policy and governance for Central Asia's emerging economies."},
    # NYU Abu Dhabi
    {"uni": "New York University Abu Dhabi", "name": "Computer Science", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 53000, "duration_years": 4.0, "description": "Liberal arts CS at a world-class campus with full scholarships available."},
    {"uni": "New York University Abu Dhabi", "name": "Economics", "category": "BUSINESS", "degree_level": "Bachelor", "language": "English", "tuition_usd": 53000, "duration_years": 4.0, "description": "Economics degree in a globally connected UAE campus."},
    {"uni": "New York University Abu Dhabi", "name": "Digital Media", "category": "DESIGN_CREATIVE", "degree_level": "Bachelor", "language": "English", "tuition_usd": 53000, "duration_years": 4.0, "description": "Creative and technical media arts in the UAE."},
    # UBC
    {"uni": "University of British Columbia", "name": "Software Engineering", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 43000, "duration_years": 4.0, "description": "Excellent SE program in Vancouver's tech hub."},
    {"uni": "University of British Columbia", "name": "Applied Mathematics", "category": "DATA_AI", "degree_level": "Bachelor", "language": "English", "tuition_usd": 38000, "duration_years": 4.0, "description": "Math-driven problem solving with applications in science and industry."},
    {"uni": "University of British Columbia", "name": "Sociology", "category": "SOCIAL_SCIENCES", "degree_level": "Bachelor", "language": "English", "tuition_usd": 36000, "duration_years": 4.0, "description": "Understanding society, culture and social structures."},
    # RWTH Aachen
    {"uni": "RWTH Aachen University", "name": "Electrical Engineering", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "German", "tuition_usd": 800, "duration_years": 3.5, "description": "Germany's best engineering university for EE — nearly tuition-free."},
    {"uni": "RWTH Aachen University", "name": "Information Systems", "category": "IT_ENGINEERING", "degree_level": "Master", "language": "English", "tuition_usd": 1200, "duration_years": 2.0, "description": "Business IT and information systems in an English-taught program."},
    {"uni": "RWTH Aachen University", "name": "Data Science", "category": "DATA_AI", "degree_level": "Master", "language": "English", "tuition_usd": 1200, "duration_years": 2.0, "description": "Modern data science with engineering depth at a top German university."},
    # University of Edinburgh
    {"uni": "University of Edinburgh", "name": "Informatics", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 28000, "duration_years": 4.0, "description": "World-renowned CS and AI program in Edinburgh."},
    {"uni": "University of Edinburgh", "name": "Medicine", "category": "MEDICINE", "degree_level": "Bachelor", "language": "English", "tuition_usd": 32000, "duration_years": 6.0, "description": "One of the UK's top medical schools with cutting-edge research."},
    {"uni": "University of Edinburgh", "name": "TESOL", "category": "EDUCATION", "degree_level": "Master", "language": "English", "tuition_usd": 25000, "duration_years": 1.0, "description": "Teaching English to Speakers of Other Languages — world-class program."},
    {"uni": "University of Edinburgh", "name": "Communications", "category": "SOCIAL_SCIENCES", "degree_level": "Bachelor", "language": "English", "tuition_usd": 26000, "duration_years": 4.0, "description": "Media, journalism and communications in a global city."},
    # KAIST
    {"uni": "KAIST", "name": "Computer Science", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 4000, "duration_years": 4.0, "description": "Korea's #1 science & tech university — fully taught in English."},
    {"uni": "KAIST", "name": "Artificial Intelligence", "category": "DATA_AI", "degree_level": "Master", "language": "English", "tuition_usd": 4500, "duration_years": 2.0, "description": "AI research at Asia's top technology institute."},
    {"uni": "KAIST", "name": "Cybersecurity", "category": "IT_ENGINEERING", "degree_level": "Master", "language": "English", "tuition_usd": 4500, "duration_years": 2.0, "description": "Advanced cybersecurity research and engineering."},
    # University of Sharjah
    {"uni": "University of Sharjah", "name": "Graphic Design", "category": "DESIGN_CREATIVE", "degree_level": "Bachelor", "language": "English", "tuition_usd": 8000, "duration_years": 4.0, "description": "Creative design education in the UAE."},
    {"uni": "University of Sharjah", "name": "Marketing", "category": "BUSINESS", "degree_level": "Bachelor", "language": "English", "tuition_usd": 7500, "duration_years": 4.0, "description": "Marketing and business communication in the UAE market."},
    {"uni": "University of Sharjah", "name": "Political Science", "category": "LAW", "degree_level": "Bachelor", "language": "English", "tuition_usd": 7000, "duration_years": 4.0, "description": "Politics and governance with a Middle East perspective."},
    # Bilkent
    {"uni": "Bilkent University", "name": "Computer Engineering", "category": "IT_ENGINEERING", "degree_level": "Bachelor", "language": "English", "tuition_usd": 10000, "duration_years": 4.0, "description": "Turkey's oldest private university with a strong tech focus."},
    {"uni": "Bilkent University", "name": "Animation", "category": "DESIGN_CREATIVE", "degree_level": "Bachelor", "language": "English", "tuition_usd": 9000, "duration_years": 4.0, "description": "Creative animation and digital arts program in Ankara."},
    {"uni": "Bilkent University", "name": "Corporate Law", "category": "LAW", "degree_level": "Bachelor", "language": "Turkish", "tuition_usd": 8000, "duration_years": 4.0, "description": "Turkish and international corporate law education."},
    {"uni": "Bilkent University", "name": "Educational Technology", "category": "EDUCATION", "degree_level": "Master", "language": "English", "tuition_usd": 9000, "duration_years": 2.0, "description": "Technology-enhanced learning design and e-learning systems."},
]


def seed():
    db = SessionLocal()
    try:
        print("Seeding achievements...")
        from app.services.gamification_service import GamificationService
        GamificationService.seed_achievements(db)
        print("  Achievements seeded.")

        print("Seeding universities and majors...")
        uni_count = db.query(University).count()
        if uni_count > 0:
            print(f"  {uni_count} universities already exist — skipping university seed.")
        else:
            uni_map = {}
            for u_data in UNIVERSITIES:
                uni = University(**u_data)
                db.add(uni)
                db.flush()
                uni_map[u_data["name"]] = uni.id

            for m_data in MAJORS:
                uni_name = m_data["uni"]
                uni_id = uni_map.get(uni_name)
                if uni_id:
                    fields = {k: v for k, v in m_data.items() if k != "uni"}
                    major = Major(university_id=uni_id, **fields)
                    db.add(major)

            db.commit()
            print(f"  {len(UNIVERSITIES)} universities and {len(MAJORS)} majors seeded.")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seed data loaded successfully!")
