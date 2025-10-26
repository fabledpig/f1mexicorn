import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { AuthResponse, GoogleAuthRequest, User } from '../interfaces/user.interface';
import { Race, Driver, Guess, RaceResult, DriverStanding, SessionStanding } from '../interfaces/f1.interface';


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
  
  getSessions(limit?: number): Observable<Race[]> {
    const params: { [key: string]: string } = {};
    if (limit) {
      params['limit'] = limit.toString();
    }
    return this.http.get<Race[]>(`${this.baseUrl}/f1/sessions`, { params })
        .pipe(
            catchError(this.handleError)
        );
  }

  getSessionDrivers(sessionID: number): Observable<Driver[]> {
    return this.http.get<Driver[]>(`${this.baseUrl}/f1/session_drivers`, { params: { session_id: sessionID.toString() } })
      .pipe(
        catchError(this.handleError)
      );
  }

  getGuess(event_id: number): Observable<Guess> {
    return this.http.get<Guess>(`${this.baseUrl}/f1/guess/${event_id}`)
      .pipe(
        catchError(this.handleError)
      );
  }

  postGuess(guess: Guess): Observable<Guess> {
    return this.http.post<Guess>(`${this.baseUrl}/f1/guess`, guess)
      .pipe(
        catchError(this.handleError)
      );
  }

  getSessionStandings(sessionID: number): Observable<SessionStanding> {
    return this.http.get<SessionStanding>(`${this.baseUrl}/f1/session_standing`, { params: { session_id: sessionID.toString() } })
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