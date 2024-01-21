import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-notice-tiles',
  standalone: true,
  imports: [],
  templateUrl: './notice-tiles.component.html',
  styleUrl: './notice-tiles.component.css'
})
export class NoticeTilesComponent {
  @Input() tile:any;


  isNotice(category:string){
    return category != "notice"
  }
}
