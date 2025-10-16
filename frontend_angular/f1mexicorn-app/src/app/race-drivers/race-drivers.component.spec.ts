import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RaceDriversComponent } from './race-drivers.component';

describe('RaceDriversComponent', () => {
  let component: RaceDriversComponent;
  let fixture: ComponentFixture<RaceDriversComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RaceDriversComponent]
    });
    fixture = TestBed.createComponent(RaceDriversComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
