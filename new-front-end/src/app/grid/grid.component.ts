import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImportantTilesComponent } from '../important-tiles/important-tiles.component';

import { EmailService } from '../email.service';
import { HttpClientModule } from '@angular/common/http';
@Component({
  selector: 'app-grid',
  standalone: true,
  imports: [ImportantTilesComponent, CommonModule, HttpClientModule ],
  templateUrl: './grid.component.html',
  styleUrl: './grid.component.css'
})
export class GridComponent {

  allEmails:any;

  constructor(private emailService:EmailService){}



  ngOnInit(){
    this.emailService.get_emails().subscribe(response => {
      this.allEmails = response;
      console.log(response)
    })
  }

  tiles = Array(9).fill(null); // Replace with your actual tile data
}
