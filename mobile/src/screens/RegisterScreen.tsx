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

type Nav = StackNavigationProp<RootStackParamList, 'Register'>;

export default function RegisterScreen() {
  const navigation = useNavigation<Nav>();
  const { t } = useLanguage();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleRegister() {
    if (!fullName.trim() || !email.trim() || !password.trim()) {
      Alert.alert(t('error'), t('register_error_fields'));
      return;
    }
    setLoading(true);
    try {
      const res = await authApi.register(email.trim(), password, fullName.trim());
      await tokenStorage.save(res.access_token);
      navigation.reset({ index: 0, routes: [{ name: 'ProfileSetup' }] });
    } catch (e: any) {
      Alert.alert(t('register_error_title'), e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardView>
      <TouchableOpacity style={s.back} onPress={() => navigation.goBack()}>
        <Text style={s.backText}>{t('back')}</Text>
      </TouchableOpacity>
      <Text style={s.title}>{t('register_title')}</Text>
      <Text style={s.subtitle}>{t('register_subtitle')}</Text>

      <Text style={s.label}>{t('register_name')}</Text>
      <TextInput
        style={s.input}
        placeholder="Азат Кошан"
        placeholderTextColor="#475569"
        value={fullName}
        onChangeText={setFullName}
        autoCapitalize="words"
        returnKeyType="next"
      />
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
        placeholder={t('register_password_hint')}
        placeholderTextColor="#475569"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        returnKeyType="done"
        onSubmitEditing={handleRegister}
      />

      <Button title={t('register_btn')} onPress={handleRegister} loading={loading} style={s.btn} />

      <TouchableOpacity onPress={() => navigation.navigate('Login')} style={s.loginRow}>
        <Text style={s.loginLink}>
          {t('register_have_account')} <Text style={s.link}>{t('register_login')}</Text>
        </Text>
      </TouchableOpacity>
    </KeyboardView>
  );
}

const s = StyleSheet.create({
  back: { marginBottom: 24 },
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
  loginRow: { alignItems: 'center' },
  loginLink: { color: '#64748B', fontSize: 14 },
  link: { color: '#6366F1', fontWeight: '700' },
});
