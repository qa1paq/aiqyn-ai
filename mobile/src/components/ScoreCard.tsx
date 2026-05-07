import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const CATEGORY_LABELS: Record<string, string> = {
  IT_ENGINEERING: '💻 Tech & Engineering',
  DATA_AI: '🤖 Data & AI',
  MEDICINE: '🩺 Medicine',
  BUSINESS: '📈 Business',
  LAW: '⚖️ Law',
  DESIGN_CREATIVE: '🎨 Design',
  SOCIAL_SCIENCES: '🌍 Social Sciences',
  EDUCATION: '📚 Education',
};

interface ScoreCardProps {
  scores: Record<string, number>;
  top?: number;
}

export default function ScoreCard({ scores, top = 4 }: ScoreCardProps) {
  const sorted = Object.entries(scores)
    .sort(([, a], [, b]) => b - a)
    .slice(0, top);

  return (
    <View style={styles.container}>
      {sorted.map(([cat, score]) => (
        <View key={cat} style={styles.row}>
          <Text style={styles.label}>{CATEGORY_LABELS[cat] ?? cat}</Text>
          <View style={styles.barTrack}>
            <View style={[styles.barFill, { width: `${score}%` }]} />
          </View>
          <Text style={styles.score}>{score.toFixed(0)}%</Text>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { gap: 12 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  label: { color: '#CBD5E1', fontSize: 13, width: 140 },
  barTrack: { flex: 1, height: 8, backgroundColor: '#334155', borderRadius: 4, overflow: 'hidden' },
  barFill: { height: '100%', backgroundColor: '#6366F1', borderRadius: 4 },
  score: { color: '#94A3B8', fontSize: 12, width: 36, textAlign: 'right' },
});
