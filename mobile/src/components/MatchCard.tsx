import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { MatchUser } from '../types';

interface MatchCardProps {
  user: MatchUser;
  onLike?: () => void;
  onSkip?: () => void;
}

export default function MatchCard({ user, onLike, onSkip }: MatchCardProps) {
  return (
    <View style={styles.card}>
      <View style={styles.avatar}>
        <Text style={styles.avatarText}>{user.full_name.charAt(0).toUpperCase()}</Text>
      </View>
      <Text style={styles.name}>{user.full_name}</Text>
      <Text style={styles.location}>{user.city ?? '—'}, {user.country ?? '—'}</Text>
      {user.target_country && (
        <Text style={styles.target}>🎯 Applying to {user.target_country}</Text>
      )}
      {user.recommended_majors && user.recommended_majors.length > 0 && (
        <Text style={styles.major}>📚 {user.recommended_majors[0]}</Text>
      )}
      <View style={styles.scoreBadge}>
        <Text style={styles.scoreText}>{user.match_score}% match</Text>
      </View>
      <View style={styles.actions}>
        <TouchableOpacity style={[styles.btn, styles.skipBtn]} onPress={onSkip}>
          <Text style={styles.skipText}>Skip</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.btn, styles.likeBtn]} onPress={onLike}>
          <Text style={styles.likeText}>Connect 👋</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1E293B',
    borderRadius: 24,
    padding: 24,
    alignItems: 'center',
    marginBottom: 16,
  },
  avatar: {
    width: 72, height: 72, borderRadius: 36,
    backgroundColor: '#6366F1',
    alignItems: 'center', justifyContent: 'center', marginBottom: 12,
  },
  avatarText: { color: '#fff', fontSize: 32, fontWeight: '800' },
  name: { color: '#F8FAFC', fontSize: 18, fontWeight: '800', marginBottom: 4 },
  location: { color: '#64748B', fontSize: 13, marginBottom: 4 },
  target: { color: '#A5B4FC', fontSize: 13, marginBottom: 4 },
  major: { color: '#94A3B8', fontSize: 13, marginBottom: 12 },
  scoreBadge: {
    backgroundColor: '#312E81', borderRadius: 20,
    paddingHorizontal: 16, paddingVertical: 6, marginBottom: 16,
  },
  scoreText: { color: '#A5B4FC', fontWeight: '700', fontSize: 14 },
  actions: { flexDirection: 'row', gap: 12, width: '100%' },
  btn: { flex: 1, borderRadius: 14, paddingVertical: 14, alignItems: 'center' },
  skipBtn: { backgroundColor: '#334155' },
  likeBtn: { backgroundColor: '#6366F1' },
  skipText: { color: '#94A3B8', fontWeight: '700' },
  likeText: { color: '#fff', fontWeight: '700' },
});
