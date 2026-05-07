import AsyncStorage from '@react-native-async-storage/async-storage';

const TOKEN_KEY = 'aiqyn_access_token';

export const tokenStorage = {
  async save(token: string): Promise<void> {
    await AsyncStorage.setItem(TOKEN_KEY, token);
  },

  async get(): Promise<string | null> {
    return AsyncStorage.getItem(TOKEN_KEY);
  },

  async remove(): Promise<void> {
    await AsyncStorage.removeItem(TOKEN_KEY);
  },
};
