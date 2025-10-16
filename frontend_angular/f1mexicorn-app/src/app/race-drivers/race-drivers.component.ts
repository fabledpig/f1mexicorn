import { Component } from '@angular/core';
import { Guess, Driver, Race } from '../interfaces/f1.interface';
import { ApiService } from '../services/api.service';
import { switchMap } from 'rxjs/operators';
import { CdkDrag, CdkDragDrop, CdkDropList, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-race-drivers',
  templateUrl: './race-drivers.component.html',
  styleUrls: ['./race-drivers.component.css']
})
export class RaceDriversComponent {
  race: Race = null!;
  drivers: Driver[] = [];
  prediction: Driver[] = [];
  constructor(
    private apiService: ApiService,
    private authService: AuthService
  ) {}
  ngOnInit(): void {
    this.apiService.getSessions(1).pipe(
      switchMap((race: Race[]) => {
        this.race = race[0];
        console.log("Latest race:", this.race);
        // Return the second API call
        console.log("Fetching drivers for raceId:", this.race.race_id);
        return this.apiService.getSessionDrivers(this.race.race_id ?? 0);
      })
    ).subscribe({
      next: (drivers: Driver[]) => {
        this.drivers = drivers;
        console.log("Drivers in latest race:", drivers);
      },
      error: (err) => {
        console.error("Error fetching data:", err);
      }
    });
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
      race_id: this.race.race_id ?? 0,
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

}


