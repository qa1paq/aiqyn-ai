import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import MatchCard from '../components/MatchCard';
import Button from '../components/Button';
import { matchingApi } from '../api/matching';
import { MatchUser, RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'MatchingFeed'>;

export default function MatchingFeedScreen() {
  const navigation = useNavigation<Nav>();
  const [users, setUsers] = useState<MatchUser[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    matchingApi.getFeed()
      .then(setUsers)
      .catch((e) => Alert.alert('Ошибка', e.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleAction(userId: number, action: 'like' | 'skip') {
    await matchingApi.performAction(userId, action).catch(() => {});
    setUsers((prev) => prev.filter((u) => u.user_id !== userId));
  }

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <Text style={s.title}>Студенты как ты</Text>
        <Text style={s.subtitle}>Найди будущих однокурсников со всего мира</Text>
      </View>
      {loading ? (
        <View style={s.center}><Text style={s.emptyText}>Ищем совпадения...</Text></View>
      ) : users.length === 0 ? (
        <View style={s.center}>
          <Text style={s.emptyEmoji}>🎉</Text>
          <Text style={s.emptyText}>Ты просмотрел всех!</Text>
          <Button title="Создать мой план" onPress={() => navigation.navigate('Roadmap')} style={{ marginTop: 20 }} />
        </View>
      ) : (
        <FlatList
          data={users}
          keyExtractor={(item) => item.user_id.toString()}
          contentContainerStyle={s.list}
          renderItem={({ item }) => (
            <MatchCard
              user={item}
              onLike={() => handleAction(item.user_id, 'like')}
              onSkip={() => handleAction(item.user_id, 'skip')}
            />
          )}
        />
      )}
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  header: { padding: 24, paddingBottom: 8 },
  title: { color: '#F8FAFC', fontSize: 24, fontWeight: '900' },
  subtitle: { color: '#64748B', fontSize: 14, marginTop: 4 },
  list: { paddingHorizontal: 16, paddingBottom: 24 },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 24 },
  emptyEmoji: { fontSize: 48, marginBottom: 12 },
  emptyText: { color: '#94A3B8', fontSize: 16, textAlign: 'center' },
});
