import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import UniversityCard from '../components/UniversityCard';
import { universitiesApi } from '../api/universities';
import { University, RootStackParamList } from '../types';

type Nav = StackNavigationProp<RootStackParamList, 'Universities'>;

export default function UniversitiesScreen() {
  const navigation = useNavigation<Nav>();
  const [universities, setUniversities] = useState<University[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    universitiesApi.getUniversities()
      .then(setUniversities)
      .catch((e) => Alert.alert('Ошибка', e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <Text style={s.title}>Университеты</Text>
        <Text style={s.subtitle}>{loading ? 'Загрузка...' : `${universities.length} учебных заведений`}</Text>
      </View>
      <FlatList
        data={universities}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={s.list}
        renderItem={({ item }) => (
          <UniversityCard university={item} onPress={() => navigation.navigate('UniversityDetail', { universityId: item.id })} />
        )}
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
});
