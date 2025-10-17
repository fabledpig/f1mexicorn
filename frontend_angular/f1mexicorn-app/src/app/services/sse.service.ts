import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SseService {
  private eventSource: EventSource | null = null;
  private messageSubject = new BehaviorSubject<string>('');
  private readonly baseUrl = environment.apiUrl;

  message$ = this.messageSubject.asObservable();

  constructor() { }

  connect(): Observable<string> {
    this.eventSource = new EventSource(`${this.baseUrl}/f1/session_standing_sse`);

    this.eventSource.onmessage = (event) => {
      this.messageSubject.next(event.data);
    }

    this.eventSource.onerror = (error: Event) => {
        console.error('SSE Error:', error);
        this.messageSubject.error(error);
      };

    return this.message$;
  }

  closeConnection(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}
