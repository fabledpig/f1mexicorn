import { inject, NgModule } from '@angular/core';
import { Router, RouterModule, Routes } from '@angular/router';
import { GoogleSignInComponent } from './google-sign-in/google-sign-in.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { authGuard } from './guards/auth.guard';

const routes: Routes = [
  {
    path: 'login',
    component: GoogleSignInComponent,
    canActivate: [() => {
      const router = inject(Router);
      const isAuthenticated = localStorage.getItem('auth_token') !== null;
      if (isAuthenticated) {
        router.navigate(['/dashboard']);
        return false;
      }
      return true;
    }]
  },
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] },
  { path: '', redirectTo: '/login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
