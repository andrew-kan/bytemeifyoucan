import { Component, Input } from '@angular/core';
import { AvatarComponent } from '../avatar/avatar.component';
import { DialogOverviewExample } from '../example/dialog-overview-example';
import {MatButtonModule} from '@angular/material/button';

@Component({
  selector: 'app-important-tiles',
  standalone: true,
  imports: [AvatarComponent,MatButtonModule, DialogOverviewExample],
  templateUrl: './important-tiles.component.html',
  styleUrl: './important-tiles.component.css'
})
export class ImportantTilesComponent {
  @Input() name!:string
}
