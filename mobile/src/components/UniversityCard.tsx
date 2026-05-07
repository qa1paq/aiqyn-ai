import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { University } from '../types';

interface UniversityCardProps {
  university: University;
  onPress?: () => void;
}

const FLAG: Record<string, string> = {
  USA: '🇺🇸', Canada: '🇨🇦', UK: '🇬🇧', Germany: '🇩🇪',
  Turkey: '🇹🇷', 'South Korea': '🇰🇷', Malaysia: '🇲🇾',
  Kazakhstan: '🇰🇿', UAE: '🇦🇪',
};

export default function UniversityCard({ university, onPress }: UniversityCardProps) {
  const flag = FLAG[university.country] ?? '🌍';
  const tuition = university.tuition_min_usd === 0
    ? 'Tuition-Free'
    : university.tuition_min_usd
    ? `$${(university.tuition_min_usd / 1000).toFixed(0)}k–$${(university.tuition_max_usd! / 1000).toFixed(0)}k/yr`
    : 'Contact for fees';

  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.85}>
      <View style={styles.header}>
        <Text style={styles.flag}>{flag}</Text>
        <View style={styles.info}>
          <Text style={styles.name} numberOfLines={2}>{university.name}</Text>
          <Text style={styles.location}>{university.city}, {university.country}</Text>
        </View>
        {university.ranking && (
          <View style={styles.rankBadge}>
            <Text style={styles.rankText}>#{university.ranking}</Text>
          </View>
        )}
      </View>
      <Text style={styles.tuition}>{tuition}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1E293B',
    borderRadius: 20,
    padding: 16,
    marginBottom: 12,
  },
  header: { flexDirection: 'row', alignItems: 'flex-start', gap: 12, marginBottom: 8 },
  flag: { fontSize: 32 },
  info: { flex: 1 },
  name: { color: '#F8FAFC', fontSize: 15, fontWeight: '700' },
  location: { color: '#64748B', fontSize: 13, marginTop: 2 },
  rankBadge: { backgroundColor: '#312E81', borderRadius: 8, paddingHorizontal: 8, paddingVertical: 4 },
  rankText: { color: '#A5B4FC', fontSize: 11, fontWeight: '700' },
  tuition: { color: '#4ADE80', fontSize: 13, fontWeight: '600' },
});
