import React, { useState } from 'react';
import { Text, TextInput, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import { authApi } from '../api/auth';
import { RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'ForgotPassword'>;

export default function ForgotPasswordScreen() {
  const navigation = useNavigation<Nav>();
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSend() {
    if (!email.trim()) {
      Alert.alert('Ошибка', 'Введи email');
      return;
    }
    setLoading(true);
    try {
      await authApi.forgotPassword(email.trim());
      navigation.navigate('ResetPassword', { email: email.trim() });
    } catch (e: any) {
      Alert.alert('Ошибка', e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={s.container}>
      <TouchableOpacity style={s.back} onPress={() => navigation.goBack()}>
        <Text style={s.backText}>← Назад</Text>
      </TouchableOpacity>

      <Text style={s.emoji}>🔐</Text>
      <Text style={s.title}>Забыл пароль?</Text>
      <Text style={s.subtitle}>
        Введи свой email — мы отправим 6-значный код для восстановления пароля.
      </Text>

      <Text style={s.label}>Email</Text>
      <TextInput
        style={s.input}
        placeholder="you@email.com"
        placeholderTextColor="#475569"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
        returnKeyType="done"
        onSubmitEditing={handleSend}
      />

      <Button title="Отправить код" onPress={handleSend} loading={loading} />

      <Text style={s.hint}>
        Код действителен 15 минут
      </Text>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A', padding: 24 },
  back: { marginBottom: 32 },
  backText: { color: '#6366F1', fontSize: 16 },
  emoji: { fontSize: 56, marginBottom: 16 },
  title: { color: '#F8FAFC', fontSize: 26, fontWeight: '900', marginBottom: 8 },
  subtitle: { color: '#94A3B8', fontSize: 15, lineHeight: 24, marginBottom: 32 },
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
  hint: { color: '#475569', fontSize: 13, textAlign: 'center', marginTop: 16 },
});
