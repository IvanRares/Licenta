import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IndividualCountriesComponent } from './individual-countries.component';

describe('IndividualCountriesComponent', () => {
  let component: IndividualCountriesComponent;
  let fixture: ComponentFixture<IndividualCountriesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IndividualCountriesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IndividualCountriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
