import { Component } from '@angular/core';
import { GridComponent } from '../grid/grid.component';
import { SidePanelComponent } from '../side-panel/side-panel.component';
@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [GridComponent, SidePanelComponent],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {

}
