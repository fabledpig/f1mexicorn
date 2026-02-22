'use client';

import {
  useGetRacesF1SessionsGet,
  useSessionDriversF1SessionDriversGet,
} from '@/services/default/default';
import { memo, useEffect, useState } from 'react';
import SessionDrivers from '../session-drivers/SessionDrivers';
import GuessBox, { Guess } from '../guess-box/GuessBox';
import { RaceDriver } from '@/services/model';

export default memo(function RaceSession() {
  const { isPending: racesIsPending, data: racesData } = useGetRacesF1SessionsGet({ limit: 1 });
  const { isPending: driversIsPending, data: driversData } = useSessionDriversF1SessionDriversGet(
    {
      session_id: racesData?.data[0].race_id || 0,
    },
    { query: { enabled: !!racesData?.data } },
  );
  const [sessionId, setSessionId] = useState<number | null>();
  const [raceName, setRaceName] = useState<string>('');
  const [sessionType, setSessionType] = useState<string>('');
  const [sessionDateTime, setSessionDateTime] = useState<Date | null>(null);
  const [guesses, setGuesses] = useState<Guess[]>([undefined, undefined, undefined]);

  useEffect(() => {
    if (!racesData) {
      return;
    }

    const race = racesData.data[0];
    setSessionId(race.race_id || null);
    setRaceName(race.race_name);
    setSessionType(race.race_type);
    setSessionDateTime(new Date(race.race_date));
  }, [racesData]);

  const onGuess = (index: number, driver: RaceDriver) => {
    const newGuesses = [...guesses];
    newGuesses[index] = driver;
    setGuesses(newGuesses);
  };

  return (
    <>
      {racesIsPending && <span>Loading...</span>}
      {racesData && (
        <>
          <span>
            {raceName} - {sessionType}#[{sessionId}] - {sessionDateTime?.toLocaleDateString()}
          </span>
          <div>
            {driversIsPending && <span>Loading...</span>}
            {driversData && <SessionDrivers drivers={driversData.data} draggable={true} />}
            <GuessBox guesses={guesses} onGuess={onGuess} />
          </div>
        </>
      )}
    </>
  );
});
