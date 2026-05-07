import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import Card from '../components/Card';
import { universitiesApi } from '../api/universities';
import { University, RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'UniversityDetail'>;
type RouteType = RouteProp<RootStackParamList, 'UniversityDetail'>;

const FLAG: Record<string, string> = { USA: '🇺🇸', Canada: '🇨🇦', UK: '🇬🇧', Germany: '🇩🇪', Turkey: '🇹🇷', 'South Korea': '🇰🇷', Malaysia: '🇲🇾', Kazakhstan: '🇰🇿', UAE: '🇦🇪' };

export default function UniversityDetailScreen() {
  const navigation = useNavigation<Nav>();
  const route = useRoute<RouteType>();
  const [university, setUniversity] = useState<University | null>(null);
  const [loading, setLoading] = useState(true);
  const [choosing, setChoosing] = useState(false);

  useEffect(() => {
    universitiesApi.getUniversity(route.params.universityId)
      .then(setUniversity)
      .catch((e) => Alert.alert('Ошибка', e.message))
      .finally(() => setLoading(false));
  }, [route.params.universityId]);

  async function handleChoose() {
    if (!university) return;
    setChoosing(true);
    try {
      await universitiesApi.chooseUniversity(university.id);
      Alert.alert('Добавлено! 🎉', 'Университет добавлен в твой список. +100 XP!', [
        { text: 'Найти студентов', onPress: () => navigation.navigate('MatchingFeed') },
        { text: 'Мой план поступления', onPress: () => navigation.navigate('Roadmap') },
      ]);
    } catch (e: any) {
      Alert.alert('Ошибка', e.message);
    } finally {
      setChoosing(false);
    }
  }

  if (loading || !university) {
    return <SafeAreaView style={s.container}><View style={s.center}><Text style={s.loadingText}>Загрузка...</Text></View></SafeAreaView>;
  }

  const flag = FLAG[university.country] ?? '🌍';
  const tuition = university.tuition_min_usd === 0
    ? 'Бесплатно'
    : university.tuition_min_usd
    ? `$${(university.tuition_min_usd / 1000).toFixed(0)}k–$${(university.tuition_max_usd! / 1000).toFixed(0)}k/год`
    : 'Уточнить';

  return (
    <SafeAreaView style={s.container}>
      <ScrollView contentContainerStyle={s.scroll}>
        <Text style={s.flag}>{flag}</Text>
        <Text style={s.name}>{university.name}</Text>
        <Text style={s.location}>{university.city}, {university.country}</Text>
        <View style={s.stats}>
          {university.ranking && (
            <View style={s.stat}><Text style={s.statValue}>#{university.ranking}</Text><Text style={s.statLabel}>Рейтинг</Text></View>
          )}
          <View style={s.stat}><Text style={s.statValue}>{tuition}</Text><Text style={s.statLabel}>В год</Text></View>
        </View>
        {university.description && <Card><Text style={s.description}>{university.description}</Text></Card>}
        <Text style={s.sectionTitle}>Доступные программы</Text>
        {university.majors?.map((major) => (
          <Card key={major.id} style={s.majorCard}>
            <Text style={s.majorName}>{major.name}</Text>
            <Text style={s.majorMeta}>{major.degree_level} · {major.language} · {major.duration_years} лет</Text>
            {major.tuition_usd && <Text style={s.majorTuition}>${(major.tuition_usd / 1000).toFixed(0)}k/год</Text>}
          </Card>
        ))}
        <Button title="Выбрать университет 🎯" onPress={handleChoose} loading={choosing} style={s.btn} />
        <Button title="Найти таких же студентов" variant="secondary" onPress={() => navigation.navigate('MatchingFeed')} style={s.btn} />
      </ScrollView>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  loadingText: { color: '#94A3B8' },
  scroll: { padding: 24, paddingBottom: 48 },
  flag: { fontSize: 56, marginBottom: 12 },
  name: { color: '#F8FAFC', fontSize: 22, fontWeight: '900', marginBottom: 4 },
  location: { color: '#64748B', fontSize: 15, marginBottom: 20 },
  stats: { flexDirection: 'row', gap: 16, marginBottom: 20 },
  stat: { backgroundColor: '#1E293B', borderRadius: 14, padding: 14, flex: 1, alignItems: 'center' },
  statValue: { color: '#6366F1', fontSize: 20, fontWeight: '900' },
  statLabel: { color: '#64748B', fontSize: 12, marginTop: 2 },
  description: { color: '#CBD5E1', fontSize: 14, lineHeight: 22 },
  sectionTitle: { color: '#94A3B8', fontSize: 13, fontWeight: '700', marginVertical: 12, textTransform: 'uppercase', letterSpacing: 1 },
  majorCard: { marginVertical: 4 },
  majorName: { color: '#F8FAFC', fontWeight: '700', fontSize: 15 },
  majorMeta: { color: '#64748B', fontSize: 13, marginTop: 2 },
  majorTuition: { color: '#4ADE80', fontSize: 13, marginTop: 4, fontWeight: '600' },
  btn: { marginTop: 12 },
});
