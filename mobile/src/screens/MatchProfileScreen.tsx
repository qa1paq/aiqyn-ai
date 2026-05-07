import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRoute, RouteProp } from '@react-navigation/native';
import Button from '../components/Button';
import { matchingApi } from '../api/matching';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../types';

type RouteType = RouteProp<RootStackParamList, 'MatchProfile'>;
type Nav = StackNavigationProp<RootStackParamList, 'MatchProfile'>;

export default function MatchProfileScreen() {
  const route = useRoute<RouteType>();
  const navigation = useNavigation<Nav>();
  const { matchUser } = route.params;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{matchUser.full_name.charAt(0).toUpperCase()}</Text>
        </View>
        <Text style={styles.name}>{matchUser.full_name}</Text>
        <Text style={styles.location}>{matchUser.city ?? '—'}, {matchUser.country ?? '—'}</Text>
        <View style={styles.matchScore}>
          <Text style={styles.matchText}>{matchUser.match_score}% match with you</Text>
        </View>
        <View style={styles.infoGrid}>
          <View style={styles.infoCard}>
            <Text style={styles.infoLabel}>🎯 Target</Text>
            <Text style={styles.infoValue}>{matchUser.target_country ?? '—'}</Text>
          </View>
          <View style={styles.infoCard}>
            <Text style={styles.infoLabel}>🇬🇧 English</Text>
            <Text style={styles.infoValue}>{matchUser.english_level ?? '—'}</Text>
          </View>
        </View>
        {matchUser.recommended_majors && matchUser.recommended_majors.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Interested In</Text>
            {matchUser.recommended_majors.map((m) => (
              <Text key={m} style={styles.major}>• {m}</Text>
            ))}
          </View>
        )}
        <Button
          title="Connect 👋"
          onPress={async () => {
            await matchingApi.performAction(matchUser.user_id, 'like').catch(() => {});
            navigation.goBack();
          }}
          style={styles.btn}
        />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  scroll: { padding: 24, alignItems: 'center', paddingBottom: 48 },
  avatar: {
    width: 100, height: 100, borderRadius: 50,
    backgroundColor: '#6366F1',
    alignItems: 'center', justifyContent: 'center', marginBottom: 16,
  },
  avatarText: { color: '#fff', fontSize: 44, fontWeight: '900' },
  name: { color: '#F8FAFC', fontSize: 24, fontWeight: '900', marginBottom: 4 },
  location: { color: '#64748B', fontSize: 15, marginBottom: 16 },
  matchScore: { backgroundColor: '#312E81', borderRadius: 20, paddingHorizontal: 20, paddingVertical: 8, marginBottom: 24 },
  matchText: { color: '#A5B4FC', fontWeight: '700', fontSize: 16 },
  infoGrid: { flexDirection: 'row', gap: 12, marginBottom: 24, width: '100%' },
  infoCard: { flex: 1, backgroundColor: '#1E293B', borderRadius: 14, padding: 14 },
  infoLabel: { color: '#64748B', fontSize: 12, marginBottom: 4 },
  infoValue: { color: '#F8FAFC', fontWeight: '700', fontSize: 16 },
  section: { width: '100%', marginBottom: 24 },
  sectionTitle: { color: '#94A3B8', fontSize: 13, fontWeight: '700', marginBottom: 8, textTransform: 'uppercase' },
  major: { color: '#CBD5E1', fontSize: 14, marginBottom: 4 },
  btn: { width: '100%' },
});
