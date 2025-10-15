import { Component, NgZone } from '@angular/core';
import { OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../services/auth.service';

const clientId = '762758862056-4d4mibt265bofejjnmm5f3815bnukjge.apps.googleusercontent.com';
const scope = 'openid email profile';

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
    private http: HttpClient
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
        { theme: 'outline', size: 'large', type: "standard" }  // customization attributes
      );
    } else {
      console.error("Google Sign-In button element not found.");
    }

    google.accounts.id.prompt();
  }

  handleCredentialResponse(response: any): void {
    this.http.post('http://localhost:8000/users/auth/google', {
      auth_token: response.credential
    }).subscribe({
      next: (res: any) => {
        console.log(res);
            this.ngZone.run(() => {
              this.authService.setAuthState(true);
              // Navigate to a different route or update the UI
              console.log("User authenticated successfully");
              this.router.navigate(['/dashboard']); // Replace with your actual route
            });
          },
          error: (err: any) => {
            console.error("Error during Google Sign-In:", err);
          }

    });
  }
}
