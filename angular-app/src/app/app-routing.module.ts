import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { IndividualCountriesComponent } from './individual-countries/individual-countries.component';
import { NeighboringCountriesComponent } from './neighboring-countries/neighboring-countries.component';

const routes: Routes = [
  { path: 'individual-countries', component: IndividualCountriesComponent },
  { path: 'neighboring-countries', component: NeighboringCountriesComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
