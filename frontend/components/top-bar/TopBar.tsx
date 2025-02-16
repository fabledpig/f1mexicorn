'use client';

import { memo } from 'react';
import styles from './TopBar.module.scss';

type Props = {
  name: string;
};

export default memo(function TopBar({ name }: Props) {
  return (
    <nav className={styles.frame}>
      <span>F1 Mexicorn</span>
      <span>{name}</span>
    </nav>
  );
});
