import { Component } from '@angular/core';
import { ScriptService } from '../script.service';
import { SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-individual-countries',
  templateUrl: './individual-countries.component.html',
  styleUrls: ['./individual-countries.component.scss'],
})
export class IndividualCountriesComponent {
  public loading = false;
  showPrediction: boolean = false;
  showSpread: boolean = false;
  showComparison: boolean = false;
  showMap: boolean = false;
  showError: boolean = false;
  mortalityRate: number = 0.21;
  transmissionRate: number = 1.4;
  incubationPeriod: number = 5.1;
  selectedCountry: string = 'China';
  drawMap!: SafeUrl;
  spreadMap!: SafeUrl;
  plots: SafeUrl[] = [];
  constructor(private scriptService: ScriptService) {}

  runDrawMap() {
    this.loading = true;
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
        this.showSpread = false;
        this.showPrediction = false;
        this.showComparison = false;
        this.showError = false;
        this.loading = false;
      });
  }

  showFirst6Weeks() {
    this.loading = true;
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
        this.showMap = false;
        this.showSpread = true;
        this.showPrediction = false;
        this.showComparison = false;
        this.showError = false;
        this.loading = false;
      });
  }

  showPlots() {
    this.loading = true;
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
          this.showMap = false;
        this.showSpread = false;
        this.showPrediction = true;
        this.showComparison = false;
        this.showError = false;
          this.loading = false;
        });
    else {
      this.showMap = false;
      this.showSpread = false;
      this.showPrediction = true;
      this.showComparison = false;
      this.showError = false;
      this.loading = false;
    }
  }

  showComparisons() {
    this.loading = true;
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
          this.showMap = false;
          this.showSpread = false;
          this.showPrediction = false;
          this.showComparison = true;
          this.showError = false;
          this.loading = false;
        });
    else {
      this.showMap = false;
      this.showSpread = false;
      this.showPrediction = false;
      this.showComparison = true;
      this.showError = false;
      this.loading = false;
    }
  }

  showErrors() {
    this.loading = true;
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
          this.showMap = false;
          this.showSpread = false;
          this.showPrediction = false;
          this.showComparison = false;
          this.showError = true;
          this.loading=false;
        });
    else {
      this.showMap = false;
      this.showSpread = false;
      this.showPrediction = false;
      this.showComparison = false;
      this.showError = true;
      this.loading=false;
    }
  }

  onOptionChange() {
    this.showPrediction = false;
    this.showSpread = false;
    this.showComparison = false;
    this.showMap = false;
    this.showError = false;
    this.plots = [];
    this.drawMap = "";
    this.spreadMap = "";
  }
}
