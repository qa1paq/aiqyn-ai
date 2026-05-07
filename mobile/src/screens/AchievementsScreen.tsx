import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import Card from '../components/Card';
import LevelCard from '../components/LevelCard';
import { gamificationApi } from '../api/gamification';
import { Achievement, Gamification } from '../types';

export default function AchievementsScreen() {
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [gamification, setGamification] = useState<Gamification | null>(null);

  useEffect(() => {
    Promise.all([gamificationApi.getAchievements(), gamificationApi.getMyGamification()])
      .then(([achs, gam]) => { setAchievements(achs); setGamification(gam); })
      .catch((e) => Alert.alert('Ошибка', e.message));
  }, []);

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <Text style={s.title}>Достижения 🏆</Text>
      </View>
      <FlatList
        data={achievements}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={s.list}
        ListHeaderComponent={
          gamification ? (
            <LevelCard level={gamification.level} totalXp={gamification.total_xp} streak={gamification.current_streak} />
          ) : null
        }
        renderItem={({ item }) => (
          <Card style={[s.achCard, !item.unlocked ? s.locked : null]}>
            <View style={s.row}>
              <Text style={s.achIcon}>{item.unlocked ? '🏅' : '🔒'}</Text>
              <View style={{ flex: 1 }}>
                <Text style={[s.achTitle, !item.unlocked && s.lockedText]}>{item.title}</Text>
                <Text style={s.achDesc}>{item.description}</Text>
              </View>
              <Text style={s.xp}>+{item.xp_reward} XP</Text>
            </View>
            {item.unlocked_at && (
              <Text style={s.unlockedAt}>Получено {new Date(item.unlocked_at).toLocaleDateString('ru-RU')}</Text>
            )}
          </Card>
        )}
      />
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  header: { padding: 24, paddingBottom: 8 },
  title: { color: '#F8FAFC', fontSize: 24, fontWeight: '900' },
  list: { paddingHorizontal: 16, paddingBottom: 24 },
  achCard: { marginBottom: 8 },
  locked: { opacity: 0.5 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  achIcon: { fontSize: 28 },
  achTitle: { color: '#F8FAFC', fontWeight: '700', fontSize: 15 },
  lockedText: { color: '#475569' },
  achDesc: { color: '#64748B', fontSize: 13, marginTop: 2 },
  xp: { color: '#4ADE80', fontWeight: '700', fontSize: 13 },
  unlockedAt: { color: '#475569', fontSize: 11, marginTop: 8 },
});
