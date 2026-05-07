import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface ProgressBarProps {
  current: number;
  total: number;
  showLabel?: boolean;
  color?: string;
}

export default function ProgressBar({
  current,
  total,
  showLabel = true,
  color = '#6366F1',
}: ProgressBarProps) {
  const progress = Math.min(Math.max(current / total, 0), 1);
  return (
    <View style={styles.container}>
      {showLabel && (
        <Text style={styles.label}>
          {current} / {total}
        </Text>
      )}
      <View style={styles.track}>
        <View style={[styles.fill, { width: `${progress * 100}%`, backgroundColor: color }]} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginVertical: 8 },
  label: { color: '#94A3B8', fontSize: 12, marginBottom: 4, textAlign: 'right' },
  track: {
    height: 8,
    backgroundColor: '#334155',
    borderRadius: 4,
    overflow: 'hidden',
  },
  fill: { height: '100%', borderRadius: 4 },
});
