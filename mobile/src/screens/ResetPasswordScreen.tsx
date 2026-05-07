import React, { useState, useRef } from 'react';
import { Text, TextInput, StyleSheet, View, Alert, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Button from '../components/Button';
import { authApi } from '../api/auth';
import { RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'ResetPassword'>;
type RouteType = RouteProp<RootStackParamList, 'ResetPassword'>;

export default function ResetPasswordScreen() {
  const navigation = useNavigation<Nav>();
  const route = useRoute<RouteType>();
  const { email } = route.params;

  const [code, setCode] = useState(['', '', '', '', '', '']);
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const inputs = useRef<(TextInput | null)[]>([]);

  function handleCodeChange(val: string, idx: number) {
    const cleaned = val.replace(/\D/g, '').slice(-1);
    const next = [...code];
    next[idx] = cleaned;
    setCode(next);
    if (cleaned && idx < 5) {
      inputs.current[idx + 1]?.focus();
    }
  }

  function handleCodeKeyPress(key: string, idx: number) {
    if (key === 'Backspace' && !code[idx] && idx > 0) {
      inputs.current[idx - 1]?.focus();
    }
  }

  async function handleReset() {
    const fullCode = code.join('');
    if (fullCode.length < 6) {
      Alert.alert('Ошибка', 'Введи 6-значный код');
      return;
    }
    if (newPassword.length < 6) {
      Alert.alert('Ошибка', 'Пароль должен быть минимум 6 символов');
      return;
    }
    if (newPassword !== confirmPassword) {
      Alert.alert('Ошибка', 'Пароли не совпадают');
      return;
    }
    setLoading(true);
    try {
      await authApi.resetPassword(email, fullCode, newPassword);
      Alert.alert('Готово! ✅', 'Пароль успешно изменён. Войди с новым паролем.', [
        { text: 'Войти', onPress: () => navigation.reset({ index: 0, routes: [{ name: 'Login' }] }) },
      ]);
    } catch (e: any) {
      Alert.alert('Ошибка', e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleResend() {
    try {
      await authApi.forgotPassword(email);
      Alert.alert('Отправлено', 'Новый код отправлен на твой email');
      setCode(['', '', '', '', '', '']);
      inputs.current[0]?.focus();
    } catch (e: any) {
      Alert.alert('Ошибка', e.message);
    }
  }

  return (
    <SafeAreaView style={s.container}>
      <TouchableOpacity style={s.back} onPress={() => navigation.goBack()}>
        <Text style={s.backText}>← Назад</Text>
      </TouchableOpacity>

      <Text style={s.emoji}>📩</Text>
      <Text style={s.title}>Введи код</Text>
      <Text style={s.subtitle}>
        Мы отправили 6-значный код на{'\n'}
        <Text style={s.email}>{email}</Text>
      </Text>

      {/* Code input */}
      <View style={s.codeRow}>
        {code.map((digit, idx) => (
          <TextInput
            key={idx}
            ref={(r) => { inputs.current[idx] = r; }}
            style={[s.codeBox, digit ? s.codeBoxFilled : null]}
            value={digit}
            onChangeText={(v) => handleCodeChange(v, idx)}
            onKeyPress={({ nativeEvent }) => handleCodeKeyPress(nativeEvent.key, idx)}
            keyboardType="number-pad"
            maxLength={1}
            textAlign="center"
            selectTextOnFocus
          />
        ))}
      </View>

      <Text style={s.label}>Новый пароль</Text>
      <TextInput
        style={s.input}
        placeholder="Минимум 6 символов"
        placeholderTextColor="#475569"
        value={newPassword}
        onChangeText={setNewPassword}
        secureTextEntry
        returnKeyType="next"
      />

      <Text style={s.label}>Повтори пароль</Text>
      <TextInput
        style={s.input}
        placeholder="Повтори пароль"
        placeholderTextColor="#475569"
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        secureTextEntry
        returnKeyType="done"
        onSubmitEditing={handleReset}
      />

      <Button title="Изменить пароль" onPress={handleReset} loading={loading} style={s.btn} />

      <TouchableOpacity onPress={handleResend} style={s.resendRow}>
        <Text style={s.resend}>Не получил код? <Text style={s.resendLink}>Отправить снова</Text></Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A', padding: 24 },
  back: { marginBottom: 24 },
  backText: { color: '#6366F1', fontSize: 16 },
  emoji: { fontSize: 48, marginBottom: 12 },
  title: { color: '#F8FAFC', fontSize: 26, fontWeight: '900', marginBottom: 8 },
  subtitle: { color: '#94A3B8', fontSize: 15, lineHeight: 24, marginBottom: 28 },
  email: { color: '#6366F1', fontWeight: '700' },
  codeRow: { flexDirection: 'row', gap: 10, justifyContent: 'center', marginBottom: 28 },
  codeBox: {
    width: 46, height: 56,
    backgroundColor: '#1E293B',
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#334155',
    color: '#F8FAFC',
    fontSize: 22,
    fontWeight: '800',
  },
  codeBoxFilled: { borderColor: '#6366F1' },
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
  btn: { marginTop: 4, marginBottom: 16 },
  resendRow: { alignItems: 'center' },
  resend: { color: '#64748B', fontSize: 14 },
  resendLink: { color: '#6366F1', fontWeight: '700' },
});
