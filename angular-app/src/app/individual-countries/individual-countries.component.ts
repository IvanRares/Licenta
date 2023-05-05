import { Component } from '@angular/core';
import { ScriptService } from '../script.service';
import { SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-individual-countries',
  templateUrl: './individual-countries.component.html',
  styleUrls: ['./individual-countries.component.scss'],
})
export class IndividualCountriesComponent {
  showPrediction: boolean = false;
  showSpread: boolean = false;
  showComparison: boolean = false;
  selectedCountry: string = 'China';
  drawMap: SafeUrl | undefined;
  spreadMap: SafeUrl | undefined;
  plots: SafeUrl[] = [];
  constructor(private scriptService: ScriptService) {}

  runDrawMap() {
    this.scriptService
      .callScript('run_draw_map', this.selectedCountry)
      .subscribe((imageUrls) => {
        this.drawMap = imageUrls[0];
      });
  }

  showFirst6Weeks() {
    this.scriptService
      .callScript('run_spread_map_first_weeks', this.selectedCountry)
      .subscribe((imageUrls) => {
        this.spreadMap = imageUrls[0];
        this.showSpread = true;
      });
  }

  showPlots() {
    if (this.plots.length == 0)
      this.scriptService
        .callScript('run_plots', this.selectedCountry)
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
        .callScript('run_plots', this.selectedCountry)
        .subscribe((imageUrls) => {
          this.plots = imageUrls;
          this.showComparison = true;
        });
    else {
      this.showComparison = true;
    }
  }

  onOptionChange() {
    this.showPrediction = false;
    this.showSpread = false;
    this.showComparison = false;
    this.plots = [];
    this.drawMap = undefined;
    this.spreadMap = undefined;
  }
}
