import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { MainComponent } from './main/main.component';
import { IndividualCountriesComponent } from './individual-countries/individual-countries.component';
import { NeighboringCountriesComponent } from './neighboring-countries/neighboring-countries.component';

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    IndividualCountriesComponent,
    NeighboringCountriesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
