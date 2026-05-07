# AIQYN AI

AI-powered career guidance and university admission platform for Grade 11 graduates going abroad.

## Quick Start

### Backend
```bash
cd backend

# 1. Create PostgreSQL database
# CREATE DATABASE aiqyn_db;

# 2. Setup
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt

# 3. Configure .env
cp .env.example .env
# Edit DATABASE_URL in .env

# 4. Run migrations
alembic upgrade head

# 5. Load seed data (15 universities, 50+ majors, achievements)
python -m app.seed.seed_data

# 6. Start server
uvicorn app.main:app --reload
# → http://localhost:8000/docs
```

### Mobile
```bash
cd mobile
npm install
npx expo start
# Scan QR code with Expo Go app
```

## Architecture

```
User answers 30 questions
         ↓
Deterministic rule-based scoring
(8 categories: IT, AI, Medicine, Business, Law, Design, Social, Education)
         ↓
Top 3 categories + recommended majors
         ↓
Personalized university recommendations
(filtered by target_country, budget, language)
         ↓
Mock AI generates roadmap + daily tasks
(MockAIService — swap for OpenAI/Claude later)
         ↓
Gamification: XP, Levels, Streaks, Achievements
```

## Tech Stack
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT
- **Frontend**: React Native, Expo, TypeScript, React Navigation
- **AI**: MockAIService (ready to plug in OpenAI/Claude/Gemini)
