import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NeighboringCountriesComponent } from './neighboring-countries.component';

describe('NeighboringCountriesComponent', () => {
  let component: NeighboringCountriesComponent;
  let fixture: ComponentFixture<NeighboringCountriesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NeighboringCountriesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NeighboringCountriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
