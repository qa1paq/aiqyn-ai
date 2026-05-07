import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface XPBadgeProps {
  xp: number;
  size?: 'sm' | 'md' | 'lg';
}

export default function XPBadge({ xp, size = 'md' }: XPBadgeProps) {
  const fontSize = size === 'sm' ? 11 : size === 'lg' ? 16 : 13;
  return (
    <View style={styles.badge}>
      <Text style={[styles.text, { fontSize }]}>+{xp} XP</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    backgroundColor: '#4ADE80',
    borderRadius: 20,
    paddingHorizontal: 10,
    paddingVertical: 4,
    alignSelf: 'flex-start',
  },
  text: { color: '#0F172A', fontWeight: '800' },
});
