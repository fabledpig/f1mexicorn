'use client';

import { useAuth } from '@/components/auth-provider/AuthProvider';
import { LOGIN_STATE_KEY, LoginState, NONCE_KEY } from '@/components/login/Login';
import { useGoogleAuthUsersAuthGooglePost } from '@/services/default/default';
import { useRouter } from 'next/navigation';
import { memo, useEffect, useRef } from 'react';

export default memo(function GoogleSso() {
  const didRun = useRef(false);
  const router = useRouter();
  const { mutate: authWithGoogleSso } = useGoogleAuthUsersAuthGooglePost();
  const { login } = useAuth();

  useEffect(() => {
    if (didRun.current) {
      return;
    }
    didRun.current = true;

    const params = new URLSearchParams(window.location.hash.substring(1));
    const state = params.get('state')!;
    const loginState = JSON.parse(
      window.localStorage.getItem(LOGIN_STATE_KEY) ?? '{}',
    ) as LoginState;

    if (loginState.type !== 'GoogleSso' || loginState.data.state !== state) {
      console.error('Login state mismatch');
      router.push('/login');
      return;
    }

    const id_token = params.get('id_token')!;
    const payload: { nonce: string } = JSON.parse(atob(id_token.split('.')[1]));

    const nonce = window.localStorage.getItem(NONCE_KEY);

    if (payload.nonce !== nonce) {
      console.error('Nonce mismatch');
      router.push('/login');
      return;
    }

    authWithGoogleSso(
      {
        data: {
          auth_token: id_token,
        },
      },
      {
        onSuccess: (response) => {
          if (!response.data.access_token) {
            router.push('/');
            return;
          }

          login(response.data.name, response.data.email, response.data.access_token.access_token);
          router.push('/');
        },
        onError: () => {
          router.push('/login');
        },
      },
    );
  }, [authWithGoogleSso, login, router]);

  return <></>;
});
