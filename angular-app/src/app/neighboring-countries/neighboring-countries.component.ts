import { Component } from '@angular/core';
import { SafeUrl } from '@angular/platform-browser';
import { ScriptService } from '../script.service';

@Component({
  selector: 'app-neighboring-countries',
  templateUrl: './neighboring-countries.component.html',
  styleUrls: ['./neighboring-countries.component.scss'],
})
export class NeighboringCountriesComponent {
  showPrediction: boolean = false;
  showSpread: boolean = false;
  showComparison: boolean = false;
  showNeighborPrediction: boolean = false;
  showMap: boolean = false;
  mortalityRate: number = 0.21;
  transmissionRate: number = 1.4;
  incubationPeriod: number = 5.1;
  selectedCountry: string = 'Austria';
  drawMap: SafeUrl | undefined;
  spreadMap: SafeUrl | undefined;
  plots: SafeUrl[] = [];
  constructor(private scriptService: ScriptService) {}

  runDrawMap() {
    this.scriptService
      .callScript(
        'run_draw_map',
        this.selectedCountry,
        this.transmissionRate,
        this.mortalityRate,
        this.incubationPeriod
      )
      .subscribe((imageUrls) => {
        this.drawMap = imageUrls[0];
        this.showMap = true;
      });
  }

  showFirst6Weeks() {
    this.scriptService
      .callScript(
        'run_spread_map_first_weeks',
        this.selectedCountry,
        this.transmissionRate,
        this.mortalityRate,
        this.incubationPeriod
      )
      .subscribe((imageUrls) => {
        this.spreadMap = imageUrls[0];
        this.showSpread = true;
      });
  }

  showPlots() {
    if (this.plots.length == 0)
      this.scriptService
        .callScript(
          'run_plots',
          this.selectedCountry,
          this.transmissionRate,
          this.mortalityRate,
          this.incubationPeriod
        )
        .subscribe((imageUrls) => {
          this.plots = imageUrls;
          this.showPrediction = true;
        });
    else {
      this.showPrediction = true;
    }
  }

  showComparisons() {
    if (this.plots.length == 0)
      this.scriptService
        .callScript(
          'run_plots',
          this.selectedCountry,
          this.transmissionRate,
          this.mortalityRate,
          this.incubationPeriod
        )
        .subscribe((imageUrls) => {
          this.plots = imageUrls;
          this.showComparison = true;
        });
    else {
      this.showComparison = true;
    }
  }

  showNeighbor() {
    if (this.plots.length == 0)
      this.scriptService
        .callScript(
          'run_plots',
          this.selectedCountry,
          this.transmissionRate,
          this.mortalityRate,
          this.incubationPeriod
        )
        .subscribe((imageUrls) => {
          this.plots = imageUrls;
          this.showNeighborPrediction = true;
        });
    else {
      this.showNeighborPrediction = true;
    }
  }

  onOptionChange() {
    this.showPrediction = false;
    this.showSpread = false;
    this.showComparison = false;
    this.showNeighborPrediction = false;
    this.showMap = false;
    this.plots = [];
    this.drawMap = undefined;
    this.spreadMap = undefined;
  }
}
