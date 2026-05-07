import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import ProgressBar from './ProgressBar';

const LEVEL_NAMES = ['', 'New Applicant', 'Explorer', 'Career Finder', 'University Hunter', 'Future Student', 'Global Applicant'];
const LEVEL_XP = [0, 0, 100, 300, 600, 1000, 1500];

interface LevelCardProps {
  level: number;
  totalXp: number;
  streak: number;
}

export default function LevelCard({ level, totalXp, streak }: LevelCardProps) {
  const nextXp = LEVEL_XP[level + 1] ?? LEVEL_XP[level];
  const currentXp = LEVEL_XP[level] ?? 0;
  const progressToNext = nextXp > currentXp ? totalXp - currentXp : totalXp;
  const progressMax = nextXp > currentXp ? nextXp - currentXp : 1;

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <View>
          <Text style={styles.levelLabel}>Level {level}</Text>
          <Text style={styles.levelName}>{LEVEL_NAMES[level] ?? 'Expert'}</Text>
        </View>
        <View style={styles.streak}>
          <Text style={styles.streakIcon}>🔥</Text>
          <Text style={styles.streakNum}>{streak}</Text>
        </View>
      </View>
      <ProgressBar current={progressToNext} total={progressMax} showLabel={false} />
      <Text style={styles.xpText}>{totalXp} XP total</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#1E293B',
    borderRadius: 20,
    padding: 16,
    marginBottom: 12,
  },
  row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  levelLabel: { color: '#6366F1', fontSize: 12, fontWeight: '700' },
  levelName: { color: '#F8FAFC', fontSize: 18, fontWeight: '800' },
  streak: { alignItems: 'center' },
  streakIcon: { fontSize: 20 },
  streakNum: { color: '#FB923C', fontWeight: '800', fontSize: 14 },
  xpText: { color: '#64748B', fontSize: 12, marginTop: 4 },
});
