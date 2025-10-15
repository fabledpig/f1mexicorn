import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private authState = new BehaviorSubject<boolean>(false);
  authstate$ = this.authState.asObservable();

  constructor() { }

  setAuthState(state: boolean) :void {
    this.authState.next(state);
  }

  isAuthenticated(): boolean {
    return this.authState.value;
  }
}
