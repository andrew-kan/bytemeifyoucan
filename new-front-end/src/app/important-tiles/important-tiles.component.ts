import { Component, Input } from '@angular/core';
import { AvatarComponent } from '../avatar/avatar.component';
import { DialogOverviewExample } from '../example/dialog-overview-example';
import {MatButtonModule} from '@angular/material/button';
import { EmailService } from '../email.service';

@Component({
  selector: 'app-important-tiles',
  standalone: true,
  imports: [AvatarComponent,MatButtonModule, DialogOverviewExample,],
  templateUrl: './important-tiles.component.html',
  styleUrl: './important-tiles.component.css'
})
export class ImportantTilesComponent {
  @Input() name!:string
  @Input() subject!:string
  @Input() email!:any;

  constructor(private emailService:EmailService){}


  extractName(email: string): string {
    const match = email.match(/^(.*)\s<.*>$/);
    if (match && match.length > 1) {
      return match[1]; // This will be "Byteme Test"
    }
    return email; // Return the original string if no match is found
  }


  sendMail(){
    this.emailService.send_reply(this.email, this.email["reply"][0]["reply"]).subscribe(response => {
      console.log("called")
    })
  }
  
}
