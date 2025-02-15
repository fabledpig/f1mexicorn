'use client';

import localFont from 'next/font/local';
import './globals.scss';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import axios from 'axios';

const geistSans = localFont({
  src: './fonts/GeistVF.woff',
  variable: '--font-geist-sans',
  weight: '100 900',
});
const geistMono = localFont({
  src: './fonts/GeistMonoVF.woff',
  variable: '--font-geist-mono',
  weight: '100 900',
});

const queryClient = new QueryClient();
axios.defaults.baseURL = 'http://localhost:8000';

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <QueryClientProvider client={queryClient}>
        <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
          {children}
        </body>
      </QueryClientProvider>
    </html>
  );
}
