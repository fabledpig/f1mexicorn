'use client';

import { LOGIN_STATE_KEY, LoginState } from '@/components/login/Login';
import { useGoogleAuthUsersAuthGooglePost } from '@/services/default/default';
import { useRouter, useSearchParams } from 'next/navigation';
import { memo, useEffect } from 'react';

let didRun = false;

export default memo(function GoogleSso() {
  const router = useRouter();
  const queryParams = useSearchParams();
  const { mutateAsync: authWithGoogleSso } = useGoogleAuthUsersAuthGooglePost();

  useEffect(() => {
    if (didRun) {
      return;
    }
    didRun = true;

    const state = queryParams.get('state');
    const loginState = JSON.parse(
      window.localStorage.getItem(LOGIN_STATE_KEY) ?? '{}',
    ) as LoginState;

    if (loginState.type !== 'GoogleSso' || loginState.data.state !== state) {
      console.error('Login state mismatch');
      router.push('/login');
    }
    authWithGoogleSso({
      data: {
        auth_token: queryParams.get('code')!,
      },
    }).catch(() => {
      router.push('/login');
    });
  }, []);

  return <>{queryParams.get('code')}</>;
});
