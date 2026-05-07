import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Alert, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import RoadmapCard from '../components/RoadmapCard';
import { roadmapApi } from '../api/roadmap';
import { assessmentApi } from '../api/assessment';
import { profileApi } from '../api/profile';
import { Roadmap, RootStackParamList } from '../types';
import { useLanguage } from '../i18n/LanguageContext';

type Nav = StackNavigationProp<RootStackParamList, 'Roadmap'>;

const COUNTRIES = ['Germany', 'USA', 'Canada', 'UK', 'Turkey', 'South Korea', 'Malaysia', 'Kazakhstan', 'UAE'];

export default function RoadmapScreen() {
  const navigation = useNavigation<Nav>();
  const { t } = useLanguage();
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [selectedMajor, setSelectedMajor] = useState('Software Engineering');
  const [selectedCountry, setSelectedCountry] = useState('Germany');
  const [availableMajors, setAvailableMajors] = useState<string[]>([]);

  useEffect(() => {
    async function init() {
      try {
        const existing = await roadmapApi.getMyRoadmap().catch(() => null);
        if (existing) { setRoadmap(existing); return; }

        // Prefill from assessment + profile
        const [result, profile] = await Promise.all([
          assessmentApi.getResult().catch(() => null),
          profileApi.getMyProfile().catch(() => null),
        ]);
        if (result?.recommended_majors?.length) {
          setAvailableMajors(result.recommended_majors);
          setSelectedMajor(result.recommended_majors[0]);
        }
        if (profile?.target_country) {
          setSelectedCountry(profile.target_country);
        }
      } finally {
        setLoading(false);
      }
    }
    init();
  }, []);

  async function handleGenerate() {
    setGenerating(true);
    try {
      const r = await roadmapApi.generate(selectedMajor, selectedCountry);
      setRoadmap(r);
    } catch (e: any) {
      Alert.alert(t('error'), e.message);
    } finally {
      setGenerating(false);
    }
  }

  async function handleCompleteStep(stepId: number) {
    try {
      const res = await roadmapApi.completeStep(stepId);
      Alert.alert(t('roadmap_done'), res.message);
      const updated = await roadmapApi.getMyRoadmap();
      setRoadmap(updated);
    } catch (e: any) {
      Alert.alert(t('error'), e.message);
    }
  }

  if (loading) {
    return (
      <SafeAreaView style={s.container}>
        <View style={s.center}><Text style={s.loadingText}>{t('loading')}</Text></View>
      </SafeAreaView>
    );
  }

  if (!roadmap) {
    return (
      <SafeAreaView style={s.container}>
        <ScrollView contentContainerStyle={s.scroll}>
          <Text style={s.emoji}>🗺️</Text>
          <Text style={s.title}>{t('roadmap_title')}</Text>
          <Text style={s.subtitle}>{t('roadmap_subtitle')}</Text>

          <Text style={s.sectionLabel}>{t('roadmap_major')}</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={s.chips}>
            {(availableMajors.length ? availableMajors : ['Software Engineering', 'Cybersecurity', 'Data Science', 'Business Administration']).map((m) => (
              <TouchableOpacity
                key={m}
                style={[s.chip, selectedMajor === m && s.chipActive]}
                onPress={() => setSelectedMajor(m)}
              >
                <Text style={[s.chipText, selectedMajor === m && s.chipTextActive]}>{m}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          <Text style={s.sectionLabel}>{t('roadmap_country')}</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={s.chips}>
            {COUNTRIES.map((c) => (
              <TouchableOpacity
                key={c}
                style={[s.chip, selectedCountry === c && s.chipActive]}
                onPress={() => setSelectedCountry(c)}
              >
                <Text style={[s.chipText, selectedCountry === c && s.chipTextActive]}>{c}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          <View style={s.preview}>
            <Text style={s.previewText}>📚 {selectedMajor}</Text>
            <Text style={s.previewText}>🌍 {selectedCountry}</Text>
          </View>

          <Button title={t('roadmap_generate')} onPress={handleGenerate} loading={generating} style={s.btn} />
        </ScrollView>
      </SafeAreaView>
    );
  }

  const completed = roadmap.steps.filter((step) => step.is_completed).length;
  const total = roadmap.steps.length;
  const progressPct = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <SafeAreaView style={s.container}>
      <ScrollView contentContainerStyle={s.scroll}>
        <Text style={s.roadmapTitle}>{roadmap.roadmap_title}</Text>
        <View style={s.progressRow}>
          <Text style={s.progressText}>{completed}/{total} {t('roadmap_progress')}</Text>
          <Text style={s.progressPct}>{progressPct}%</Text>
        </View>
        <View style={s.progressBar}>
          <View style={[s.progressFill, { width: `${progressPct}%` as any }]} />
        </View>
        {roadmap.roadmap_summary && (
          <Text style={s.summary}>{roadmap.roadmap_summary}</Text>
        )}
        {roadmap.steps.map((step) => (
          <RoadmapCard key={step.id} step={step} onComplete={() => handleCompleteStep(step.id)} />
        ))}
        <Button
          title={t('roadmap_daily')}
          variant="secondary"
          onPress={() => navigation.navigate('DailyTasks')}
          style={s.btn}
        />
        <Button
          title="🔄 Создать новый план"
          variant="outline"
          onPress={() => setRoadmap(null)}
          style={s.btn}
        />
      </ScrollView>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  loadingText: { color: '#94A3B8', fontSize: 16 },
  scroll: { padding: 24, paddingBottom: 48 },
  emoji: { fontSize: 64, textAlign: 'center', marginBottom: 16 },
  title: { color: '#F8FAFC', fontSize: 26, fontWeight: '900', marginBottom: 8 },
  subtitle: { color: '#94A3B8', fontSize: 14, marginBottom: 24, lineHeight: 22 },
  sectionLabel: { color: '#94A3B8', fontSize: 13, fontWeight: '700', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 0.5 },
  chips: { marginBottom: 20 },
  chip: { backgroundColor: '#1E293B', borderRadius: 20, paddingHorizontal: 16, paddingVertical: 8, marginRight: 8, borderWidth: 1, borderColor: '#334155' },
  chipActive: { backgroundColor: '#6366F1', borderColor: '#6366F1' },
  chipText: { color: '#94A3B8', fontWeight: '600', fontSize: 13 },
  chipTextActive: { color: '#fff' },
  preview: { backgroundColor: '#1E293B', borderRadius: 16, padding: 16, marginBottom: 24, gap: 8 },
  previewText: { color: '#A5B4FC', fontSize: 15, fontWeight: '600' },
  btn: { marginTop: 12 },
  roadmapTitle: { color: '#F8FAFC', fontSize: 22, fontWeight: '900', marginBottom: 8 },
  progressRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 6 },
  progressText: { color: '#6366F1', fontSize: 13, fontWeight: '700' },
  progressPct: { color: '#4ADE80', fontSize: 13, fontWeight: '700' },
  progressBar: { height: 8, backgroundColor: '#334155', borderRadius: 4, overflow: 'hidden', marginBottom: 16 },
  progressFill: { height: '100%', backgroundColor: '#6366F1', borderRadius: 4 },
  summary: { color: '#94A3B8', fontSize: 14, lineHeight: 22, marginBottom: 20 },
});
