import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { tokenStorage } from '../storage/tokenStorage';
import { useLanguage } from '../i18n/LanguageContext';
import { Language } from '../i18n/translations';
import { RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'Settings'>;

const LANGUAGES: { code: Language; label: string; flag: string }[] = [
  { code: 'ru', label: 'Русский', flag: '🇷🇺' },
  { code: 'en', label: 'English', flag: '🇬🇧' },
  { code: 'kk', label: 'Қазақша', flag: '🇰🇿' },
];

export default function SettingsScreen() {
  const navigation = useNavigation<Nav>();
  const { t, language, setLanguage } = useLanguage();

  async function handleLogout() {
    Alert.alert(t('settings_logout_confirm'), t('settings_logout_msg'), [
      { text: t('settings_logout_cancel'), style: 'cancel' },
      {
        text: t('settings_logout'),
        style: 'destructive',
        onPress: async () => {
          await tokenStorage.remove();
          navigation.reset({ index: 0, routes: [{ name: 'Welcome' }] });
        },
      },
    ]);
  }

  const items: { label: string; screen: keyof RootStackParamList }[] = [
    { label: t('settings_profile'), screen: 'ProfileSetup' },
    { label: t('settings_assessment'), screen: 'AssessmentIntro' },
    { label: t('settings_unis'), screen: 'Universities' },
    { label: t('settings_roadmap'), screen: 'Roadmap' },
    { label: t('settings_achievements'), screen: 'Achievements' },
  ];

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <Text style={s.title}>{t('settings_title')}</Text>
      </View>
      <View style={s.list}>
        {/* Language selector */}
        <View style={s.langSection}>
          <Text style={s.langLabel}>{t('settings_language')}</Text>
          <View style={s.langRow}>
            {LANGUAGES.map((lang) => (
              <TouchableOpacity
                key={lang.code}
                style={[s.langBtn, language === lang.code && s.langBtnActive]}
                onPress={() => setLanguage(lang.code)}
              >
                <Text style={s.langFlag}>{lang.flag}</Text>
                <Text style={[s.langText, language === lang.code && s.langTextActive]}>
                  {lang.label}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {items.map((item) => (
          <TouchableOpacity
            key={item.label}
            style={s.item}
            onPress={() => navigation.navigate(item.screen as any)}
          >
            <Text style={s.itemText}>{item.label}</Text>
            <Text style={s.arrow}>›</Text>
          </TouchableOpacity>
        ))}

        <TouchableOpacity style={[s.item, s.logoutItem]} onPress={handleLogout}>
          <Text style={s.logoutText}>{t('settings_logout')}</Text>
        </TouchableOpacity>
      </View>
      <Text style={s.version}>AIQYN AI v1.0.0</Text>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  header: { padding: 24, paddingBottom: 8 },
  title: { color: '#F8FAFC', fontSize: 24, fontWeight: '900' },
  list: { paddingHorizontal: 16, marginTop: 16 },
  langSection: { backgroundColor: '#1E293B', borderRadius: 14, padding: 16, marginBottom: 10 },
  langLabel: { color: '#94A3B8', fontSize: 13, fontWeight: '600', marginBottom: 12 },
  langRow: { flexDirection: 'row', gap: 8 },
  langBtn: { flex: 1, alignItems: 'center', paddingVertical: 10, borderRadius: 10, backgroundColor: '#0F172A', borderWidth: 1, borderColor: '#334155' },
  langBtnActive: { borderColor: '#6366F1', backgroundColor: '#1E1B4B' },
  langFlag: { fontSize: 22, marginBottom: 4 },
  langText: { color: '#64748B', fontSize: 12, fontWeight: '600' },
  langTextActive: { color: '#A5B4FC' },
  item: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#1E293B', borderRadius: 14, padding: 18, marginBottom: 10 },
  itemText: { color: '#F8FAFC', fontSize: 16 },
  arrow: { color: '#475569', fontSize: 20 },
  logoutItem: { backgroundColor: '#1E1B1B', marginTop: 8 },
  logoutText: { color: '#EF4444', fontSize: 16 },
  version: { color: '#334155', textAlign: 'center', marginTop: 32, fontSize: 12 },
});
