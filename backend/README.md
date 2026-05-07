# AIQYN AI — Backend

FastAPI backend для платформы профориентации и поступления в зарубежные вузы.

## Требования
- Python 3.11+
- PostgreSQL 14+

## Установка и запуск

### 1. Создать базу данных PostgreSQL
```sql
CREATE DATABASE aiqyn_db;
```

### 2. Установить зависимости
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Настроить .env
```bash
cp .env.example .env
# Открой .env и укажи свой DATABASE_URL
```

Пример:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/aiqyn_db
SECRET_KEY=aiqyn-super-secret-key-change-in-production-32chars!!
```

### 4. Запустить миграции
```bash
alembic upgrade head
```

### 5. Загрузить seed data
```bash
python -m app.seed.seed_data
```

### 6. Запустить сервер
```bash
uvicorn app.main:app --reload
```

## Проверка

Открой: http://localhost:8000/docs

### Тест API:
```bash
# Регистрация
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","full_name":"Test User"}'

# Список вопросов
curl http://localhost:8000/api/v1/assessment/questions

# Университеты
curl http://localhost:8000/api/v1/universities
```

## API Endpoints

| Method | Endpoint | Описание |
|--------|----------|----------|
| POST | /api/v1/auth/register | Регистрация |
| POST | /api/v1/auth/login | Логин |
| GET  | /api/v1/auth/me | Текущий пользователь |
| GET  | /api/v1/profile/me | Мой профиль |
| PUT  | /api/v1/profile/me | Обновить профиль |
| GET  | /api/v1/assessment/questions | 30 вопросов анкеты |
| POST | /api/v1/assessment/submit | Отправить ответы |
| GET  | /api/v1/assessment/result | Результат |
| GET  | /api/v1/universities | Список университетов |
| GET  | /api/v1/universities/{id} | Детали университета |
| GET  | /api/v1/majors/recommended | Рекомендованные специальности |
| POST | /api/v1/choices/university | Выбрать университет |
| GET  | /api/v1/choices/me | Мои выборы |
| GET  | /api/v1/matching/feed | Лента студентов |
| POST | /api/v1/matching/action | Лайк/пропуск |
| POST | /api/v1/roadmap/generate | Сгенерировать roadmap |
| GET  | /api/v1/roadmap/me | Мой roadmap |
| POST | /api/v1/roadmap/steps/{id}/complete | Завершить шаг |
| GET  | /api/v1/roadmap/daily-tasks | Ежедневные задачи |
| GET  | /api/v1/gamification/me | Мой прогресс |
| GET  | /api/v1/gamification/achievements | Достижения |
| POST | /api/v1/gamification/daily-checkin | Ежедневный чекин |
