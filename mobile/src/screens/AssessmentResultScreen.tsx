import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import ScoreCard from '../components/ScoreCard';
import XPBadge from '../components/XPBadge';
import { assessmentApi } from '../api/assessment';
import { AssessmentResult, RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'AssessmentResult'>;

const CATEGORY_LABELS: Record<string, string> = {
  IT_ENGINEERING: '💻 Технологии и инженерия',
  DATA_AI: '🤖 Data Science и ИИ',
  MEDICINE: '🩺 Медицина',
  BUSINESS: '📈 Бизнес',
  LAW: '⚖️ Право',
  DESIGN_CREATIVE: '🎨 Дизайн',
  SOCIAL_SCIENCES: '🌍 Социальные науки',
  EDUCATION: '📚 Образование',
};

export default function AssessmentResultScreen() {
  const navigation = useNavigation<Nav>();
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    assessmentApi.getResult()
      .then(setResult)
      .catch((e) => Alert.alert('Ошибка', e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !result) {
    return (
      <SafeAreaView style={s.container}>
        <View style={s.center}><Text style={s.loadingText}>Анализируем твои ответы...</Text></View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={s.container}>
      <ScrollView contentContainerStyle={s.scroll}>
        <View style={s.header}>
          <Text style={s.emoji}>🎯</Text>
          <Text style={s.title}>Твои результаты!</Text>
          <XPBadge xp={250} size="lg" />
        </View>
        {result.profile_summary && (
          <View style={s.summaryCard}>
            <Text style={s.summaryText}>{result.profile_summary}</Text>
          </View>
        )}
        <Text style={s.sectionTitle}>Топ направления</Text>
        {result.top_categories.map((cat, i) => (
          <View key={cat} style={[s.categoryRow, i === 0 && s.topCategory]}>
            <Text style={s.rank}>#{i + 1}</Text>
            <Text style={s.categoryName}>{CATEGORY_LABELS[cat] ?? cat}</Text>
            <Text style={s.categoryScore}>{result.normalized_scores[cat]?.toFixed(0)}%</Text>
          </View>
        ))}
        <Text style={s.sectionTitle}>Распределение баллов</Text>
        <View style={s.scoreCard}>
          <ScoreCard scores={result.normalized_scores} top={6} />
        </View>
        <Text style={s.sectionTitle}>Рекомендованные специальности</Text>
        <View style={s.majors}>
          {result.recommended_majors.map((major) => (
            <View key={major} style={s.majorBadge}>
              <Text style={s.majorText}>{major}</Text>
            </View>
          ))}
        </View>
        <Button title="Найти университеты 🏛️" onPress={() => navigation.navigate('Universities')} style={s.btn} />
        <Button title="Рекомендованные специальности" variant="secondary" onPress={() => navigation.navigate('RecommendedMajors')} style={s.btn} />
      </ScrollView>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  loadingText: { color: '#94A3B8', fontSize: 16 },
  scroll: { padding: 24, paddingBottom: 48 },
  header: { alignItems: 'center', marginBottom: 24 },
  emoji: { fontSize: 64, marginBottom: 8 },
  title: { color: '#F8FAFC', fontSize: 28, fontWeight: '900', marginBottom: 12 },
  summaryCard: { backgroundColor: '#1E293B', borderRadius: 20, padding: 16, marginBottom: 24 },
  summaryText: { color: '#CBD5E1', fontSize: 14, lineHeight: 22 },
  sectionTitle: { color: '#94A3B8', fontSize: 13, fontWeight: '700', marginBottom: 12, marginTop: 8, textTransform: 'uppercase', letterSpacing: 1 },
  categoryRow: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#1E293B', borderRadius: 14, padding: 14, marginBottom: 8 },
  topCategory: { borderWidth: 2, borderColor: '#6366F1' },
  rank: { color: '#6366F1', fontWeight: '800', fontSize: 16, width: 32 },
  categoryName: { flex: 1, color: '#F8FAFC', fontWeight: '700', fontSize: 15 },
  categoryScore: { color: '#4ADE80', fontWeight: '700' },
  scoreCard: { backgroundColor: '#1E293B', borderRadius: 20, padding: 16, marginBottom: 24 },
  majors: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 28 },
  majorBadge: { backgroundColor: '#312E81', borderRadius: 10, paddingHorizontal: 12, paddingVertical: 8 },
  majorText: { color: '#A5B4FC', fontSize: 13, fontWeight: '600' },
  btn: { marginBottom: 12 },
});
