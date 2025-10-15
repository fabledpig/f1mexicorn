import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private authState = new BehaviorSubject<boolean>(this.getStoredAuthState());
  authstate$ = this.authState.asObservable();

  constructor() { 
    // Check if user is already authenticated on service initialization
    this.initializeAuthState();
  }

  private initializeAuthState(): void {
    const token = this.getToken();
    if (token && this.isTokenValid(token)) {
      this.setAuthState(true);
    }
  }

  private getStoredAuthState(): boolean {
    const token = localStorage.getItem('auth_token');
    return token ? this.isTokenValid(token) : false;
  }

  setAuthState(state: boolean, token?: string, userInfo?: any): void {
    this.authState.next(state);
    if (state && token) {
      localStorage.setItem('auth_token', token);
      // Also store user info if provided
      if (userInfo) {
        localStorage.setItem('user_info', JSON.stringify(userInfo));
      }
    } else if (!state) {
      this.logout();
    }
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    return token ? this.isTokenValid(token) : false;
  }

  getToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  getUserInfo(): any {
    const userInfo = localStorage.getItem('user_info');
    return userInfo ? JSON.parse(userInfo) : null;
  }

  private isTokenValid(token: string): boolean {
    if (!token) return false;
    
    try {
      // Basic JWT validation - check if it's expired
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp ? payload.exp > currentTime : true;
    } catch (error) {
      return false;
    }
  }

  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_info');
    this.authState.next(false);
  }
}
