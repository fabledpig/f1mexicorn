'use client';

import { memo, useCallback } from 'react';

const clientId = '169032501865-jiehcs4eprbf3ghm9tdut3heglr7pfsk.apps.googleusercontent.com';
const redirectUri = 'http://localhost:3000/googlesso';
const scope = 'openid email profile';

export type LoginState = {
  type: 'GoogleSso';
  data: {
    state: 'string';
  };
};

export const LOGIN_STATE_KEY = 'LOGIN_STATE';

const bytesToBase64 = (bytes: Uint8Array): string => {
  const binString = Array.from(bytes, (byte) => String.fromCodePoint(byte)).join('');
  return btoa(binString);
};

export default memo(function LoginComponent() {
  const getAuthUrl = useCallback(() => {
    const randomArray = new Uint8Array(32);

    window.crypto.getRandomValues(randomArray);
    const state = bytesToBase64(randomArray);

    window.localStorage.setItem(
      LOGIN_STATE_KEY,
      JSON.stringify({
        type: 'GoogleSso',
        data: { state },
      } as LoginState),
    );

    return `https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}&state=${encodeURIComponent(state)}`;
  }, []);

  const onClick = useCallback(() => {
    window.location.href = getAuthUrl();
  }, [getAuthUrl]);

  return (
    <>
      <button onClick={onClick}>Login with Google SSO</button>
    </>
  );
});
