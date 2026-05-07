import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import ProgressBar from '../components/ProgressBar';
import Button from '../components/Button';
import { assessmentApi } from '../api/assessment';
import { useLanguage } from '../i18n/LanguageContext';
import { AssessmentQuestion, RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'AssessmentQuestion'>;

export default function AssessmentQuestionScreen() {
  const navigation = useNavigation<Nav>();
  const { language, t } = useLanguage();
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [selected, setSelected] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    assessmentApi.getQuestions(language)
      .then(setQuestions)
      .catch((e) => Alert.alert(t('error'), e.message))
      .finally(() => setLoading(false));
  }, [language]);

  if (loading || questions.length === 0) {
    return (
      <SafeAreaView style={s.container}>
        <View style={s.center}><Text style={s.loadingText}>{t('assessment_loading')}</Text></View>
      </SafeAreaView>
    );
  }

  const question = questions[currentIndex];
  const isLast = currentIndex === questions.length - 1;

  async function handleNext() {
    if (!selected) return;
    const newAnswers = { ...answers, [question.question_key]: selected };
    setAnswers(newAnswers);
    if (isLast) {
      setSubmitting(true);
      try {
        await assessmentApi.submitAnswers(newAnswers, language);
        navigation.reset({ index: 0, routes: [{ name: 'AssessmentResult' }] });
      } catch (e: any) {
        Alert.alert(t('error'), e.message);
        setSubmitting(false);
      }
      return;
    }
    setCurrentIndex(currentIndex + 1);
    setSelected(null);
  }

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <Text style={s.counter}>{currentIndex + 1} / {questions.length}</Text>
        <ProgressBar current={currentIndex + 1} total={questions.length} showLabel={false} />
      </View>
      <ScrollView contentContainerStyle={s.scroll}>
        <Text style={s.question}>{question.text}</Text>
        <View style={s.options}>
          {question.options.map((opt) => (
            <TouchableOpacity
              key={opt.value}
              style={[s.option, selected === opt.value && s.optionSelected]}
              onPress={() => setSelected(opt.value)}
              activeOpacity={0.8}
            >
              <Text style={[s.optionText, selected === opt.value && s.optionTextSelected]}>
                {opt.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
      <View style={s.footer}>
        <Button
          title={isLast ? t('assessment_finish') : t('assessment_continue')}
          onPress={handleNext}
          disabled={!selected}
          loading={submitting}
        />
      </View>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  loadingText: { color: '#94A3B8', fontSize: 16 },
  header: { paddingHorizontal: 24, paddingTop: 16, paddingBottom: 8 },
  counter: { color: '#6366F1', fontWeight: '700', fontSize: 13, marginBottom: 6 },
  scroll: { padding: 24, paddingBottom: 8 },
  question: { color: '#F8FAFC', fontSize: 22, fontWeight: '800', lineHeight: 30, marginBottom: 28 },
  options: { gap: 12 },
  option: { backgroundColor: '#1E293B', borderRadius: 16, padding: 18, borderWidth: 2, borderColor: '#334155' },
  optionSelected: { borderColor: '#6366F1', backgroundColor: '#1E1B4B' },
  optionText: { color: '#CBD5E1', fontSize: 15, lineHeight: 22 },
  optionTextSelected: { color: '#A5B4FC', fontWeight: '700' },
  footer: { paddingHorizontal: 24, paddingBottom: 32, paddingTop: 16 },
});
