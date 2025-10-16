import { Component } from '@angular/core';
import { Guess, Driver, Race } from '../interfaces/f1.interface';
import { ApiService } from '../services/api.service';
import { switchMap } from 'rxjs/operators';
import { CdkDrag, CdkDragDrop, CdkDropList, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';

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
    private apiService: ApiService
  ) {}
  ngOnInit(): void {
    this.apiService.getSessions(1).pipe(
      switchMap((race: Race[]) => {
        this.race = race[0];
        console.log("Latest race:", this.race);
        // Return the second API call
        console.log("Fetching drivers for raceId:", this.race.race_id);
        return this.apiService.getSessionDrivers(this.race.race_id);
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
      if (event.container.data.length >= 3) {
        // TODO add a warning on the screen for the user that no more than 3 drivers are allowed
        return;
      }
      transferArrayItem(event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }
  }

  submitPrediction() {
    const guess: Guess = {
      userId: 1, // Replace with actual user ID
      raceId: this.race.race_id,
      position1DriverId: this.prediction[0]?.driver_number,
      position2DriverId: this.prediction[1]?.driver_number,
      position3DriverId: this.prediction[2]?.driver_number
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


