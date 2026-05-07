import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import { useLanguage } from '../i18n/LanguageContext';
import { RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'AssessmentIntro'>;

export default function AssessmentIntroScreen() {
  const navigation = useNavigation<Nav>();
  const { t } = useLanguage();

  const facts = [
    { e: '⚡', t: t('assessment_f1') },
    { e: '🎯', t: t('assessment_f2') },
    { e: '🏆', t: t('assessment_f3') },
    { e: '🌍', t: t('assessment_f4') },
  ];

  return (
    <SafeAreaView style={s.container}>
      <View style={s.content}>
        <Text style={s.emoji}>🧠</Text>
        <Text style={s.title}>{t('assessment_title')}</Text>
        <Text style={s.subtitle}>{t('assessment_subtitle')}</Text>
        <View style={s.facts}>
          {facts.map((f) => (
            <View key={f.t} style={s.fact}>
              <Text style={s.factEmoji}>{f.e}</Text>
              <Text style={s.factText}>{f.t}</Text>
            </View>
          ))}
        </View>
      </View>
      <View style={s.bottom}>
        <Button title={t('assessment_start')} onPress={() => navigation.navigate('AssessmentQuestion')} />
      </View>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  content: { flex: 1, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 32 },
  emoji: { fontSize: 80, marginBottom: 20 },
  title: { color: '#F8FAFC', fontSize: 32, fontWeight: '900', marginBottom: 12 },
  subtitle: { color: '#94A3B8', fontSize: 16, textAlign: 'center', marginBottom: 40, lineHeight: 24 },
  facts: { width: '100%', gap: 16 },
  fact: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  factEmoji: { fontSize: 24 },
  factText: { color: '#CBD5E1', fontSize: 16 },
  bottom: { paddingHorizontal: 24, paddingBottom: 32 },
});
