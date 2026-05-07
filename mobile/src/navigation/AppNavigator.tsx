import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import WelcomeScreen from '../screens/WelcomeScreen';
import RegisterScreen from '../screens/RegisterScreen';
import LoginScreen from '../screens/LoginScreen';
import ProfileSetupScreen from '../screens/ProfileSetupScreen';
import AssessmentIntroScreen from '../screens/AssessmentIntroScreen';
import AssessmentQuestionScreen from '../screens/AssessmentQuestionScreen';
import AssessmentResultScreen from '../screens/AssessmentResultScreen';
import RecommendedMajorsScreen from '../screens/RecommendedMajorsScreen';
import UniversitiesScreen from '../screens/UniversitiesScreen';
import UniversityDetailScreen from '../screens/UniversityDetailScreen';
import MatchingFeedScreen from '../screens/MatchingFeedScreen';
import MatchProfileScreen from '../screens/MatchProfileScreen';
import RoadmapScreen from '../screens/RoadmapScreen';
import DailyTasksScreen from '../screens/DailyTasksScreen';
import AchievementsScreen from '../screens/AchievementsScreen';
import SettingsScreen from '../screens/SettingsScreen';
import { RootStackParamList } from '../types';

const Stack = createStackNavigator<RootStackParamList>();

const screenOptions = {
  headerStyle: { backgroundColor: '#0F172A' },
  headerTintColor: '#6366F1',
  headerTitleStyle: { color: '#F8FAFC', fontWeight: '700' as const },
  cardStyle: { backgroundColor: '#0F172A' },
};

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Welcome" screenOptions={screenOptions}>
        <Stack.Screen name="Welcome" component={WelcomeScreen} options={{ headerShown: false }} />
        <Stack.Screen name="Register" component={RegisterScreen} options={{ headerShown: false }} />
        <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
        <Stack.Screen name="ProfileSetup" component={ProfileSetupScreen} options={{ title: 'Мой профиль' }} />
        <Stack.Screen name="AssessmentIntro" component={AssessmentIntroScreen} options={{ headerShown: false }} />
        <Stack.Screen name="AssessmentQuestion" component={AssessmentQuestionScreen} options={{ title: 'Тест', headerLeft: () => null }} />
        <Stack.Screen name="AssessmentResult" component={AssessmentResultScreen} options={{ title: 'Результаты', headerLeft: () => null }} />
        <Stack.Screen name="RecommendedMajors" component={RecommendedMajorsScreen} options={{ title: 'Специальности для тебя' }} />
        <Stack.Screen name="Universities" component={UniversitiesScreen} options={{ title: 'Университеты' }} />
        <Stack.Screen name="UniversityDetail" component={UniversityDetailScreen} options={{ title: '' }} />
        <Stack.Screen name="MatchingFeed" component={MatchingFeedScreen} options={{ title: 'Найти студентов' }} />
        <Stack.Screen name="MatchProfile" component={MatchProfileScreen} options={{ title: 'Профиль студента' }} />
        <Stack.Screen name="Roadmap" component={RoadmapScreen} options={{ title: 'Мой план' }} />
        <Stack.Screen name="DailyTasks" component={DailyTasksScreen} options={{ title: 'Задачи на сегодня' }} />
        <Stack.Screen name="Achievements" component={AchievementsScreen} options={{ title: 'Достижения' }} />
        <Stack.Screen name="Settings" component={SettingsScreen} options={{ title: 'Настройки' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
