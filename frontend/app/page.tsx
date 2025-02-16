'use client';

import { useAuth } from '@/components/auth-provider/AuthProvider';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function Home() {
  const router = useRouter();
  const { authState } = useAuth();

  useEffect(() => {
    if (authState == null) {
      router.push('/login');
    }
  }, [router, authState]);

  return <>{authState && `Hello ${authState.name}`}</>;
}
