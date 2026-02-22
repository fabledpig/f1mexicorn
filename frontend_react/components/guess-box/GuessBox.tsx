import { RaceDriver } from '@/services/model';
import { memo } from 'react';
import DragTarget from '../drag-target/DragTarget';
import Driver from '../driver/Driver';

export type Guess = RaceDriver | undefined;

type Props = { onGuess: (index: number, driver: RaceDriver) => void; guesses: Guess[] };

export default memo(function GuessBox({ onGuess, guesses }: Props) {
  const onDrop = (position: number) => {
    return (driver: RaceDriver) => {
      onGuess(position, driver);
    };
  };

  const deserializeDriver = (data: string) => {
    try {
      return JSON.parse(data) as RaceDriver;
    } catch {
      return undefined;
    }
  };

  return (
    <ul>
      {guesses.map((driver, index) => (
        <DragTarget key={index} onDrop={onDrop(index)} deserialize={deserializeDriver}>
          <li>
            <span>{index + 1}</span>
            <Driver driver={driver} />
          </li>
        </DragTarget>
      ))}
    </ul>
  );
});
