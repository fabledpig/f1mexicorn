import { Component, NgZone } from '@angular/core';
import { Guess, Driver, Race } from '../interfaces/f1.interface';
import { ApiService } from '../services/api.service';
import { switchMap } from 'rxjs/operators';
import { CdkDrag, CdkDragDrop, CdkDropList, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';
import { AuthService } from '../services/auth.service';
import { SseService } from '../services/sse.service';
import { Observable } from 'rxjs/internal/Observable';
import { Subscription } from 'rxjs';

const teamLogos = new Map<string, string>([
  ['Mercedes', "url('/assets/teams/mercedes.png')"],
  ['Red Bull Racing', "url('/assets/teams/redbull.png')"],
  ['Ferrari', "url('/assets/teams/ferrari.png')"],
  ['McLaren', "url('/assets/teams/mclaren.png')"],
  ['Alpine', "url('/assets/teams/alpine.png')"],
  ['Aston Martin', "url('/assets/teams/aston.png')"],
  ['Williams', "url('/assets/teams/williams.png')"],
  ['Racing Bulls', "url('/assets/teams/visarb.png')"],
  ['Haas F1 Team', "url('/assets/teams/haas.png')"],
  ['Kick Sauber', "url('/assets/teams/stake.png')"]
]);


@Component({
  selector: 'app-race-drivers',
  templateUrl: './race-drivers.component.html',
  styleUrls: ['./race-drivers.component.css']
})
export class RaceDriversComponent {
  eventFinished: boolean = false;
  race: Race = {} as Race;
  drivers: Driver[] = [];
  prediction: Driver[] = [];
  message$: Observable<string> = new Observable<string>();
  private sseSubscription: Subscription | null = null;
  
  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private sseService: SseService,
    private ngZone: NgZone
  ) {}
  ngOnInit(): void {
    this.apiService.getSessions(1).pipe(
      switchMap((race: Race[]) => {
        this.race = race[0];
        this.eventFinished = this.isNextEventFinished(this.race);
        console.log("Latest race:", this.race);
        console.log("Fetching drivers for raceId:", this.race.race_id);
        return this.apiService.getSessionDrivers(this.race.race_id ?? 0);
      }),
      switchMap((drivers: Driver[]) => {
        this.drivers = drivers;
        console.log("Drivers in latest race:", drivers);
        return this.apiService.getGuess(this.race.race_id ?? 0);
      })).subscribe({
      next: (guess: Guess) => {
        this.populatePrediction(guess);
        console.log("User's existing guess:", guess);
      },
      error: (err) => {
        console.error("Error fetching data:", err);
      }
    });

    // Set up SSE connection
    // TODO CHANGE THIS AFTER FIGURING OUT WHAT TO DO HERE LOL
    this.message$ = this.sseService.connect();
    this.sseSubscription = this.message$.subscribe({
      next: (message: string) => {
        this.ngZone.run(() => {
          console.log("SSE Message received:", message);
          this.eventFinished = !this.eventFinished;
          console.log("Event finished changed to:", this.eventFinished);
        });
      },
      error: (err) => {
        console.error("SSE Error:", err);
      }
    })

  }

  drop(event: CdkDragDrop<Driver[]>) {
    if (event.previousContainer === event.container) {
      // Reordering within the same list
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }
  }

  dropBack(event: CdkDragDrop<Driver[]>) {
    if (event.previousContainer === event.container) {
      // Reordering within the same list
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      if (this.prediction.length >= 3) {
        return; // Prevent adding more than 3 drivers to prediction
      }
      transferArrayItem(event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }
  }

  submitPrediction() {
    const userEmail = this.authService.getUserInfo().email;
    const guess: Guess = {
      user_email: userEmail,
      race_id: this.race?.race_id ?? 0,
      position_1_driver_id: this.prediction[0]?.driver_number,
      position_2_driver_id: this.prediction[1]?.driver_number,
      position_3_driver_id: this.prediction[2]?.driver_number
    };

    this.apiService.postGuess(guess).subscribe({
      next: (response) => {
        console.log("Prediction submitted successfully:", response);
      },
      error: (err) => {
        console.error("Error submitting prediction:", err);
      }
    });
  }

  isNextEventFinished(race: Race): boolean {
    const now = new Date();
    const raceDate = new Date(race.race_date);
    return raceDate < now;
  }

  populatePrediction(guess: Guess) {
    // populate prediction array based on guess
    this.prediction = [];
    if (guess.position_1_driver_id) {
      const driver1 = this.drivers.find(d => d.driver_number === guess.position_1_driver_id);
      if (driver1) {
        this.prediction.push(driver1);
        this.drivers = this.drivers.filter(d => d.driver_number !== driver1.driver_number);
      }
    }
    if (guess.position_2_driver_id) {
      const driver2 = this.drivers.find(d => d.driver_number === guess.position_2_driver_id);
      if (driver2) {
        this.prediction.push(driver2);
        this.drivers = this.drivers.filter(d => d.driver_number !== driver2.driver_number);
      }

    }
    if (guess.position_3_driver_id) {
      const driver3 = this.drivers.find(d => d.driver_number === guess.position_3_driver_id);
      if (driver3) {
        this.prediction.push(driver3);
        this.drivers = this.drivers.filter(d => d.driver_number !== driver3.driver_number);
      }
    }
  }

  getDriverBackground(driver: Driver): { [key: string]: string } {
    return {
      'background-image': teamLogos.get(driver.team) || 'none',
      'background-size': 'fit',
      'background-position': 'center',
      'background-color': 'rgba(183, 208, 216, 1)',
      'background-blend-mode': 'overlay'
    }
  }
}