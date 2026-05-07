export interface User {
  id: number;
  email: string;
  full_name: string;
  created_at: string;
  updated_at: string;
}

export interface Profile {
  id: number;
  user_id: number;
  age: number | null;
  grade: number | null;
  city: string | null;
  country: string | null;
  native_language: string | null;
  english_level: string | null;
  target_country: string | null;
  budget_usd: number | null;
  preferred_study_language: string | null;
  interests: string[] | null;
  about: string | null;
  created_at: string;
  updated_at: string;
}

export interface AssessmentOption {
  value: string;
  label: string;
  weights: Record<string, number>;
}

export interface AssessmentQuestion {
  question_key: string;
  text: string;
  options: AssessmentOption[];
}

export interface AssessmentResult {
  id: number;
  user_id: number;
  raw_scores: Record<string, number>;
  normalized_scores: Record<string, number>;
  top_categories: string[];
  recommended_majors: string[];
  profile_summary: string | null;
  answers: Record<string, string>;
  created_at: string;
  updated_at: string;
}

export interface Major {
  id: number;
  university_id: number;
  name: string;
  category: string;
  degree_level: string;
  language: string;
  tuition_usd: number | null;
  duration_years: number | null;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface University {
  id: number;
  name: string;
  country: string;
  city: string;
  website: string | null;
  description: string | null;
  ranking: number | null;
  tuition_min_usd: number | null;
  tuition_max_usd: number | null;
  created_at: string;
  updated_at: string;
  majors?: Major[];
}

export interface MatchUser {
  user_id: number;
  full_name: string;
  city: string | null;
  country: string | null;
  target_country: string | null;
  english_level: string | null;
  match_score: number;
  top_categories: string[] | null;
  recommended_majors: string[] | null;
}

export interface RoadmapStep {
  id: number;
  roadmap_id: number;
  month_number: number;
  week_number: number | null;
  title: string;
  description: string | null;
  tasks: string[] | null;
  xp_reward: number;
  is_completed: boolean;
  created_at: string;
}

export interface Roadmap {
  id: number;
  user_id: number;
  target_major: string;
  target_country: string;
  roadmap_title: string;
  roadmap_summary: string | null;
  duration_months: number;
  created_at: string;
  updated_at: string;
  steps: RoadmapStep[];
}

export interface Gamification {
  id: number;
  user_id: number;
  total_xp: number;
  level: number;
  current_streak: number;
  longest_streak: number;
  last_active_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface Achievement {
  id: number;
  code: string;
  title: string;
  description: string | null;
  xp_reward: number;
  unlocked: boolean;
  unlocked_at: string | null;
}

export type RootStackParamList = {
  Welcome: undefined;
  Register: undefined;
  Login: undefined;
  ProfileSetup: undefined;
  AssessmentIntro: undefined;
  AssessmentQuestion: undefined;
  AssessmentResult: undefined;
  RecommendedMajors: undefined;
  Universities: undefined;
  UniversityDetail: { universityId: number };
  MatchingFeed: undefined;
  MatchProfile: { matchUser: MatchUser };
  Roadmap: undefined;
  DailyTasks: undefined;
  Achievements: undefined;
  Settings: undefined;
};
