import { memo } from 'react';
import styles from './styles.module.scss';

import LoginComponent from '@/components/login/Login';

export default memo(function Login() {
  return (
    <>
      <div className={styles.login}>
        <p className={styles.welcome}>Welcome to F1 Mexicorn!</p>
        <LoginComponent />
      </div>
    </>
  );
});
