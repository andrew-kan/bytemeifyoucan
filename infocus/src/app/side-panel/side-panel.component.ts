import { Component } from '@angular/core';
import { NoticeTilesComponent } from '../notice-tiles/notice-tiles.component';
@Component({
  selector: 'app-side-panel',
  standalone: true,
  imports: [NoticeTilesComponent],
  templateUrl: './side-panel.component.html',
  styleUrl: './side-panel.component.css'
})
export class SidePanelComponent {

}
