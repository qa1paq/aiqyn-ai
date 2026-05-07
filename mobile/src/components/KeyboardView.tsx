import React from 'react';
import {
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

interface KeyboardViewProps {
  children: React.ReactNode;
  // true  = ScrollView внутри (формы с длинным контентом — Register, Profile)
  // false = просто flex View (короткие экраны — Login)
  scrollable?: boolean;
}

export default function KeyboardView({ children, scrollable = true }: KeyboardViewProps) {
  return (
    <SafeAreaView style={s.container}>
      <KeyboardAvoidingView
        style={s.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
      >
        {scrollable ? (
          <ScrollView
            contentContainerStyle={s.scrollContent}
            keyboardShouldPersistTaps="handled"
            showsVerticalScrollIndicator={false}
          >
            {children}
          </ScrollView>
        ) : (
          <View style={s.inner}>{children}</View>
        )}
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  flex: { flex: 1 },
  scrollContent: { flexGrow: 1, padding: 24, paddingBottom: 48 },
  inner: { flex: 1, padding: 24, justifyContent: 'center' },
});
