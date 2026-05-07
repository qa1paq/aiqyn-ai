import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { KeyboardAvoidingView, Platform } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import { profileApi } from '../api/profile';
import { useLanguage } from '../i18n/LanguageContext';
import { RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'ProfileSetup'>;

const ENGLISH_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
const COUNTRIES = ['США', 'Канада', 'Германия', 'Великобритания', 'Турция', 'Южная Корея', 'Малайзия', 'Казахстан', 'ОАЭ'];
const COUNTRY_MAP: Record<string, string> = {
  'США': 'USA', 'Канада': 'Canada', 'Германия': 'Germany', 'Великобритания': 'UK',
  'Турция': 'Turkey', 'Южная Корея': 'South Korea', 'Малайзия': 'Malaysia',
  'Казахстан': 'Kazakhstan', 'ОАЭ': 'UAE',
};
const LANGUAGES = ['Английский', 'Немецкий', 'Корейский', 'Малайский', 'Турецкий'];
const LANG_MAP: Record<string, string> = {
  'Английский': 'English', 'Немецкий': 'German', 'Корейский': 'Korean',
  'Малайский': 'Malay', 'Турецкий': 'Turkish',
};

function Selector({ label, options, selected, onSelect }: {
  label: string; options: string[]; selected: string; onSelect: (v: string) => void;
}) {
  return (
    <View style={s.selectorGroup}>
      <Text style={s.label}>{label}</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        {options.map((opt) => (
          <TouchableOpacity
            key={opt}
            style={[s.chip, selected === opt && s.chipSelected]}
            onPress={() => onSelect(opt)}
          >
            <Text style={[s.chipText, selected === opt && s.chipTextSelected]}>{opt}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
}

export default function ProfileSetupScreen() {
  const navigation = useNavigation<Nav>();
  const { t } = useLanguage();
  const [age, setAge] = useState('');
  const [city, setCity] = useState('');
  const [country, setCountry] = useState('');
  const [englishLevel, setEnglishLevel] = useState('B1');
  const [targetCountry, setTargetCountry] = useState('Германия');
  const [budget, setBudget] = useState('');
  const [studyLanguage, setStudyLanguage] = useState('Английский');
  const [loading, setLoading] = useState(false);

  async function handleSave() {
    setLoading(true);
    try {
      await profileApi.updateProfile({
        age: age ? parseInt(age) : undefined,
        grade: 11,
        city: city || undefined,
        country: country || undefined,
        english_level: englishLevel,
        target_country: COUNTRY_MAP[targetCountry] ?? targetCountry,
        budget_usd: budget ? parseInt(budget) : undefined,
        preferred_study_language: LANG_MAP[studyLanguage] ?? studyLanguage,
      });
      navigation.reset({ index: 0, routes: [{ name: 'AssessmentIntro' }] });
    } catch (e: any) {
      Alert.alert(t('error'), e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={s.container}>
      <KeyboardAvoidingView
        style={s.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView
          contentContainerStyle={s.scroll}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <Text style={s.title}>{t('profile_title')}</Text>
          <Text style={s.subtitle}>{t('profile_subtitle')}</Text>

          <Text style={s.label}>{t('profile_age')}</Text>
          <TextInput
            style={s.input}
            placeholder="17"
            placeholderTextColor="#475569"
            value={age}
            onChangeText={setAge}
            keyboardType="numeric"
            returnKeyType="next"
          />
          <Text style={s.label}>{t('profile_city')}</Text>
          <TextInput
            style={s.input}
            placeholder="Алматы"
            placeholderTextColor="#475569"
            value={city}
            onChangeText={setCity}
            returnKeyType="next"
          />
          <Text style={s.label}>{t('profile_country')}</Text>
          <TextInput
            style={s.input}
            placeholder="Казахстан"
            placeholderTextColor="#475569"
            value={country}
            onChangeText={setCountry}
            returnKeyType="next"
          />

          <Selector
            label={t('profile_english')}
            options={ENGLISH_LEVELS}
            selected={englishLevel}
            onSelect={setEnglishLevel}
          />
          <Selector
            label={t('profile_target')}
            options={COUNTRIES}
            selected={targetCountry}
            onSelect={setTargetCountry}
          />

          <Text style={s.label}>{t('profile_budget')}</Text>
          <TextInput
            style={s.input}
            placeholder="15000"
            placeholderTextColor="#475569"
            value={budget}
            onChangeText={setBudget}
            keyboardType="numeric"
            returnKeyType="done"
          />

          <Selector
            label={t('profile_language')}
            options={LANGUAGES}
            selected={studyLanguage}
            onSelect={setStudyLanguage}
          />

          <Button title={t('profile_btn')} onPress={handleSave} loading={loading} style={s.btn} />
          <TouchableOpacity onPress={() => navigation.navigate('AssessmentIntro')}>
            <Text style={s.skip}>{t('profile_skip')}</Text>
          </TouchableOpacity>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  flex: { flex: 1 },
  scroll: { padding: 24, paddingBottom: 48 },
  title: { color: '#F8FAFC', fontSize: 26, fontWeight: '900', marginBottom: 8 },
  subtitle: { color: '#94A3B8', fontSize: 14, marginBottom: 28 },
  label: { color: '#94A3B8', fontSize: 13, fontWeight: '600', marginBottom: 6 },
  input: {
    backgroundColor: '#1E293B',
    borderRadius: 14,
    padding: 16,
    color: '#F8FAFC',
    fontSize: 16,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#334155',
  },
  selectorGroup: { marginBottom: 20 },
  chip: {
    backgroundColor: '#1E293B',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  chipSelected: { backgroundColor: '#6366F1', borderColor: '#6366F1' },
  chipText: { color: '#94A3B8', fontWeight: '600' },
  chipTextSelected: { color: '#fff' },
  btn: { marginTop: 8, marginBottom: 16 },
  skip: { color: '#475569', textAlign: 'center', fontSize: 14 },
});
