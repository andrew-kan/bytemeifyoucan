import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NoticeTilesComponent } from '../notice-tiles/notice-tiles.component';
import { EmailService } from '../email.service';
@Component({
  selector: 'app-side-panel',
  standalone: true,
  imports: [NoticeTilesComponent, CommonModule],
  templateUrl: './side-panel.component.html',
  styleUrl: './side-panel.component.css'
})
export class SidePanelComponent {

  @Input() allEmails:any;


  
}
