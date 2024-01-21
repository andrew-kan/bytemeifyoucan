import { Component } from '@angular/core';

@Component({
  selector: 'app-notice-tiles',
  standalone: true,
  imports: [],
  templateUrl: './notice-tiles.component.html',
  styleUrl: './notice-tiles.component.css'
})
export class NoticeTilesComponent {
  tiles = Array(9).fill(null); // Replace with your actual tile data
}
