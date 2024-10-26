'use client';

import { LOGIN_STATE_KEY, LoginState } from '@/components/Login';
import { useRouter, useSearchParams } from 'next/navigation';
import { memo, useEffect } from 'react';

export default memo(function GoogleSso() {
  const router = useRouter();
  const queryParams = useSearchParams();

  useEffect(() => {
    const state = queryParams.get('state');
    const loginState = JSON.parse(
      window.localStorage.getItem(LOGIN_STATE_KEY) ?? '{}',
    ) as LoginState;

    if (loginState.type !== 'GoogleSso' || loginState.data.state !== state) {
      console.error('Login state mismatch');
      router.push('/login');
    }
  }, [router, queryParams]);

  return <>{queryParams.get('code')}</>;
});
