import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements HttpInterceptor {
  
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const startTime = Date.now();
    
    console.log(`HTTP Request: ${req.method} ${req.url}`);
    
    return next.handle(req).pipe(
      tap({
        next: (event) => {
          if (event instanceof HttpResponse) {
            const duration = Date.now() - startTime;
            console.log(`HTTP Response: ${req.method} ${req.url} - ${event.status} (${duration}ms)`);
          }
        },
        error: (error) => {
          const duration = Date.now() - startTime;
          console.log(`HTTP Error: ${req.method} ${req.url} - ${error.status} (${duration}ms)`);
        }
      })
    );
  }
}