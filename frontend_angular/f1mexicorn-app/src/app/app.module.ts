import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GoogleSignInComponent } from './google-sign-in/google-sign-in.component';
import { DashboardComponent } from './dashboard/dashboard.component';

// Import all interceptors
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { LoggingInterceptor } from './interceptors/logging.interceptor';
import { RaceDriversComponent } from './race-drivers/race-drivers.component';
import { CdkDrag, CdkDropList } from "@angular/cdk/drag-drop";


@NgModule({
  declarations: [
    AppComponent,
    GoogleSignInComponent,
    DashboardComponent,
    RaceDriversComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    CdkDrag,
    CdkDropList
],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: LoggingInterceptor,
      multi: true
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
