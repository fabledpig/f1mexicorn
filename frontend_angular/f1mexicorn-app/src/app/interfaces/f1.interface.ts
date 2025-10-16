export interface Race {
    race_id: number;
    race_name: string;
    race_type: string;
    race_date: string;
}

export interface Driver {
    driver_id: number;
    race_id: number;
    driver_number: number;
    driver_name: string;
    team: string;
}

export interface Guess {
    guessId?: number;
    userId: number;
    raceId: number;
    position1DriverId: number;
    position2DriverId: number;
    position3DriverId: number;
}
export interface RaceResult {
    resultId: number;
    raceId: number;
    position1DriverId: number;
    position2DriverId: number;
    position3DriverId: number;
}

export interface DriverStanding {
    position: number;
    driverNumber: number;
    driverName: string;
}

export interface SessionStanding {
    sessionId: number;
    standings: DriverStanding[];
}