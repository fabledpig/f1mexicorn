'use client';

import { createContext, PropsWithChildren, useContext, useState } from 'react';

type AuthState = {
  name: string;
  email: string;
  access_token: string;
};

const AuthContext = createContext<{
  authState: AuthState | null;
  login: (name: string, email: string, access_token: string) => void;
}>({ authState: null, login: () => {} });

export default function AuthProvider({ children }: PropsWithChildren) {
  const [authState, setAuthState] = useState<AuthState | null>(null);

  const login = (name: string, email: string, access_token: string) => {
    setAuthState({ name, email, access_token });
  };

  return <AuthContext.Provider value={{ authState, login }}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
