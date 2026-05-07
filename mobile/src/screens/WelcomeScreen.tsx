import React from 'react';
import { View, Text, StyleSheet, StatusBar } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import { useLanguage } from '../i18n/LanguageContext';
import { RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'Welcome'>;

export default function WelcomeScreen() {
  const navigation = useNavigation<Nav>();
  const { t } = useLanguage();

  return (
    <SafeAreaView style={s.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0F172A" />
      <View style={s.content}>
        <Text style={s.emoji}>🌍</Text>
        <Text style={s.title}>{t('welcome_title')}</Text>
        <Text style={s.subtitle}>{t('welcome_subtitle')}</Text>
        <View style={s.features}>
          {[t('welcome_f1'), t('welcome_f2'), t('welcome_f3'), t('welcome_f4')].map((f) => (
            <Text key={f} style={s.feature}>{f}</Text>
          ))}
        </View>
      </View>
      <View style={s.buttons}>
        <Button title={t('welcome_btn_start')} onPress={() => navigation.navigate('Register')} />
        <Button title={t('welcome_btn_login')} variant="outline" onPress={() => navigation.navigate('Login')} style={s.loginBtn} />
      </View>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  content: { flex: 1, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 32 },
  emoji: { fontSize: 72, marginBottom: 16 },
  title: { fontSize: 36, fontWeight: '900', color: '#F8FAFC', letterSpacing: 1 },
  subtitle: { fontSize: 16, color: '#94A3B8', textAlign: 'center', marginTop: 8, marginBottom: 32 },
  features: { gap: 12, width: '100%' },
  feature: { color: '#CBD5E1', fontSize: 16, textAlign: 'center' },
  buttons: { paddingHorizontal: 24, paddingBottom: 32, gap: 12 },
  loginBtn: { marginTop: 4 },
});
