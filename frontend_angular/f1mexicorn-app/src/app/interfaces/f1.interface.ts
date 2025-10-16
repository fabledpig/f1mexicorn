export interface Race {
    race_id: number | null;
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
    user_email: string;
    race_id: number;
    position_1_driver_id: number;
    position_2_driver_id: number;
    position_3_driver_id: number;
}
export interface RaceResult {
    result_id: number | null;
    race_id: number;
    position_1_driver_id: number;
    position_2_driver_id: number;
    position_3_driver_id: number;
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