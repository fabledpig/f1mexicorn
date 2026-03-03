'use client';

import {
  useGetRacesF1SessionsGet,
  useGetSessionDriversF1SessionDriversGet,
  usePostUserGuessF1GuessPost,
} from '@/services/default/default';
import { memo, useEffect, useState } from 'react';
import SessionDrivers from '../session-drivers/SessionDrivers';
import GuessBox, { Guess } from '../guess-box/GuessBox';
import { RaceDriver } from '@/services/model';
import Button from '../button/Button';
import { useAuth } from '../auth-provider/AuthProvider';

export default memo(function RaceSession() {
  const { isPending: racesIsPending, data: racesData } = useGetRacesF1SessionsGet({ limit: 1 });
  const { isPending: driversIsPending, data: driversData } =
    useGetSessionDriversF1SessionDriversGet(
      {
        session_id: racesData?.data[0].race_id || 0,
      },
      { query: { enabled: !!racesData?.data } },
    );
  const { mutateAsync: postGuess } = usePostUserGuessF1GuessPost();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [raceName, setRaceName] = useState<string>('');
  const [sessionType, setSessionType] = useState<string>('');
  const [sessionDateTime, setSessionDateTime] = useState<Date | null>(null);
  const [guesses, setGuesses] = useState<Guess[]>([undefined, undefined, undefined]);
  const { authState } = useAuth();

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

  const onGuessButtonClicked = async () => {
    if (!sessionId || guesses.some((guess) => !guess)) {
      return;
    }

    await postGuess({
      data: {
        user_id: 0,
        race_id: sessionId,
        position_1_driver_id: guesses[0]!.driver_number,
        position_2_driver_id: guesses[1]!.driver_number,
        position_3_driver_id: guesses[2]!.driver_number,
      },
    });
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
            {driversData && (
              <>
                <SessionDrivers drivers={driversData.data} />
                <GuessBox guesses={guesses} onGuess={onGuess} />
                <Button onClick={onGuessButtonClicked}>Guess</Button>
              </>
            )}
          </div>
        </>
      )}
    </>
  );
});
