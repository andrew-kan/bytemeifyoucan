import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NoticeTilesComponent } from '../notice-tiles/notice-tiles.component';
@Component({
  selector: 'app-side-panel',
  standalone: true,
  imports: [NoticeTilesComponent, CommonModule],
  templateUrl: './side-panel.component.html',
  styleUrl: './side-panel.component.css'
})
export class SidePanelComponent {
  tiles = Array(9).fill(null); // Replace with your actual tile data

}
