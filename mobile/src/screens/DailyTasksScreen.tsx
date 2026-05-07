import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import Card from '../components/Card';
import XPBadge from '../components/XPBadge';
import { roadmapApi } from '../api/roadmap';

interface DailyTask { title: string; xp: number; duration_min: number; }

export default function DailyTasksScreen() {
  const [tasks, setTasks] = useState<DailyTask[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    roadmapApi.getDailyTasks()
      .then((data) => setTasks(data.tasks ?? []))
      .catch((e) => Alert.alert('Ошибка', e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <Text style={s.title}>Задачи на сегодня ⚡</Text>
        <Text style={s.subtitle}>Выполняй задачи — поддерживай серию</Text>
      </View>
      <FlatList
        data={tasks}
        keyExtractor={(_, i) => i.toString()}
        contentContainerStyle={s.list}
        renderItem={({ item }) => (
          <Card>
            <Text style={s.taskTitle}>{item.title}</Text>
            <View style={s.meta}>
              <Text style={s.duration}>⏱ {item.duration_min} мин</Text>
              <XPBadge xp={item.xp} />
            </View>
          </Card>
        )}
        ListEmptyComponent={<Text style={s.empty}>{loading ? 'Загрузка...' : 'Нет задач'}</Text>}
      />
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  header: { padding: 24, paddingBottom: 8 },
  title: { color: '#F8FAFC', fontSize: 24, fontWeight: '900' },
  subtitle: { color: '#64748B', fontSize: 14, marginTop: 4 },
  list: { paddingHorizontal: 16, paddingBottom: 24 },
  taskTitle: { color: '#F8FAFC', fontSize: 15, fontWeight: '700', marginBottom: 10 },
  meta: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  duration: { color: '#64748B', fontSize: 13 },
  empty: { textAlign: 'center', color: '#64748B', padding: 48, fontSize: 16 },
});
