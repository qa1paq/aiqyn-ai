import React, { useState } from 'react';
import { Text, TextInput, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import KeyboardView from '../components/KeyboardView';
import { authApi } from '../api/auth';
import { tokenStorage } from '../storage/tokenStorage';
import { useLanguage } from '../i18n/LanguageContext';
import { RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'Login'>;

export default function LoginScreen() {
  const navigation = useNavigation<Nav>();
  const { t } = useLanguage();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    setLoading(true);
    try {
      const res = await authApi.login(email.trim(), password);
      await tokenStorage.save(res.access_token);
      navigation.reset({ index: 0, routes: [{ name: 'AssessmentIntro' }] });
    } catch (e: any) {
      Alert.alert(t('login_error'), e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardView scrollable={false}>
      <TouchableOpacity style={s.back} onPress={() => navigation.goBack()}>
        <Text style={s.backText}>{t('back')}</Text>
      </TouchableOpacity>
      <Text style={s.title}>{t('login_title')}</Text>
      <Text style={s.subtitle}>{t('login_subtitle')}</Text>

      <Text style={s.label}>{t('register_email')}</Text>
      <TextInput
        style={s.input}
        placeholder="you@email.com"
        placeholderTextColor="#475569"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
        returnKeyType="next"
      />
      <Text style={s.label}>{t('register_password')}</Text>
      <TextInput
        style={s.input}
        placeholder="••••••••"
        placeholderTextColor="#475569"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        returnKeyType="done"
        onSubmitEditing={handleLogin}
      />

      <Button title={t('login_btn')} onPress={handleLogin} loading={loading} style={s.btn} />

      <TouchableOpacity onPress={() => navigation.navigate('Register')} style={s.row}>
        <Text style={s.link}>
          {t('login_no_account')} <Text style={s.linkAccent}>{t('login_register')}</Text>
        </Text>
      </TouchableOpacity>
    </KeyboardView>
  );
}

const s = StyleSheet.create({
  back: { marginBottom: 32 },
  backText: { color: '#6366F1', fontSize: 16 },
  title: { color: '#F8FAFC', fontSize: 28, fontWeight: '900', marginBottom: 8 },
  subtitle: { color: '#94A3B8', fontSize: 15, marginBottom: 32 },
  label: { color: '#94A3B8', fontSize: 13, fontWeight: '600', marginBottom: 6 },
  input: {
    backgroundColor: '#1E293B',
    borderRadius: 14,
    padding: 16,
    color: '#F8FAFC',
    fontSize: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#334155',
  },
  btn: { marginTop: 8, marginBottom: 20 },
  row: { alignItems: 'center' },
  link: { color: '#64748B', fontSize: 14 },
  linkAccent: { color: '#6366F1', fontWeight: '700' },
});
