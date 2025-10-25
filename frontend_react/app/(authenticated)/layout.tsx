'use client';

import { useAuth } from '@/components/auth-provider/AuthProvider';
import TopBar from '@/components/top-bar/TopBar';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function AuthenticatedLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter();
  const { authState } = useAuth();

  useEffect(() => {
    if (!authState) {
      router.push('/login');
    }
  }, [authState, router]);

  return (
    <>
      {authState && (
        <>
          <TopBar name={authState.name} />
          {children}
        </>
      )}
    </>
  );
}
