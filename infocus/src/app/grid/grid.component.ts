import { Component } from '@angular/core';
import { ImportantTilesComponent } from '../important-tiles/important-tiles.component';
@Component({
  selector: 'app-grid',
  standalone: true,
  imports: [ImportantTilesComponent],
  templateUrl: './grid.component.html',
  styleUrl: './grid.component.css'
})
export class GridComponent {

}
