'use client';

import { ButtonHTMLAttributes, memo } from 'react';
import styles from './Button.module.scss';

type Props = {} & ButtonHTMLAttributes<HTMLButtonElement>;

export default memo(function ButtonComponent(props: Props) {
  return <button className={styles.button} {...props}></button>;
});
