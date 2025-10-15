import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

// Define interfaces for type safety
export interface GoogleAuthRequest {
  auth_token: string;
}

export interface AuthResponse {
  name: string;
  email: string;
  access_token: {
    access_token: string;
  } | string;
}

export interface User {
  userId: number;
  name: string;
  email: string;
}

export interface Race {
    raceId: number;
    raceName: string;
    raceType: string;
    raceDate: string;
}

export interface Driver {
    driverId: number;
    raceId: number;
    driveNumber: number;
    driverName: string;
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

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // ===== AUTH ENDPOINTS =====
  
  authenticateWithGoogle(authToken: string): Observable<AuthResponse> {
    const payload: GoogleAuthRequest = { auth_token: authToken };

    return this.http.post<AuthResponse>(`${this.baseUrl}/users/auth/google`, payload)
      .pipe(
        catchError(this.handleError)
      );
  }

  // ===== F1 ENDPOINTS =====
  
  getSessions(limit?: number): Observable<any> {
    const params: { [key: string]: string } = {};
    if (limit) {
      params['limit'] = limit.toString();
    }
    return this.http.get(`${this.baseUrl}/sessions`, { params })
        .pipe(
            catchError(this.handleError)
        );
  }

  getSessionDrivers(sessionID: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/session_drivers`, { params: { session_id: sessionID.toString() } })
      .pipe(
        catchError(this.handleError)
      );
  }

  postGuess(guess: Guess): Observable<Guess> {
    return this.http.post<Guess>(`${this.baseUrl}/guesses`, guess)
      .pipe(
        catchError(this.handleError)
      );
  }

  getSessionStandings(sessionID: number): Observable<SessionStanding> {
    return this.http.get<SessionStanding>(`${this.baseUrl}/session_standing`, { params: { session_id: sessionID.toString() } })
      .pipe(
        catchError(this.handleError)
      );
  }

  getWinners(sessionKey?: number): Observable<Guess> {
    const params: { [key: string]: string } = {};
    if (sessionKey) {
      params['session_key'] = sessionKey.toString();
    }
    return this.http.get<Guess>(`${this.baseUrl}/results/winners`, { params })
      .pipe(
        catchError(this.handleError)
      );
  }
  // ===== PRIVATE METHODS =====

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred';
    
    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Client Error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = `Server Error: ${error.status} - ${error.message}`;
      
      // Handle specific status codes
      switch (error.status) {
        case 401:
          errorMessage = 'Unauthorized - Please login again';
          // Optionally trigger logout here
          break;
        case 403:
          errorMessage = 'Forbidden - You do not have permission';
          break;
        case 404:
          errorMessage = 'Resource not found';
          break;
        case 500:
          errorMessage = 'Internal server error';
          break;
      }
    }
    
    console.error('API Error:', errorMessage, error);
    return throwError(() => new Error(errorMessage));
  }

  // Note: Authorization headers are automatically added by AuthInterceptor
  // No need for manual auth header methods since interceptor handles it
}