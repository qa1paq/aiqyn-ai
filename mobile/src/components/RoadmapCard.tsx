import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { RoadmapStep } from '../types';
import XPBadge from './XPBadge';

interface RoadmapCardProps {
  step: RoadmapStep;
  onComplete?: () => void;
}

export default function RoadmapCard({ step, onComplete }: RoadmapCardProps) {
  return (
    <View style={[styles.card, step.is_completed && styles.completed]}>
      <View style={styles.header}>
        <View style={styles.monthBadge}>
          <Text style={styles.monthText}>Month {step.month_number}</Text>
        </View>
        {step.is_completed && <Text style={styles.checkmark}>✅</Text>}
      </View>
      <Text style={styles.title}>{step.title}</Text>
      {step.description && <Text style={styles.description}>{step.description}</Text>}
      {step.tasks && step.tasks.length > 0 && (
        <View style={styles.tasks}>
          {step.tasks.map((task, i) => (
            <Text key={i} style={styles.task}>• {task}</Text>
          ))}
        </View>
      )}
      <View style={styles.footer}>
        <XPBadge xp={step.xp_reward} />
        {!step.is_completed && onComplete && (
          <TouchableOpacity style={styles.completeBtn} onPress={onComplete}>
            <Text style={styles.completeBtnText}>Complete Task</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1E293B',
    borderRadius: 20,
    padding: 18,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#6366F1',
  },
  completed: {
    borderLeftColor: '#4ADE80',
    opacity: 0.75,
  },
  header: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  monthBadge: {
    backgroundColor: '#312E81',
    borderRadius: 8,
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  monthText: { color: '#A5B4FC', fontSize: 11, fontWeight: '700' },
  checkmark: { fontSize: 18 },
  title: { color: '#F8FAFC', fontSize: 16, fontWeight: '800', marginBottom: 6 },
  description: { color: '#94A3B8', fontSize: 13, marginBottom: 10 },
  tasks: { gap: 4, marginBottom: 12 },
  task: { color: '#CBD5E1', fontSize: 13, lineHeight: 20 },
  footer: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  completeBtn: {
    backgroundColor: '#6366F1',
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 8,
  },
  completeBtnText: { color: '#fff', fontWeight: '700', fontSize: 13 },
});
