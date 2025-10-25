import { Component, NgZone } from '@angular/core';
import { OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';
import { AuthService } from '../services/auth.service';
import { environment } from '../../environments/environment';

const clientId = environment.googleClientId;
declare const google: any;

@Component({
  selector: 'app-google-sign-in',
  templateUrl: './google-sign-in.component.html',
  styleUrls: ['./google-sign-in.component.css']
})
export class GoogleSignInComponent implements OnInit{
  constructor(
    private ngZone: NgZone,
    private router: Router,
    private authService: AuthService,
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.initializeGoogleSignIn();
  }

  initializeGoogleSignIn(): void {
    google.accounts.id.initialize({
      client_id: clientId,
      callback: (response:any) => this.handleCredentialResponse(response)
    });
    const button = document.getElementById('google-signin-button');
    if (button) {
      google.accounts.id.renderButton(
        button,
        { theme: 'outline', size: 'large', type: "standard" }
      );
    } else {
      console.error("Google Sign-In button element not found.");
    }

    google.accounts.id.prompt();
  }

  handleCredentialResponse(response: any): void {
    this.apiService.authenticateWithGoogle(response.credential).subscribe({
      next: (res: any) => {
        this.ngZone.run(() => {
          // Store the token and user info from the backend response
          const token = res.access_token?.access_token || res.access_token;
          const userInfo = {
            name: res.name,
            email: res.email
          };
          
          this.authService.setAuthState(true, token, userInfo);
          console.log("User authenticated successfully");
          this.router.navigate(['/dashboard']);
        });
      },
      error: (err: any) => {
        console.error("Error during Google Sign-In:", err);
      }
    });
  }
}
