import { RaceDriver } from '@/services/model';
import { memo } from 'react';
import Draggable from '../draggable/Draggable';
import Driver from '../driver/Driver';

type Props = { drivers: RaceDriver[] };

export default memo(function SessionDrivers(props: Props) {
  const serializeDriver = (driver: RaceDriver) => {
    return () => {
      return JSON.stringify(driver);
    };
  };

  return (
    <>
      <ul>
        {props.drivers.map((driver) => (
          <Draggable key={driver.driver_number} serialize={serializeDriver(driver)}>
            <li id={`${driver.driver_number}`} key={driver.driver_number}>
              <Driver driver={driver} />
            </li>
          </Draggable>
        ))}
      </ul>
    </>
  );
});
