import { Component, Input } from '@angular/core';
import { AvatarComponent } from '../avatar/avatar.component';
@Component({
  selector: 'app-important-tiles',
  standalone: true,
  imports: [AvatarComponent],
  templateUrl: './important-tiles.component.html',
  styleUrl: './important-tiles.component.css'
})
export class ImportantTilesComponent {
  @Input() name!:string
}
