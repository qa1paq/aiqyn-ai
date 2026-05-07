# AIQYN AI — Mobile App

React Native + Expo мобильное приложение.

## Требования
- Node.js 18+
- npm / yarn
- Expo Go app на телефоне (или Android/iOS эмулятор)

## Установка и запуск

```bash
cd mobile
npm install
npx expo start
```

Отсканируй QR-код через приложение **Expo Go** на телефоне.

## Настройка Backend URL

Открой `src/api/client.ts` и замени:
```typescript
const BASE_URL = 'http://localhost:8000/api/v1';
```

На IP твоего компьютера в локальной сети:
```typescript
const BASE_URL = 'http://192.168.1.xxx:8000/api/v1';
```

## Экраны

1. **WelcomeScreen** — Приветствие и навигация
2. **RegisterScreen** — Регистрация
3. **LoginScreen** — Логин
4. **ProfileSetupScreen** — Настройка профиля (+50 XP)
5. **AssessmentIntroScreen** — Intro к квизу
6. **AssessmentQuestionScreen** — 30 вопросов (+250 XP)
7. **AssessmentResultScreen** — Результаты и топ направления
8. **RecommendedMajorsScreen** — Рекомендованные специальности
9. **UniversitiesScreen** — Список университетов
10. **UniversityDetailScreen** — Детали университета (+10 XP за просмотр)
11. **MatchingFeedScreen** — Лента студентов
12. **MatchProfileScreen** — Профиль студента
13. **RoadmapScreen** — Персональный roadmap (+100 XP)
14. **DailyTasksScreen** — Ежедневные задачи
15. **AchievementsScreen** — Достижения и уровень
16. **SettingsScreen** — Настройки и выход
