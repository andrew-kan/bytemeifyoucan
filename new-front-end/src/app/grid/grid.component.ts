import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImportantTilesComponent } from '../important-tiles/important-tiles.component';
@Component({
  selector: 'app-grid',
  standalone: true,
  imports: [ImportantTilesComponent, CommonModule],
  templateUrl: './grid.component.html',
  styleUrl: './grid.component.css'
})
export class GridComponent {
  tiles = Array(9).fill(null); // Replace with your actual tile data
}
