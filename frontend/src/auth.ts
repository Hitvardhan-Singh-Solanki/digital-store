import { reactive } from "vue";

export const authState = reactive({
  isLoggedIn: false,
  userId: null as string | null,
  username: null as string | null,
});

export const login = (userId: string, username: string) => {
  authState.isLoggedIn = true;
  authState.userId = userId;
  authState.username = username;
};

export const logout = () => {
  authState.isLoggedIn = false;
  authState.userId = null;
  authState.username = null;
};
