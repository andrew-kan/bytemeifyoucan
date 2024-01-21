import { Component, importProvidersFrom } from '@angular/core';
import { GridComponent } from '../grid/grid.component';
import { SidePanelComponent } from '../side-panel/side-panel.component';
import { DialogOverviewExample } from '../example/dialog-overview-example';
import { provideHttpClient } from '@angular/common/http';
import { MatNativeDateModule } from '@angular/material/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideAnimations } from '@angular/platform-browser/animations';
@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [GridComponent, SidePanelComponent, DialogOverviewExample],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {



  
}

