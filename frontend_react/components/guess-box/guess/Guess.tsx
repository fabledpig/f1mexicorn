import Driver from '@/components/driver/Driver';
import { RaceDriver } from '@/services/model';
import { HTMLAttributes, memo } from 'react';

type Props = HTMLAttributes<HTMLDivElement> & {
  position: number;
  driver?: RaceDriver;
};

export default memo(function Guess({ position, driver, ...props }: Props) {
  return (
    <div {...props}>
      <span>{position}</span>
      <Driver driver={driver} />
    </div>
  );
});
