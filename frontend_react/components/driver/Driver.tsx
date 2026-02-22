import { RaceDriver } from '@/services/model';
import { HTMLAttributes, memo } from 'react';

type Props = HTMLAttributes<HTMLDivElement> & {
  driver?: RaceDriver;
};

export default memo(function Driver({ driver, ...props }: Props) {
  return (
    <div {...props}>
      {!driver && <>???</>}
      {driver && (
        <>
          <span>{driver.driver_number}</span>
          <span>{driver.driver_name}</span>
        </>
      )}
    </div>
  );
});
