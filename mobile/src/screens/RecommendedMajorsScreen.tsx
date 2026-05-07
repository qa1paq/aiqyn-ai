import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import Card from '../components/Card';
import { universitiesApi } from '../api/universities';
import { Major, RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'RecommendedMajors'>;

const CATEGORY_COLORS: Record<string, string> = {
  IT_ENGINEERING: '#6366F1', DATA_AI: '#8B5CF6', MEDICINE: '#EF4444',
  BUSINESS: '#F59E0B', LAW: '#10B981', DESIGN_CREATIVE: '#EC4899',
  SOCIAL_SCIENCES: '#3B82F6', EDUCATION: '#14B8A6',
};

const DEGREE_LABELS: Record<string, string> = { Bachelor: 'Бакалавриат', Master: 'Магистратура' };

export default function RecommendedMajorsScreen() {
  const navigation = useNavigation<Nav>();
  const [majors, setMajors] = useState<Major[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    universitiesApi.getRecommendedMajors()
      .then(setMajors)
      .catch((e) => Alert.alert('Ошибка', e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <Text style={s.title}>Рекомендованные специальности</Text>
        <Text style={s.subtitle}>На основе твоих результатов теста</Text>
      </View>
      <FlatList
        data={majors}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={s.list}
        ListEmptyComponent={<Text style={s.empty}>{loading ? 'Загрузка...' : 'Специальности не найдены'}</Text>}
        renderItem={({ item }) => (
          <Card>
            <View style={s.row}>
              <View style={[s.dot, { backgroundColor: CATEGORY_COLORS[item.category] ?? '#6366F1' }]} />
              <View style={{ flex: 1 }}>
                <Text style={s.majorName}>{item.name}</Text>
                <Text style={s.degree}>{DEGREE_LABELS[item.degree_level] ?? item.degree_level} · {item.language} · {item.duration_years} лет</Text>
                {item.tuition_usd ? (
                  <Text style={s.tuition}>${(item.tuition_usd / 1000).toFixed(0)}k/год</Text>
                ) : (
                  <Text style={s.free}>Бесплатно</Text>
                )}
              </View>
            </View>
          </Card>
        )}
        ListFooterComponent={
          <Button title="Найти университеты 🏛️" onPress={() => navigation.navigate('Universities')} style={{ margin: 16 }} />
        }
      />
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  header: { padding: 24, paddingBottom: 8 },
  title: { color: '#F8FAFC', fontSize: 24, fontWeight: '900' },
  subtitle: { color: '#64748B', fontSize: 14, marginTop: 4 },
  list: { paddingHorizontal: 16 },
  row: { flexDirection: 'row', alignItems: 'flex-start', gap: 12 },
  dot: { width: 12, height: 12, borderRadius: 6, marginTop: 4 },
  majorName: { color: '#F8FAFC', fontSize: 15, fontWeight: '700' },
  degree: { color: '#64748B', fontSize: 13, marginTop: 2 },
  tuition: { color: '#4ADE80', fontSize: 13, marginTop: 2, fontWeight: '600' },
  free: { color: '#4ADE80', fontSize: 13, marginTop: 2, fontWeight: '600' },
  empty: { textAlign: 'center', color: '#64748B', padding: 48 },
});
