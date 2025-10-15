import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GoogleSignInComponent } from './google-sign-in/google-sign-in.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { authGuard } from './guards/auth.guard';

const routes: Routes = [
  {
    path: 'login',
    component: GoogleSignInComponent,
    canActivate: [() => {
      const isAuthenticated = localStorage.getItem('authToken') !== null;
      if (isAuthenticated) {
        return ['/dashboard'];
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
